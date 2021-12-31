from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base, SessionLocal, engine #Se importa el objeto Base desde el archivo database.py

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

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    new1 = New(title='Conflicto Mapuche', date='2021-10-18', url='https://www.elmostrador.cl/claves/conflicto-mapuche/', media_outlet='Pagina Web')
    cat11 = Category(value='Politica',owner=new1)
    cat12 = Category(value='Conflicto',owner=new1)

    new2 = New(title='Falsedades del Covid19', date='2021-05-12', url='https://iris.paho.org/handle/10665.2/53901', media_outlet = 'Infodemia')
    cat21 = Category(value='Tendencia',owner=new2)
    cat22 = Category(value='Salud',owner=new2)
    cat23 = Category(value='Global',owner=new2)

    new3 = New(title='Asamblea General de la ONU', date='2021-09-20', url='https://elpais.com/hemeroteca/2021-09-20/', media_outlet = 'Pagina Web')
    cat31 = Category(value='Politica',owner=new3)

    new4 = New(title='El Oporto tumba al Benfica', date='2020-12-31', url='https://as.com/futbol/2021/12/30/internacional/1640841807_994671.html', media_outlet = 'Diario web')
    cat41 = Category(value='Deporte',owner=new4)

    new5 = New(title='Quinto Retiro AFP', date='2021-12-30', url='https://chile.as.com/chile/2021/12/30/actualidad/1640860616_372550.html', media_outlet = 'Diario web')
    cat51 = Category(value='Economia',owner=new5)
    cat52 = Category(value='Politica',owner=new5)

    new6 = New(title='Resiliencia al Covid', date='2021-12-29', url='https://www.df.cl/noticias/economia-y-politica/pais/resiliencia-al-covid-cual-es-la-razon-del-exito-de-chile/2021-12-29/163053.html', media_outlet = 'Diario')
    cat61 = Category(value='Salud',owner=new6)

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
except:
    print("Entradas duplicadas")