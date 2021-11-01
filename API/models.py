from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

class News(Base): 

    __tablename__ = "News"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    date = Column(Integer)
    url = Column(String(50))
    media_outlet = Column(String(50))
    value = Column(String(50))
