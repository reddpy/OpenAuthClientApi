from fastapi import FastAPI

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

from .schema import *

app = FastAPI()


@app.get("/")
def read_root():
    return {"hello": "world"}
