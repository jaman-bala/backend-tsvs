# router.py
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from backend.db.session import get_db
from backend.src.chat.api_utils import get_users
from backend.src.chat.models import Chat, Message
from backend.src.chat.schemas import ChatCreate, MessageCreate, MessageResponse

router = APIRouter()

@router.post("/chats/", response_model=ChatCreate)
async def create_chat(chat: ChatCreate, db: AsyncSession = Depends(get_db)):
    db_chat = Chat(name=chat.name)
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    return db_chat

@router.post("/chats/{chat_id}/messages/", response_model=MessageResponse)
async def create_message(chat_id: int, message: MessageCreate, db: AsyncSession = Depends(get_db)):
    db_message = Message(
        chat_id=chat_id,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

@router.get("/chats/{chat_id}/messages/", response_model=List[MessageResponse])
async def read_messages(chat_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Message).filter(Message.chat_id == chat_id))
    messages = result.scalars().all()
    return messages

# Обработчик для загрузки файлов
@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        with open(f"static/files/{file.filename}", "wb") as f:
            f.write(contents)
    return {"filenames": [file.filename for file in files]}

@router.get("/users/")
async def list_users():
    users = await get_users()
    return users
