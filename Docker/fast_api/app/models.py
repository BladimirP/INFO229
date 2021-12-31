from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base, engine #Se importa el objeto Base desde el archivo database.py

class New(Base): 

    __tablename__ = "news"

    id_news = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    date = Column(String(10))
    url = Column(String(200), unique=True)
    media_outlet = Column(String(50))
    category = Column(String(50))