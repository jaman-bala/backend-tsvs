from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from backend.db.session import get_db
from backend.src.chat.schemas import MessageResponse, ChatResponse, ChatCreate
from backend.src.chat.crud import create_message, get_messages_by_chat_id, delete_message, update_message_content, \
    create_chat, get_chat, get_all_messages
from backend.src.chat.websocket import connect_to_websocket, broadcast_message, disconnect_from_websocket

router = APIRouter()


@router.post("/create/chat/", response_model=ChatResponse)
async def create_chat_endpoint(
        body: ChatCreate,
        session: AsyncSession = Depends(get_db)
):
    new_chat = await create_chat(body, session)
    return new_chat


@router.get("/get/chat/", response_model=List[ChatResponse])
async def get_chat_all(
        session: AsyncSession = Depends(get_db),
):
    all_chat = await get_chat(session)
    return all_chat


@router.post("/chats/messages/", response_model=MessageResponse)
async def create_chat_message(
    chat_id: int = Form(...),
    content: str = Form(None),
    sender_id: UUID = Form(...),
    receiver_id: UUID = Form(...),
    file: UploadFile = File(None),
    session: AsyncSession = Depends(get_db),
):
    file_url = None
    if file:
        file_url = f"static/files/{file.filename}"
        with open(file_url, "wb") as f:
            f.write(await file.read())

    new_message = await create_message(
        session=session,
        chat_id=chat_id,
        content=content,
        sender_id=sender_id,
        receiver_id=receiver_id,
        file_url=file_url,

    )
    return new_message


@router.get("/get_all/messages/", response_model=List[MessageResponse])
async def get_messages_all(
        session: AsyncSession = Depends(get_db),
):
    all_messages = await get_all_messages(session)
    return all_messages


@router.get("/chats/{chat_id}/messages/", response_model=List[MessageResponse])
async def get_chat_messages_id(
        chat_id: int,
        session: AsyncSession = Depends(get_db),
):
    messages = await get_messages_by_chat_id(chat_id, session)
    if not messages:
        raise HTTPException(status_code=404, detail="Messages not found")
    return messages


@router.put("/messages/{message_id}/", response_model=MessageResponse)
async def update_message(message_id: int, new_content: str, db: AsyncSession = Depends(get_db)):
    updated_message = await update_message_content(db, message_id, new_content)
    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message


@router.delete("/messages/{message_id}/", response_model=MessageResponse)
async def delete_chat_message(message_id: int, db: AsyncSession = Depends(get_db)):
    deleted_message = await delete_message(db, message_id)
    if not deleted_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return deleted_message


@router.websocket("/ws/chats/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await websocket.accept()
    await connect_to_websocket(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Получаем данные
            await broadcast_message(f"Chat {chat_id}: {data}")  # Отправляем всем клиентам
            print(f"Broadcasting message: {chat_id}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await disconnect_from_websocket(websocket)
