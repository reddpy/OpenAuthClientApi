from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: str

class UserCreate(UserBase):
    password: str
    is_active: bool = True

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
