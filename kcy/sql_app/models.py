from sqlalchemy import Boolean, Column, ForeignKey, Integer, VARCHAR,TIMESTAMP
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from .database import Base




class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), unique=True, index=True)
    hashed_password = Column(VARCHAR(255))
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")
    user_albums = relationship("Albums",back_populates="user_albums")
    users_permissions = relationship("Permissions",back_populates="permissions_user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(255), index=True)
    description = Column(VARCHAR(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")

"""
相册表
"""
class Albums(Base):
    __tablename__ = "albums"
    AlbumID = Column(Integer,primary_key=True)
    UserID = Column(Integer,ForeignKey("users.id"))
    AlbumName = Column(VARCHAR(100),nullable=False)
    Description = Column(VARCHAR(255),nullable=True)
    CreatedAt = Column(TIMESTAMP,nullable=False)
    user_albums = relationship("User",back_populates="user_albums")
    albums_photos = relationship("Photos",back_populates="photos_albums")

"""
图片
"""
class Photos(Base):
    __tablename__ = "photos"
    PhotoID = Column(Integer,primary_key=True)
    AlbumID = Column(Integer,ForeignKey("albums.AlbumID"))
    PhotoName = Column(VARCHAR(100),nullable=False)
    FilePath = Column(VARCHAR(255),nullable=False)
    ThumbPath = Column(VARCHAR(255),nullable=False)
    photos_albums = relationship("Albums",back_populates="albums_photos")





class Permissions(Base):
    __tablename__ = "permissions"
    UserID = Column(Integer,ForeignKey("users.id"),primary_key=True,autoincrement=False)
    AlbumID = Column(Integer,ForeignKey("albums.AlbumID"),primary_key=True,autoincrement=False)
    PermissionType = Column(VARCHAR(100),nullable=False)
    permissions_user = relationship("User",back_populates="users_permissions")


class ActivityLog(Base):
    __tablename__ = "activityLog"
    LogID = Column(Integer,primary_key=True)
    UserID = Column(Integer,ForeignKey("users.id"))
    ActivityDate = Column(TIMESTAMP,nullable=False)



