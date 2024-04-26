import uuid

from fastapi import FastAPI, Query, Path, Body, Header, Form, File, UploadFile, HTTPException, Request, Depends, Cookie, \
    status
from jose import JWTError , jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Union, Annotated, List
from uuid import UUID
from datetime import datetime, time, timedelta, timezone
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware


class Image(BaseModel):
    url: HttpUrl | None = None
    name: str


# 必须定义了BaseModel才算请求体参数
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: Union[str, None] = Field(
        default=None, examples=["The description of the item"]
    )
    price: float = Field(examples=[35.4])
    tax: Union[float, None] = Field(default=None, examples=[3.2])
    image: list[Image]


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_user_db = {
    "kcy": {
        "username": "kcy",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$.hoppvg07ABvp5/xbNlJfu43gm6CRE63j.bTq0y5iTg20W13yG8zK",
        "disabled": False
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "kcy123456",
        "disabled": True
    }
}


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserInDB(User):
    hashed_password: str


# 加密类实例化
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

aouth2_schem = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


origins = [
    "http://localhost.com",
    "https://localhost.com",
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db,username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# @app.post("/items/{item_id}")
# async def read_item(
#         item_id:Annotated[int,Path(title="1111")],
#         q: Annotated[str | None , Query(alias='item-query')] = None
#         # q: Union[str, None] = Query(
#         #     default=None ,#默认值
#         #     title="Query string", #表头
#         #     description="关于这个接口的描述", #描述
#         #     alias="item-query", #将参数声明一个别名
#         #     deprecated = True #弃用参数
#         # )
#     ):
#     results = {"item_id":item_id}
#     if q:
#         results.update({"q":q})
#     return results


# @app.post("/items/{item_id}")
# async def read_item(*,item_id:int = Path(title="The ID of the item to get",ge=1,le=3),
#                     q:str,
#                     size:float = Query(gt=2,lt=10.5)
#                     ):
#     results = {"item_id":item_id}
#     if q:
#         results["q"] = q
#     return results


# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Union[str, None] = None


# class UserIn(UserBase):
#     password: str


# class UserOut(UserBase):
#     pass

#
# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name
#
#
# items = {"foo": "The Foo Wrestlers"}
#
#
# def query_extractor(q: Union[str, None] = None):
#     return q
#
#
# def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: Union[str, None] = Cookie(default="None")):
#     if not q:
#         return last_query
#     return q
#
#
# @app.post("/query")
# async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
#     return {"q_or_cookie": query_or_default}
#
#
# # 异常处理
# @app.post("/items-header/{item_id}")
# async def read_item_header(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"item": items[item_id]}
#
#
# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
#     )
#
#
# @app.post("/unicorns/{name}")
# async def read_unicorn(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}


# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password


# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db





# 获取token


# 用密码计算哈希值
# def fake_hash_password(password: str):
#     return "kcy" + password


def get_user(db, username: str):
    print("username:", username)
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_user_db, token)
#     # print("user:",user)
#     return user


async def get_current_user(token: str = Depends(aouth2_schem)):
    print("token为:", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers= {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_user_db,username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="该用户未启用，请换一个用户")
    return current_user


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(fake_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号密码错误,请检查后再输入",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 获取用户信息
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data= {"sub":user.username},expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/users/me",response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "kcy", "owner": current_user.username}]




# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


# async def get_current_user(token: str = Depends(aouth2_schem)):
#     user = fake_decode_token(token)
#     return user


# @app.post("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user


# Bearer 11111: Bearer后面必须要加空格
@app.post("/items")
async def read_item(token: str = Depends(aouth2_schem)):
    return {"token": token}


# @app.post("/user", response_model=UserOut, status_code=500)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     # 下一步存入数据库
#     return user_saved


@app.post("/files")
async def create_file(file: UploadFile):
    return {"file": file.filename}


# 表单不能跟Body模型一起接收
@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# 响应模型返回的数据会根据 response_model=后的模型对数据进行筛选
@app.post("/user", response_model=User)
async def test_header():
    return {"username": "kcy",
            "full_name": "111",
            "id": "123"}


# 请求体最外层是一个list
@app.post("/items/multiple")
async def test_item(images: list[Image]):
    return images


# 可以在请求方法参数里面+Body去描述这个参数
@app.post("/kcy/{item_id}")
async def test2_item(
        item_id: int,
        item: Annotated[
            Item,
            Body(
                examples=[
                    {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2
                    }
                ]
            )
        ]
):
    results = {"item_id": item_id, "item": item}
    return results


# 函数内的参数有原生的数据类型，你可以，例如，执行正常的日期操作
@app.post("/time/{item_id}")
async def duration_time(
        item_id: UUID,
        start_datetime: Union[datetime, None] = Body(default=None),
        end_datetime: Union[datetime, None] = Body(default=None),
        repeat_at: Union[datetime, None] = Body(default=None),
        process_after: Union[timedelta, None] = Body(default=None)
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_datetime
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "duration": duration
    }


# 有路径参数的需要放后面
# 有默认形参的参数放在后面
# @app.post("/items/{item_id}")
# async def update_item(
#         item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#         user: User,
#         importance: Annotated[int, Body()],
#         q: str | None = None,
#         item: Item | None = None
# ):
#     results = {"items_id": item_id, "importance": importance}
#     if q:
#         results["q"] = q
#     if item:
#         results["item"] = item
#     if user:
#         results["user"] = user
#     return results


if __name__ == '__main__':
    password = "123"
    hash_password = pwd_context.hash(password)
    print(hash_password)
    # import uvicorn
    # print(uuid.uuid4())
    # uvicorn.run(app, host="127.0.0.1", port=8080)
