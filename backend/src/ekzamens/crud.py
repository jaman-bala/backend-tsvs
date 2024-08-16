from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from backend.src.ekzamens.models import Question, Answer, Category, TypeSelection
from backend.src.ekzamens.schemas import AnswerCreate, AnswerUpdate
from backend.src.ekzamens.schemas import QuestionCreate, QuestionUpdate
from backend.src.ekzamens.schemas import CategoryCreate, CategoryUpdate, CategoryDelete
from backend.src.ekzamens.schemas import TypeSelectionCreate, TypeSelectionUpdate


##########################
#        CATEGORY        #
##########################


async def _create_category(
        body: CategoryCreate,
        session: AsyncSession
):
    db_category = Category(**body.dict())
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category


async def _get_all_categories(session: AsyncSession):
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return categories


async def _get_category_by_id(
        category_id: int,
        session: AsyncSession,
):
    query = select(Category).where(Category.id == category_id)
    result = await session.execute(query)
    category = result.scalar_one_or_none()
    return category


async def _update_category(
        category_id: int,
        body: CategoryUpdate,
        session: AsyncSession,
):
    db_category = await _get_category_by_id(category_id, session)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.title = body.title
    await session.commit()
    return db_category


async def _delete_category(
        category_id: int,
        session: AsyncSession,
):
    db_category = await _get_category_by_id(category_id, session)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(db_category)
    await session.commit()
    return db_category


##########################
#    TYPE_SELECTIONS     #
##########################


async def _create_type_selection(
        body: TypeSelectionCreate,
        session: AsyncSession
):
    db_type_selection = TypeSelection(**body.dict())
    session.add(db_type_selection)
    await session.commit()
    await session.refresh(db_type_selection)
    return db_type_selection


async def _get_type_selection(session: AsyncSession):
    result = await session.execute(select(TypeSelection))
    type_selections = result.scalars().all()
    return type_selections


async def _get_type_selections_by_id(
        type_selection_id: int,
        session: AsyncSession,
):
    query = select(TypeSelection).where(TypeSelection.id == type_selection_id)
    result = await session.execute(query)
    type_selection = result.scalar_one_or_none()
    return type_selection


async def _update_type_selection(
        type_selection_id: int,
        body: TypeSelectionUpdate,
        session: AsyncSession,
):
    db_type_selection = await _get_type_selections_by_id(type_selection_id, session)
    if db_type_selection is None:
        raise HTTPException(status_code=404, detail="Type Selection not found")
    db_type_selection.title = body.title
    await session.commit()
    return db_type_selection


async def _delete_type_selection(
        type_selection_id: int,
        session: AsyncSession,
):
    db_type_selection = await _get_type_selections_by_id(type_selection_id, session)
    if db_type_selection is None:
        raise HTTPException(status_code=404, detail="Type Selection not found")
    await session.delete(db_type_selection)
    await session.commit()
    return db_type_selection


##########################
#        ANSWER          #
##########################
async def _create_answer(
        body: AnswerCreate,
        session: AsyncSession,
):
    db_answer = Answer(**body.dict())
    session.add(db_answer)
    await session.commit()
    await session.refresh(db_answer)
    return db_answer


async def _get_answer(session: AsyncSession):
    result = await session.execute(select(Answer))
    answers = result.scalars().all()
    return answers


async def _get_answer_by_id(
        answer_id: int,
        session: AsyncSession,
):
    query = select(Answer).where(Answer.id == answer_id)
    result = await session.execute(query)
    answer = result.scalar_one_or_none()
    return answer


##########################
#        QUESTION        #
##########################

async def _create_question(
        body: QuestionCreate,
        session: AsyncSession
):
    db_question = Question(title=body.title)
    session.add(db_question)
    await session.commit()
    await session.refresh(db_question)

    if body.answers:
        for answer_data in body.answers:
            db_answer = Answer(
                text=answer_data.text,
                is_correct=answer_data.is_correct,
                question_id=db_question.id
            )
            session.add(db_answer)
        await session.commit()

    return db_question


async def _get_question(session: AsyncSession):
    result = await session.execute(select(Question).options(selectinload(Question.answers)))
    questions = result.scalars().all()
    return questions


async def _get_question_by_id(
        question_id: int,
        session: AsyncSession,
):
    query = select(Question).where(Question.id == question_id).options(selectinload(Question.answers))
    result = await session.execute(query)
    question = result.scalar_one_or_none()
    return question


async def _update_question(
        question_id: int,
        body: QuestionUpdate,
        session: AsyncSession,
):
    db_question = await _get_question_by_id(question_id, session)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # Обновляем основные поля вопроса
    db_question.title = body.title
    db_question.category_id = body.category_id
    db_question.type_select_id = body.type_selection_id

    # Обновляем ответы
    if body.answers:
        existing_answer_ids = [answer.id for answer in db_question.answers]
        incoming_answer_ids = [answer.id for answer in body.answers if answer.id]

        # Удаляем ответы, которые отсутствуют в входных данных
        for answer in db_question.answers:
            if answer.id not in incoming_answer_ids:
                await session.delete(answer)

        # Обновляем существующие ответы и добавляем новые
        for answer_data in body.answers:
            if answer_data.id in existing_answer_ids:
                db_answer = next(answer for answer in db_question.answers if answer.id == answer_data.id)
                db_answer.text = answer_data.text
                db_answer.is_correct = answer_data.is_correct
            else:
                new_answer = Answer(
                    text=answer_data.text,
                    is_correct=answer_data.is_correct,
                    question_id=db_question.id
                )
                session.add(new_answer)

    await session.commit()
    await session.refresh(db_question)

    return db_question


async def _delete_question(
        question_id: int,
        session: AsyncSession,
):
    db_question = await _get_question_by_id(question_id, session)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    await session.delete(db_question)
    await session.commit()

    return db_question
