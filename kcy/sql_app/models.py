from sqlalchemy import Boolean, Column, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship
from .database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), unique=True, index=True)
    hashed_password = Column(VARCHAR(255))
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(255), index=True)
    description = Column(VARCHAR(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")