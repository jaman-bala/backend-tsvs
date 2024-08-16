import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

BaseExam = declarative_base()


class Category(BaseExam):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="category")

    def __str__(self):
        return self.title


class TypeSelection(BaseExam):

    __tablename__ = 'type_selections'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="type_select")

    def __str__(self):
        return self.title


class Question(BaseExam):

    __tablename__ = 'questions'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("Answer", back_populates="question")
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="questions")

    type_select_id = Column(Integer, ForeignKey('type_selections.id'))
    type_select = relationship("TypeSelection", back_populates="questions")

    def __str__(self):
        return self.title


class Answer(BaseExam):

    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False, server_default='false')
    created_at = Column(DateTime, default=datetime.utcnow)

    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="answers")

    def __str__(self):
        return self.text
