from typing import List

from pydantic import BaseModel


class EntryBase(BaseModel):
    title: str
    content: str
    status: int = 1


class EntryCreate(EntryBase):
    category_id: int


class Entry(EntryBase):
    id: int

    class Config:
        from_attributes = True


class EntryListResponse(BaseModel):
    total: int
    rows: List[Entry]


class CategoryEntry(BaseModel):
    name: str
    id: int
    entry_list: List[Entry]
    total: int

    class Config:
        from_attributes = True


class EntryListResponseByCategory(BaseModel):
    total: int
    rows: List[CategoryEntry]
