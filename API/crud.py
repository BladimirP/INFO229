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

def insert_values(db: Session):
    new1 = models.New(title='Conflicto Mapuche', date='2021-10-18', url='https://www.elmostrador.cl/claves/conflicto-mapuche/', media_outlet='Pagina Web')
    cat11 = models.Category(value='Politica',owner=new1)
    cat12 = models.Category(value='Conflicto',owner=new1)

    new2 = models.New(title='Falsedades del Covid19', date='2021-05-12', url='https://iris.paho.org/handle/10665.2/53901', media_outlet = 'Infodemia')
    cat21 = models.Category(value='Tendencia',owner=new2)
    cat22 = models.Category(value='Salud',owner=new2)
    cat23 = models.Category(value='Global',owner=new2)

    new3 = models.New(title='Asamblea General de la ONU', date='2021-09-20', url='https://elpais.com/hemeroteca/2021-09-20/', media_outlet = 'Pagina Web')
    cat31 = models.Category(value='Politica',owner=new3)

    new4 = models.New(title='El Oporto tumba al Benfica', date='2020-12-31', url='https://as.com/futbol/2021/12/30/internacional/1640841807_994671.html', media_outlet = 'Diario web')
    cat41 = models.Category(value='Deporte',owner=new4)

    new5 = models.New(title='Quinto Retiro AFP', date='2021-12-30', url='https://chile.as.com/chile/2021/12/30/actualidad/1640860616_372550.html', media_outlet = 'Diario web')
    cat51 = models.Category(value='Economia',owner=new5)
    cat52 = models.Category(value='Politica',owner=new5)

    new6 = models.New(title='Resiliencia al Covid', date='2021-12-29', url='https://www.df.cl/noticias/economia-y-politica/pais/resiliencia-al-covid-cual-es-la-razon-del-exito-de-chile/2021-12-29/163053.html', media_outlet = 'Diario')
    cat61 = models.Category(value='Salud',owner=new6)

    db.add(new1)
    db.add(cat11)
    db.add(cat12)

    db.add(new2)
    db.add(cat21)
    db.add(cat22)
    db.add(cat23)

    db.add(new3)
    db.add(cat31)

    db.add(new4)
    db.add(cat41)

    db.add(new5)
    db.add(cat51)
    db.add(cat52)

    db.add(new6)
    db.add(cat61)

    db.commit()