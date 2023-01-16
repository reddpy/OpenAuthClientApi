from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


"""
#!user payload notice
@app.get('/') will always return the full user payload
because we dont have a response model object 
being initiatived for the route. 
"""


@app.get("/")
def read_root():
    return crud.get_user(db=SessionLocal(), user_id=1)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user: models.User = crud.get_user(db=db, user_id=user_id)

    if user == None:
        raise HTTPException(404, "User does not exist")
    else:
        return user


@app.post(path="/users", response_model=schemas.User, status_code=201)
def create_user(UserData: schemas.UserCreate, db: Session = Depends(get_db)):
    found_user: models.User = crud.create_user(db=db, User=UserData)

    return found_user
