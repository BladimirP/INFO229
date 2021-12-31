from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base, SessionLocal #Se importa el objeto Base desde el archivo database.py

db = SessionLocal()

class New(Base): 

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    date = Column(String(10))
    url = Column(String(200), unique=True)
    media_outlet = Column(String(50))
    
    categories = relationship("Category", back_populates="owner")

class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(50), index=True)
    owner_id = Column(Integer, ForeignKey("news.id"))

    owner = relationship("New", back_populates="categories")