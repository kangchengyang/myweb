from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://kcy:211611.Kcy@localhost:3306/fastdb"
engin = create_engine(
    SQLALCHEMY_DATABASE_URL,echo=True
)


session_local = sessionmaker(autocommit=False, autoflush=False, bind=engin)


Base = declarative_base()
