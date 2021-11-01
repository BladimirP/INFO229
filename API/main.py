"uvicorn my-api.main:app --reload"

from typing import List

from sqlalchemy.sql.sqltypes import String

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


@app.get("/GET/v1/news", response_model=schemas.News)
def read_user(desde: int, hasta: int, category: str):
    return crud.get_news(db, datei = desde, datef = hasta, cat = category)
