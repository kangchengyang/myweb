from minio import S3Error
from sqlalchemy.orm import Session
from kcy.sql_app import models, schemas
from sqlalchemy import between, and_, desc, func
from passlib.context import CryptContext
from io import BytesIO
from datetime import datetime
from kcy.sql_app.get_md5 import generate_object_md5
from kcy.sql_app.getminio import get_minio_client
import traceback

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# def get_user_by_verify(db: Session, username: str, password: str):
#     fake_hashed_password = password + "notreallyhashed"
#     where = and_(models.User.username == username, models.User.hashed_password == fake_hashed_password)
#     resp = db.query(models.User).filter(where).first()
#     return resp


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def verify_password(plain_password, hashed_password):
    """
    该函数用于比对密码的hash值是否正确
    :param plain_password:接收的前端密码
    :param hashed_password:数据库返回的密码hash值
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    """
    :param db: 数据链接
    :param username:用户名
    :param password:前端传入的用户密码
    :return: 返回用户
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.username, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# 请求数据库返回相册
def get_albums(db: Session, start_time: str, end_time: str):
    """
    通过输入开始时间，结束时间获取相册
    :param db:
    :param start_time:
    :param end_time:
    :return:
    """
    if start_time != 'undefined' and end_time != 'undefined':
        albums = db.query(models.Albums).filter(between(models.Albums.CreatedAt, start_time, end_time)).all()
    else:
        albums = db.query(models.Albums).all()
    return albums


def get_photo_all(db: Session, albums: models.Albums):
    """
    根据提供的相册列表，获取所有图片
    :param db:
    :param album_list:相册列表
    :return:
    """
    result_list = []
    print("==========================",albums)
    for album in albums[::-1]:
        photo_by_album_id = get_photo_by_album_id(db, album),
        # print("查询到的图片", photo_by_album_id)
        result_list.append(photo_by_album_id)
    # print(result_list)
    return result_list


def get_photo_by_album_id(db: Session, albums: models.Albums):
    """
    根据相册ID获取图片
    :param db:
    :param albums:相册
    :return: 图片列表
    """
    res_dict = {}
    albums_id = int(albums.AlbumID)
    desc_str = albums.Description  # 一个相册描述
    res_dict['desc'] = desc_str
    res_dict['albumName'] = albums.AlbumName
    res_dict['photos'] = db.query(models.Photos).filter(models.Photos.AlbumID == albums_id).all()  # 相册里面的一组图片
    return res_dict


def add_photos(db: Session, photo: schemas.Photos):
    """
    kcy
    :param db: 数据链接
    :param photo: 图片
    :return: boolean
    """
    add_photo = models.Photos(**photo.dict())
    db.add(add_photo)
    db.commit()
    db.refresh(add_photo)
    return True


# 添加一个相册
def add_albums(db: Session, albums: schemas.Albums):
    """
    kcy
    :param db: 数据链接
    :param albums: 相册实体
    :return: boolean
    """
    db_albums = models.Albums(**albums.dict())
    db.add(db_albums)
    db.commit()
    db.refresh(db_albums)
    return


def get_albums_by_name(db: Session, albums: schemas.Albums):
    """
    根据相册对象获取相册
    :param db:
    :param albums:
    :return:
    """
    return db.query(models.Albums).filter(models.Albums.AlbumName == albums.AlbumName).first()


def get_photo_by_album_and_name(db: Session, albums: models.Albums, photos: schemas.Photos):
    """
    根据相册ID合图片名称判断图片是否存在
    :param db:
    :param albums:
    :param photos:
    :return:
    """
    condition = and_(models.Photos.AlbumID == albums.AlbumID, models.Photos.PhotoName == photos.PhotoName)

    return db.query(models.Photos).filter(condition).first()


def get_object(bucket_name, object_name):
    """
    在minio里面根据桶名，数据库里面的图片名取出图片
    :param bucket_name:桶名
    :param object_name:图片路径
    :return:
    """
    client = get_minio_client()
    try:
        data = client.get_object(bucket_name, object_name)
        return data
    except S3Error:
        print(S3Error)
        print(traceback.format_exc())
        return None


def get_f_object(bucket_name, object_name):
    """
    获取minio对象
    :param bucket_name:桶名
    :param object_name:文件路径
    :return:data
    """
    client = get_minio_client()
    file_name = str(object_name).split('/')[1]
    try:
        data = client.fget_object(bucket_name, object_name, file_name)
        return data
    except S3Error as s3:
        print(s3)
        return None


async def put_object(bucket_name, object_name, data):
    client = get_minio_client()
    try:
        file_contents = await data.read()
        file_io = BytesIO(file_contents)
        md_5 = generate_object_md5(file_io)
        object_name = f"{get_date_based_path()}/{md_5}.{object_name.split('.')[-1]}"
        result = client.put_object(bucket_name, object_name, file_io, length=len(file_contents),
                                   content_type=data.content_type)
        return result
    except S3Error:
        print(traceback.format_exc())
        return None


def get_date_based_path():
    # 获取当前日期并格式化为字符串
    today = datetime.now().strftime('%Y-%m-%d')
    return f"{today}"

# if __name__ == '__main__':
#    minios =  get_object("images","微信图片_20240104160506.jpg")
#    print(len(minios.data))
#    print(minios.data)
#    print(get_minio_client().list_buckets())
#    for o in get_minio_client().list_objects("images"):
#        print(o.object_name)
