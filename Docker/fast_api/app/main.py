from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from fastapi_pagination import Page, add_pagination, paginate
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
    
@app.get("/GET/v1/news", response_model=List[schemas.New])
def read_news(desde: str = "0001-01-01", hasta: str = "2022-01-01", categoria: str = "", db: Session = Depends(get_db)):
    users = crud.get_news(db, desde=desde, hasta=hasta, categoria=categoria)
    return users