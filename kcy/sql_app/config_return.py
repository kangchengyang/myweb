from pydantic import BaseModel
from kcy.sql_app.schemas import User


# 配置返回的模型
class responseUserModel(BaseModel):
    id: str
    name: str


class responseData(BaseModel):
    message: str
    code: str
    data: responseUserModel
