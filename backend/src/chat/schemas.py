# schemas.py
from datetime import datetime

from pydantic import BaseModel

class ChatCreate(BaseModel):
    name: str

class MessageCreate(BaseModel):
    chat_id: int
    sender_id: str  # ID отправителя
    receiver_id: str  # ID получателя
    content: str

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: str
    receiver_id: str
    content: str
    created_at: datetime
