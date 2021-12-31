from typing import List, Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    value: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class NewBase(BaseModel):
    pass


class NewCreate(NewBase):
    pass


class New(NewBase):
    id: int
    title: str
    url: str
    date: str
    media_outlet: str
    categories: List[Category] = []

    class Config:
        orm_mode = True


