"uvicorn my-api.main:app --reload"

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
########################### NEWS ###########################

@app.post("/news/", response_model=schemas.New)
def create_new(new: schemas.NewCreate, db: Session = Depends(get_db)):
    db_new = crud.get_new_by_url(db, new=new.url)
    if db_new:
        raise HTTPException(status_code=400, detail="New already registered")
    return crud.create_new(db=db, new=new)

@app.get("/GET/v1/news", response_model=[schemas.New])
def read_news(desde: str = "0001-01-01", hasta: str = "2022-01-01", db: Session = Depends(get_db)):
    return crud.get_news(db, desde = desde, hasta = hasta)

########################### CATEGORIES ###########################

@app.post("/news/{new_id}/categories/", response_model=schemas.Category)
def create_item_for_user( new_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_new_categories(db=db, category=category, new_id=new_id)


@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(crud_id : int = 1, db: Session = Depends(get_db)):
    categories = crud.get_items(db, crud_id=crud_id)
    return categories