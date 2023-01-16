from pydantic import BaseModel, validator


class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: str

    @validator("age")
    def age_is_13(cls, v):
        if v < 13:
            raise ValueError("age must be 13 or greater")
        return v


class UserCreate(UserBase):
    password: str
    is_active: bool = True


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
