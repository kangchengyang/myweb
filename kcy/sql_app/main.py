from datetime import timedelta, datetime, timezone
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from kcy.sql_app import crud, models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from kcy.sql_app.database import session_local, engin

from fastapi.middleware.cors import CORSMiddleware

from kcy.sql_app.schemas import TokenData, Token

from kcy.sql_app.conection_redis import redis_client

models.Base.metadata.create_all(bind=engin)

app = FastAPI()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
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


# @app.post('/login')
# def login(user: schemas.User, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_verify(db, user.username, user.password)
#     if db_user is None:
#         return {"code": 2001, "message": "账号密码错误"}
#     return {"code": 2000, "message": "登录成功", "data": db_user}


@app.post("/users/{user_id}", response_model=list[schemas.User])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="该用户没找到")
    return [db_user]


@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.post("/items", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
