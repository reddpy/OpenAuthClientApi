import re

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

    @validator("phone")
    def strip_spaces(cls, v):
        return v.strip().replace(" ", "")

    @validator("phone")
    def valid_number_regex(cls, v):
        print(v)
        regex_expression = "^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"

        match_obj = re.match(regex_expression, v)
        if not match_obj:
            raise ValueError("phone is not valid")

        return v

    @validator("phone")
    def ph_max_length(cls, v):
        wanted_chars = list("1234567890")

        valid_chars = [i for i in v if i in wanted_chars]
        print(valid_chars)

        max_length = 16
        if len(v) > max_length:
            raise ValueError("phone is not valid length")

        return "".join(valid_chars)


class UserCreate(UserBase):
    password: str
    is_active: bool = True


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
