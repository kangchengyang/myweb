import base64
from datetime import timedelta, datetime, timezone
from PIL import Image
from typing import Union
from io import BytesIO
import json
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File, Form, Header, Body

from jose import JWTError, jwt
import traceback
from sqlalchemy.orm import Session

from kcy.sql_app import crud, models, schemas, getminio
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from kcy.sql_app.database import session_local, engin

from fastapi.middleware.cors import CORSMiddleware

from kcy.sql_app.schemas import TokenData, Token

from kcy.sql_app.conection_redis import redis_client

from fastapi.responses import StreamingResponse

from copy import deepcopy
import random

models.Base.metadata.create_all(bind=engin)

app = FastAPI()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

IP = 'http://192.168.1.104:808'

ACCESS_TOKEN_EXPIRE_MINUTES = 30

aouth2_schem = OAuth2PasswordBearer(tokenUrl="token")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# def get_password_hash(password):
#     return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    创建token
    :param data: {"sub": user.username}
    :param expires_delta:  access_token_expires 过期时间之类的
    :return: token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(aouth2_schem), db: Session = Depends(get_db)):
    """
    用于验证请求的页面上是否存在token
    :param token:
    :param db:
    :return:
    """
    print("token为:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if str(redis_client.get(username)) != token:
            return {"code": 2002, "message": "无效token"}
        print("以下信息是前端传回后台的用户信息：")
        print(username)
        if username is None:
            return {"code": 4000, "message": "无法验证凭据"}
        token_data = TokenData(username=username)
    except JWTError:
        print(JWTError)
        return {"code": 4000, "message": "无法验证凭据"}
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        return {"code": 4000, "message": "非法操作,无法验证凭据"}
    return {"code": 2000, "message": "验证成功！"}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    :param form_data: 前端传入表单
    :param db: 数据链接
    :return: 用户token
    """
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return {"code": 2001, "message": "账号密码错误,请检查后再输入"}
    # 获取用户信息
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    redis_client.set(user.username, access_token)
    return {"code": 2000, "message": "登录成功！",
            "data": {"user": user.username, "Token": Token(access_token=access_token, token_type="bearer")}}


@app.get("/timeline")
async def load_albums(start_time: Union[str, None], end_time: Union[str, None], db: Session = Depends(get_db)):
    """
    kcy
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param db: 数据链接
    :return: 相册
    """
    print("开始请求接口")
    print("start_time", start_time)
    print("end_time", end_time)
    albums_list = crud.get_albums(db, start_time, end_time)
    photo_list = crud.get_photo_all(db, albums_list)
    data_list = {}  # 所有时间线列表
    # print(photo_list)
    for temp in photo_list:
        temp = temp[0]
        time_lien_one = {}
        photos = []
        thumbs = []  # 预览图
        print(temp)
        time_lien_one['desc'] = temp['desc']
        print("时间线描述：", time_lien_one['desc'])
        time_lien_one['time'] = str(temp['albumName'])  # 相册名就是时间名
        print(type(time_lien_one['time']))
        print("相册名", time_lien_one['time'])
        for photo in temp['photos']:
            print(photo)
            # photo_data = crud.get_object('images', photo.FilePath)
            photos.append(IP+'/timeline/images/' + photo.FilePath)
            thumbs.append(IP+'/timeline/thumb/' + str(photo.ThumbPath))
        time_lien_one['image_list'] = photos
        time_lien_one['thumb_list'] = thumbs
        data_list[time_lien_one['time']] = time_lien_one
    # print(data_list)
    return {"code": 2000, "message": "请求成功", "data": data_list}


@app.get("/timeline/{photo_type}/{time}/{filename}")
async def get_image(time: str, filename: str, photo_type: str):
    path = "/".join([time, filename])
    print(path)
    image = crud.get_object(photo_type, path)

    # print(image.data)
    if image:
        content_type = image.headers.get("content-type")
        return StreamingResponse(image, media_type=content_type)
    else:
        return {"code": 400, "message": "文件不存在"}


@app.post("/upload")
async def upload_albums(token: str = Header(), desc: str = Body(), file: UploadFile = File(...),
                        db: Session = Depends(get_db)):
    """
    :param token: 用户token
    :param desc: 相册描述
    :param file: 图片文件
    :param db:
    :return:
    """
    print("开始上传")
    # print(token)
    # print(desc)
    # 解码 JWT 的负载部分
    parts = token.split('.')
    payload_base64 = parts[1]
    payload_json = base64.urlsafe_b64decode(payload_base64).decode('utf-8')
    user_name = json.loads(payload_json)['sub']
    user = crud.get_user(db, user_name)
    # 验证 JWT 的签名
    # decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # print(decoded_token)
    # print(type(decoded_token))
    # encoded_jwt = jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)
    # 取出图片路径，判断图片是否存在
    image_path = await crud.get_md5_name(file)
    print('image_path:', image_path)
    photo_split = image_path.split('/')  # 拆分路径后的数组
    print('photo_split:', photo_split)
    today = datetime.now().strftime('%Y-%m-%d')
    print("desc",desc)
    albums = schemas.Albums(UserID=user.id, AlbumName=photo_split[0], Description=desc, CreatedAt=today)
    albums_exist = crud.get_albums_by_name(db, albums)
    # 添加相册前查看相册是否已经创建
    if albums_exist is not None:
        print("相册已经存在，不需要创建")
    else:
        print("第一次，创建相册")
        crud.add_albums(db, albums)
        print("相册创建成功")
    albums = crud.get_albums_by_name(db, albums)
    photo = schemas.Photos(AlbumID=albums.AlbumID, PhotoName=photo_split[1], FilePath=image_path, ThumbPath="")
    if crud.get_photo_by_album_and_name(db, albums, photo) is not None:
        print("图片已经在该相册存在，不需要添加")
        return {"code": 400, "message": "长传失败"}
    else:
        await file.seek(0)
        result = await crud.put_object_thumb("thumb", file.filename, file)
        thumb_object_name = result.object_name
        print("object_name:", thumb_object_name)
        await file.seek(0)
        put_object = await crud.put_object("images", file.filename, file)
        photo.ThumbPath = str(thumb_object_name)
        print(photo)
        crud.add_photos(db, photo)
        file_path = IP+'/timeline/images/' + photo.FilePath
        thumb_path = IP+'/timeline/thumb/' + photo.ThumbPath
        return {"code": 2000, "message": "长传成功",
                "data": {"time": today, 'file_path': file_path, "thumb_path": thumb_path}}


@app.get('/')
async def get_index(db: Session = Depends(get_db)):
    albums = crud.get_albums(db,'undefined','undefined')
    # print(albums[-1].AlbumName)
    photos = crud.get_photo_all(db,[albums[-1]])
    # print(photos[0][0]['photos'])
    data = [IP+'/timeline/thumb/'+i.ThumbPath for i in random.sample(photos[0][0]['photos'],5)]
    return {'code':2000,'message':'请求成功','data':data}

















@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.post("/items", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
