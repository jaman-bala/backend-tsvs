import re
import uuid
from typing import Optional, List
from datetime import date, datetime
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import validator


LETTER_MATCH_PATTERN = re.compile(r"[a-zA-Zа-яА-Я\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    avatar: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    birth_year: date
    email: EmailStr

    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserCreate(BaseModel):
    avatar: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    email: EmailStr
    birth_year: date
    password: str


    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    avatar: Optional[str]
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]
    birth_year: date

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class ResetPasswordRequest(BaseModel):
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
