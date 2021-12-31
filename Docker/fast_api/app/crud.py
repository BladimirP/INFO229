from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true

from . import models

from . import schemas

def get_news(db: Session, desde: str, hasta: str, categoria : str):
    if (categoria == ""):
        return  db.query(models.New).filter(models.New.date >= desde, models.New.date <= hasta).all()
    else:
        return  db.query(models.New).filter(models.New.date >= desde, models.New.date <= hasta, models.New.category == categoria).all()

def get_new_by_url(db: Session, url: str):
    return db.query(models.New).filter(models.New.url == url).first()

def create_new(db: Session, new: schemas.NewCreate):
    db_new = models.New(title=new.title, url=new.url, date=new.date, media_outlet=new.media_outlet, categories= new.categories)
    db.add(db_new)
    db.commit()
    db.refresh(db_new)
    return db_new
