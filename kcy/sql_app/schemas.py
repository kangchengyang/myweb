from typing import Union
from pydantic import BaseModel, EmailStr
from datetime import datetime



class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    is_active: bool = True
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

    class Config:
        from_attributes = True


class Albums(BaseModel):
    """
    相册
    UserID:用户ID
    AlbumName:相册名称
    Description:相册描述
    CreatedAt：创建时间
    """
    UserID: int
    AlbumName: str
    Description: str
    CreatedAt: datetime


class Photos(BaseModel):
    """图片
    AlbumID：相册ID
    PhotoName：图片名称
    FilePath：图片路径
    """
    AlbumID: int
    PhotoName: str
    FilePath: str


class Permissions(BaseModel):
    """权限
    UserID:用户ID
    AlbumID:相册ID
    PermissionType:权限类型

    """
    UserID: int
    AlbumID: int
    PermissionType: str


class ActivityLog(BaseModel):
    """活动日志
    UserID：用户ID
    ActivityDate: 日志创建时间
    """
    UserID: int
    ActivityDate: datetime
