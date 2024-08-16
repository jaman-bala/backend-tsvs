from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.db.session import get_db
from backend.src.ekzamens.schemas import AnswerOUTPUT, AnswerCreate, QuestionOUTPUT, QuestionCreate
from backend.src.ekzamens.schemas import CategoryCreate, CategoryOUTPUT, CategoryUpdate, CategoryDelete
from backend.src.ekzamens.schemas import TypeSelectionCreate, TypeSelectionOUTPUT, TypeSelectionSchema, TypeSelectionUpdate, TypeSelectionDelete

from backend.src.ekzamens.crud import _create_answer, _get_answer, _get_question, _create_question
from backend.src.ekzamens.crud import _create_category, _get_category_by_id, _get_all_categories, _update_category, _delete_category
from backend.src.ekzamens.crud import _create_type_selection, _get_type_selection, _get_type_selections_by_id, _update_type_selection, _delete_type_selection

router = APIRouter()

##########################
#        CATEGORY        #
##########################


@router.post('/create/category', response_model=CategoryOUTPUT)
async def create_category(
        body: CategoryCreate,
        session: AsyncSession = Depends(get_db),
):
    created_category = await _create_category(body, session)
    return created_category


@router.get('/category_get', response_model=List[CategoryOUTPUT])
async def get_all_categories(
        session: AsyncSession = Depends(get_db),
):
    get_all_categories = await _get_all_categories(session)
    if not get_all_categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return get_all_categories


@router.get('/category_get_id/{category_id}', response_model=CategoryOUTPUT)
async def get_category_by_id(
        category_id: int,
        session: AsyncSession = Depends(get_db),
):
    category_by_id = await _get_category_by_id(category_id, session)
    return category_by_id


@router.put('/category_update/{category_id}', response_model=CategoryOUTPUT)
async def update_category(
        category_id: int,
        body: CategoryUpdate,
        session: AsyncSession = Depends(get_db),
):
    update_categories = await _update_category(category_id, body, session)
    return update_categories


@router.delete('/delete/{category_id')
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(get_db),
):
    delete_categories = await _delete_category(category_id, session)
    return delete_categories


##########################
#    TYPE_SELECTIONS     #
##########################


@router.post('/create/type_selection', response_model=TypeSelectionOUTPUT)
async def create_type_selection(
        body: TypeSelectionCreate,
        session: AsyncSession = Depends(get_db),
):
    new_type_selection = await _create_type_selection(body, session)
    return new_type_selection


@router.get('/type_selection_get', response_model=List[TypeSelectionSchema])
async def get_all_type_selections(
        session: AsyncSession = Depends(get_db),
):
    get_all_type_selections = await _get_type_selection(session)
    if not get_all_type_selections:
        raise HTTPException(status_code=404, detail="No type selections found")
    return get_all_type_selections


@router.put('/update/{type_selections_id}', response_model=TypeSelectionUpdate)
async def update_type_selection(
        type_selections_id: int,
        body: TypeSelectionUpdate,
        session: AsyncSession = Depends(get_db),
):
    update_type_selection = await _update_type_selection(type_selections_id, body, session)
    return update_type_selection

##########################
#        QUESTION        #
##########################

@router.post('/create/question')
async def create_question(
        body: QuestionCreate,
        session: AsyncSession = Depends(get_db),
):
    created_question = await _create_question(body, session)
    return created_question


@router.get('/question_get', response_model=List[QuestionOUTPUT])
async def get_all_questions(
        session: AsyncSession = Depends(get_db),
):
    get_all_questions = await _get_question(session)
    if not get_all_questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return get_all_questions
