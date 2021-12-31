from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true

from . import models, schemas

######################## NEWS ######################

def get_news(db: Session, desde: str, hasta: str, categoria : str):
    if (categoria == ""):
        return  db.query(models.New).filter(models.New.date >= desde, models.New.date <= hasta).all()
    else:
        ids = db.query(models.Category.owner_id).filter(models.Category.value == categoria)
        h = []
        for i in ids:
            h.append(i[0])
        return  db.query(models.New).filter(models.New.date >= desde, models.New.date <= hasta, models.New.id.in_(h)).all()

def get_new_by_url(db: Session, url: str):
    return db.query(models.New).filter(models.New.url == url).first()

def create_new(db: Session, new: schemas.NewCreate):
    db_new = models.New(title=new.title, url=new.url, date=new.date, media_outlet=new.media_outlet)
    db.add(db_new)
    db.commit()
    db.refresh(db_new)
    return db_new

######################## CATEGORIES ######################

def get_categories(db: Session, owner_id: int):
    return db.query(models.Category).filter(models.Category.owner_id == owner_id).all()

def create_categories(db: Session, category: schemas.CategoryCreate, new_id: int):
    db_category = models.Category(**category.dict(), owner_id=new_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

############################### funciones auxiliares ###########################

def aux(recorrer, comparar):
    print(recorrer)
    print(type(recorrer))
    for i in recorrer:
        if (i.value == comparar):
            return True
    return False
