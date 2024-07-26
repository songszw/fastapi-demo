from typing import List

from pydantic import BaseModel


class EntryBase(BaseModel):
    title: str
    content: str
    status: int = 1
    category_id: int


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    id: int

    class Config:
        from_attributes = True


class EntryUpdate(EntryBase):
    id: int


class EntryDelete(EntryBase):
    pass


class EntryDeleteResponse(BaseModel):
    status: int
    message: str
    id: int


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
