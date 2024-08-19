from pydantic import BaseModel
from typing import List, Any, TypeVar, Generic, Optional

T = TypeVar('T')


class ResponseModel:
    def __init__(self, code: int, message: str, data: any = None):
        self.code = code
        self.message = message
        self.data = data


class ResponseListModel(BaseModel, Generic[T]):
    code: int
    rows: List[T]
    total: int


class ResponseDataModel(BaseModel, Generic[T]):
    code: int
    data: Optional[T] = None
    message: str


class ResponseDeleteModel(BaseModel, Generic[T]):
    code: int
    message: str
    id: int
