import re
import uuid
from typing import Optional, List
from datetime import date, datetime
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import validator

from backend.src.account.user.models import PortalRole

LETTER_MATCH_PATTERN = re.compile(r"[a-zA-Zа-яА-Я\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID

    name: Optional[str] = None
    surname: Optional[str] = None
    middle_name: Optional[str] = None
    birth_year: Optional[date] = None

    email: EmailStr
    inn: Optional[int] = None
    avatar: Optional[str] = None
    job_title: Optional[str] = None

    is_active: bool
    roles: List[PortalRole]
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    middle_name: Optional[str] = None
    birth_year: Optional[date] = None

    email: EmailStr
    password: str

    inn: Optional[int] = None
    avatar: Optional[str] = None
    job_title: Optional[str] = None

    is_active: bool
    roles: List[PortalRole]
    created_at: datetime
    updated_at: datetime

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
    name: Optional[str] = None
    surname: Optional[str] = None
    middle_name: Optional[str] = None
    birth_year: Optional[date] = None

    email: EmailStr
    inn: Optional[int] = None
    avatar: Optional[str] = None
    job_title: Optional[str] = None

    is_active: bool
    role: List[str]

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
