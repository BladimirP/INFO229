from typing import List, Optional

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    date: int
    url: str
    media_outlet: str
    value: str


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int

    class Config:
        orm_mode = True


