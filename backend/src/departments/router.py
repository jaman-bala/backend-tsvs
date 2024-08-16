import logging

from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.account.user.dals import User
from backend.src.account.auth.jwt import get_current_user_from_token
from backend.db.session import get_db
from backend.src.departments.schemas import DepartmentOUT
from backend.src.departments.schemas import DepartmentCreate
from backend.src.departments.schemas import DepartmentUpdate
from backend.src.departments.schemas import Is_activeShemasOUT

from backend.src.departments.crud import _get_all_department
from backend.src.departments.crud import _update_department
from backend.src.departments.crud import _create_department
from backend.src.departments.crud import _get_is_active
from backend.src.departments.crud import _get_department_by_id
from backend.src.departments.crud import _delete_department
from backend.src.departments.crud import _disable_department


router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log/departments.log', level=logging.INFO)


@router.post("/create/", response_model=DepartmentOUT)
async def create_departments(
    body: DepartmentCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового отдела: %s", body.title)
    new_department = await _create_department(body, session)
    return new_department


@router.get("/all/", response_model=List[DepartmentOUT])
async def read_departments(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на получение всех департаментов")

    all_departments = await _get_all_department(session)
    return all_departments


@router.get("/is_active/", response_model=List[DepartmentOUT])
async def read_active_departments(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на получение активных департаментов")

    is_active_department = await _get_is_active(session)
    return is_active_department


@router.get("/id/{departments_id}", response_model=DepartmentOUT)
async def get_departments_id(
        departments_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),

):
    logger.info(f"Получен запрос по id {departments_id}")

    departments = await _get_department_by_id(departments_id, session)
    return departments


@router.put("/update/{departments_id}", response_model=DepartmentOUT)
async def update_departments(
    departments_id: int,
    departments_update: DepartmentUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на обновление департамента")

    updated_department = await _update_department(departments_id, departments_update, session)
    return updated_department


@router.delete("/delete/{departments_id}")
async def delete_departments(
    departments_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на удаление отдела")

    await _delete_department(departments_id, session)
    return {"detail": f"Депортамент {departments_id} удален"}


@router.delete("/disable/{departments_id}", response_model=Is_activeShemasOUT)
async def disable_departments(
        departments_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на деактивацию департамента с id: %d", departments_id)

    await _disable_department(departments_id, session)
    updated_department_disabled = await _get_department_by_id(departments_id, session)

    if updated_department_disabled is None:
        raise HTTPException(status_code=404, detail="Департамент не найден")

    return updated_department_disabled
