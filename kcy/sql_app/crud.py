from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import between
from passlib.context import CryptContext

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
    if start_time != 'undefined' and end_time != 'undefined':
        albums = db.query(models.Albums).filter(between(models.Albums.CreatedAt, start_time, end_time)).all()
    else:
        albums = db.query(models.Albums).limit(5).all()
    return albums
