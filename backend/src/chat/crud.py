from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from uuid import UUID
from backend.src.chat.models import Message, Chat
from datetime import datetime

from backend.src.chat.schemas import ChatCreate


# Функция для создания нового чата
async def create_chat(
        body: ChatCreate,
        session: AsyncSession,
):
    new_chat = Chat(**body.dict())
    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)
    return new_chat


async def get_chat(
        session: AsyncSession,
):
    qs = await session.execute(select(Chat))
    chat = qs.scalars().all()
    return chat


# Функция для создания нового сообщения
async def create_message(
    session: AsyncSession,
    chat_id: int,
    content: str,
    sender_id: UUID,
    receiver_id: UUID,
    file_url: Optional[str] = None,
):
    new_message = Message(
        chat_id=chat_id,
        content=content,
        sender_id=sender_id,
        receiver_id=receiver_id,
        file_url=file_url,
        created_at=datetime.utcnow(),
    )
    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)
    return new_message


async def get_all_messages(
        session: AsyncSession,
):
    result = await session.execute(select(Message))
    messages = result.scalars().all()
    return messages


# Функция для получения всех сообщений чата по message_id
async def get_messages_by_chat_id(
        message_id: int,
        session: AsyncSession,
):
    query = select(Message).where(Message.id == message_id).order_by(Message.created_at)
    result = await session.execute(query)
    return result.scalars().all()


# Функция для получения конкретного сообщения по id
async def get_message_by_id(
        session: AsyncSession,
        message_id: int
):
    query = select(Message).where(Message.id == message_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


# Функция для обновления контента сообщения
async def update_message_content(
        session: AsyncSession,
        message_id: int, new_content: str
):
    message = await get_message_by_id(session, message_id)
    if message:
        message.content = new_content
        message.created_at = datetime.utcnow()
        await session.commit()
        await session.refresh(message)
        return message
    return None


# Функция для удаления сообщения
async def delete_message(
        session: AsyncSession,
        message_id: int
):
    message = await get_message_by_id(session, message_id)
    if message:
        await session.delete(message)
        await session.commit()
        return message
    return None
