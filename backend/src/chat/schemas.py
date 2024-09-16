from pydantic import BaseModel
import uuid
from typing import Optional
from datetime import datetime


class ChatCreate(BaseModel):
    title: str

    class Config:
        orm_mode = True


class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    content: str
    file_url: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    id: int
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    content: str
    file_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class MessageUpdate(BaseModel):
    content: str

    class Config:
        orm_mode = True
