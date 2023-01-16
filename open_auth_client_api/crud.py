from fastapi import HTTPException
from sqlalchemy.orm import Session

from utils.password import hash_password

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, User: schemas.UserCreate):
    existing_ph_user = (
        db.query(models.User).filter(models.User.phone == User.phone).first()
    )

    if existing_ph_user:
        raise HTTPException(status_code=422, detail="User with phone already exists")

    new_user = models.User(
        first_name=User.first_name,
        last_name=User.last_name,
        age=User.age,
        phone=User.phone,
        hashed_password=hash_password(user_password=User.password),
        is_active=User.is_active,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
