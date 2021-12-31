from typing import List, Optional

from pydantic import BaseModel

class NewBase(BaseModel):
    pass


class NewCreate(NewBase):
    pass


class New(NewBase):
    id_news: int
    title: str
    url: str
    date: str
    media_outlet: str
    category: str

    class Config:
        orm_mode = True


