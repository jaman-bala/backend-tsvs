from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CategorySchema(BaseModel):
    id: int
    title: str = None
    created_at: datetime = None

    class Config:
        orm_mode = True


class CategoryCreate(BaseModel):
    title: str = None

    class Config:
        orm_mode = True


class CategoryUpdate(CategoryCreate):
    pass


class CategoryDelete(BaseModel):
    id: int

    class Config:
        orm_mode = True


class CategoryOUTPUT(BaseModel):
    id: int
    title: str = None

    class Config:
        orm_mode = True


class TypeSelectionSchema(BaseModel):
    id: int
    title: str = None
    created_at: datetime = None

    class Config:
        orm_mode = True


class TypeSelectionCreate(BaseModel):
    title: str = None

    class Config:
        orm_mode = True


class TypeSelectionUpdate(BaseModel):
    title: str = None

    class Config:
        orm_mode = True


class TypeSelectionDelete(TypeSelectionSchema):
    id: int

    class Config:
        orm_mode = True


class TypeSelectionOUTPUT(BaseModel):
    id: int
    title: str = None

    class Config:
        orm_mode = True


class AnswerSchema(BaseModel):
    id: UUID
    text: str
    is_correct: bool
    created_at: datetime

    class Config:
        orm_mode = True


class AnswerCreate(BaseModel):
    text: str
    is_correct: bool


class AnswerUpdate(BaseModel):
    text: str
    is_correct: bool


class AnswerDelete(AnswerSchema):
    id: UUID


class AnswerOUTPUT(BaseModel):
    id: UUID
    text: str
    is_correct: bool


class QuestionSchema(BaseModel):
    title: str
    created_at: datetime
    answers: List[AnswerOUTPUT]

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    title: str
    category_id: int
    type_select_id: int
    answers: List[AnswerCreate]


class QuestionUpdate(BaseModel):
    title: str
    category_id: int
    type_select_id: int
    answers: List[AnswerUpdate]


class QuestionDelete(BaseModel):
    question_id: UUID
    title: str


class QuestionOUTPUT(BaseModel):
    question_id: UUID
    title: str
    category_id: int
    type_select_id: int
    answers: List[AnswerOUTPUT]

    class Config:
        orm_mode = True
