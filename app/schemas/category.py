from typing import List

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    status: int = 1


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    id: int


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryDelete(BaseModel):
    status: int
    message: str
    category_id: int


class CategoryInfoResponse(BaseModel):
    code: int
    data:  Category


class CategoryDeleteResponse(BaseModel):
    code: int
    message: str
    id: int


class CategoryListResponse(BaseModel):
    code: int
    total: int
    rows: List[Category]
