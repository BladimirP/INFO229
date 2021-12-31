"uvicorn my-api.main:app --reload"

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
try:
    crud.insert_values(SessionLocal())
except:
    print("Entradas duplicadas")
########################### NEWS ###########################

@app.post("/news/", response_model=schemas.New)
def create_new(new: schemas.NewCreate, db: Session = Depends(get_db)):
    db_new = crud.get_new_by_url(db, new=new.url)
    if db_new:
        raise HTTPException(status_code=400, detail="New already registered")
    return crud.create_new(db=db, new=new)

#
@app.get("/GET/v1/news", response_model=List[schemas.New])
def read_news(desde: str = "0001-01-01", hasta: str = "2022-01-01", categoria: str = "", db: Session = Depends(get_db)):
    users = crud.get_news(db, desde=desde, hasta=hasta, categoria=categoria)
    return users

########################### CATEGORIES ###########################

@app.post("/news/{new_id}/categories/", response_model=schemas.Category)
def create_item_for_user( new_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_new_categories(db=db, category=category, new_id=new_id)


@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(owner_id : int = 1, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, owner_id=owner_id)
    return categories