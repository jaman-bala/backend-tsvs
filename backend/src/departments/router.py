import logging

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.src.account.user.dals import User
from backend.src.account.auth.jwt import get_current_user_from_token
from backend.db.session import get_db
from backend.src.departments.schemas import DepartmentOUT, DepartmentCreate, DepartmentUpdate
from backend.src.departments.models import Departments

router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log/departments.log', level=logging.INFO)


@router.post("/create/", response_model=DepartmentOUT)
async def post_departments(
    departments: DepartmentCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового отдела: %s", departments.title)

    db_departments = Departments(**departments.dict())
    session.add(db_departments)
    await session.commit()
    await session.refresh(db_departments)
    logger.info("Новый отдел успешно создан: %s", db_departments.title)
    return db_departments


@router.get("/all/", response_model=List[DepartmentOUT])
async def read_departments(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на получение всех департаментов")

    result = await session.execute(select(Departments))
    departments = result.scalars().all()
    return departments


@router.get("/is_active/", response_model=List[DepartmentOUT])
async def read_departments(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на получение активных департаментов")

    stmt = select(Departments).filter(Departments.is_active)
    result = await session.execute(stmt)
    departments = result.scalars().all()
    return departments


@router.get("/id/{departments_id}", response_model=DepartmentOUT)
async def get_departments(
        departments_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),

):
    logger.info("Получен запрос по id")

    departments = await session.get(Departments, departments_id)
    if departments is None:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    return departments


@router.put("/update/{departments_id}", response_model=DepartmentOUT)
async def update_departments(
        departments_id: int,
        departments_update: DepartmentUpdate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),

):
    logger.info("Получен запрос на обновление департамента")

    departments = await session.get(Departments, departments_id)
    if departments is None:
        raise HTTPException(status_code=404, detail="Отдел не найден")

    departments.title = departments_update.title

    await session.commit()
    return departments


@router.delete("/delete/{departments_id}")
async def delete_departments(
        departments_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на удаление отдела")

    departments = await session.get(Departments, departments_id)
    if departments is None:
        raise HTTPException(status_code=404, detail="Отдел не найден")

    departments.is_active = False

    await session.commit()
    return departments


@router.delete("/disabled/{region_id}")
async def is_active(
        departments_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на удаление региона")
    departments = await session.get(Departments, departments_id)
    if departments is None:
        raise HTTPException(status_code=404, detail="Департамент не найден")
    departments.is_active = False
    await session.commit()
    return {"message": f"Департамент {departments_id} не активный"}
