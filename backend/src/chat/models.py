from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Integer
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime



BaseChat = declarative_base()

class Chat(BaseChat):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    messages = relationship('Message', back_populates='chat')

class Message(BaseChat):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    chat = relationship('Chat', back_populates='messages')
    sender_id = Column(String)  # ID отправителя
    receiver_id = Column(String)  # ID получателя
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
