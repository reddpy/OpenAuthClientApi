from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, User: schemas.UserCreate):
    new_user = models.User(
        first_name=User.first_name,
        last_name=User.last_name,
        age=User.age,
        phone=User.phone,
        hashed_password=User.password,
        is_active=User.is_active,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
