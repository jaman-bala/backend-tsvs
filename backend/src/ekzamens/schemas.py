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
    id: int
    text: str = None
    is_correct: bool = None
    created_at: datetime = None

    class Config:
        orm_mode = True


class AnswerCreate(AnswerSchema):
    text: str = None
    is_correct: bool = None

    class Config:
        orm_mode = True


class AnswerUpdate(AnswerCreate):
    pass


class AnswerDelete(AnswerSchema):
    id: int

    class Config:
        orm_mode = True


class AnswerOUTPUT(BaseModel):
    id: int
    text: str = None
    is_correct: bool = None

    class Config:
        orm_mode = True


class QuestionSchema(BaseModel):
    id: int
    title: str = None
    created_at: datetime = None
    answers: List[AnswerOUTPUT] = None

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    title: str
    category_id: int = None
    type_selection_id: int = None
    answers: List[AnswerCreate] = None

    class Config:
        orm_mode = True


class QuestionUpdate(QuestionSchema):
    pass


class QuestionDelete(QuestionSchema):
    id: int

    class Config:
        orm_mode = True


class QuestionOUTPUT(BaseModel):
    id: int
    title: str = None
    category_id: int = None
    type_selection_id: int = None
    answers: List[AnswerOUTPUT] = None

    class Config:
        orm_mode = True
