from sqlalchemy.orm import Session

from . import models, schemas


def get_news(db: Session, datei: int, datef: int, cate: str):
    return  db.query(models.News).filter(models.News.date > datei and models.News.date < datef and models.News.value == cate)

