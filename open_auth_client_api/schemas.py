import re
from typing import Union

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: str

    @validator("age")
    def age_is_13(cls, v):
        min_age: int = 13

        if v < min_age:
            error_msg = "age must be %d or greater" % min_age
            raise ValueError(error_msg)
            
        return v

    @validator("phone")
    def strip_spaces(cls, v):
        return v.strip().replace(" ", "")

    @validator("phone")
    def valid_number_regex(cls, v):
        regex_expression: str = "^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$"

        match_obj: re = re.match(regex_expression, v)
        if not match_obj:
            raise ValueError("phone is not valid")

        return v

    @validator("phone")
    def ph_max_length(cls, v):
        wanted_chars: list[str] = list("1234567890")
        valid_chars: list[str] = [i for i in v if i in wanted_chars]
        max_length: int = 16

        if len(v) > max_length:
            raise ValueError("phone is not valid length")

        return "".join(valid_chars)


class UserCreate(UserBase):
    password: str
    is_active: bool = True

    @validator("password")
    def pass_validate_length(cls, v):
        pass_len: int = 10

        if len(v) < pass_len:
            error_msg: str = "Password must be length of %d or greater" % pass_len
            raise ValueError(error_msg)

        return v

    @validator("password")
    def pass_validate_upper(cls, v):
        has_upper: list[bool] = [bool(letter) for letter in v if letter[0].istitle()]

        if len(has_upper) < 1:
            raise ValueError("Password must contain at least one uppercase character")

        return v

    @validator("password")
    def pass_special_chars(cls, v):
        special_chars: re = re.search("[@_!#$%^&*()<>?/\|}{~:;]", v)

        if not special_chars:
            raise ValueError("Password must contain at least one special character")

        return v


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
