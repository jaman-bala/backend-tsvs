from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Union
from fastapi import HTTPException

from backend.src.departments.schemas import DepartmentSchemas
from backend.src.departments.schemas import DepartmentCreate
from backend.src.departments.schemas import DepartmentUpdate
from backend.src.departments.models import Departments


async def _create_department(
        body: DepartmentCreate,
        session: AsyncSession,
        ):
    db_departments = Departments(**body.dict())
    session.add(db_departments)
    await session.commit()
    await session.refresh(db_departments)
    return db_departments


async def _get_all_department(session: AsyncSession):
    result = await session.execute(select(Departments))
    departments = result.scalars().all()
    return departments


async def _get_is_active(session: AsyncSession):
    query = select(Departments).where(Departments.is_active == True)
    res = await session.execute(query)
    return res.scalars().all()


async def _get_department_by_id(
        department_id: int,
        session: AsyncSession,
        ) -> Union[DepartmentSchemas, None]:
    query = select(Departments).where(Departments.id == department_id)
    res = await session.execute(query)
    if res is None:
        raise HTTPException(status_code=404, detail="Департамент не найден")
    return res.scalar_one_or_none()


async def _update_department(
    department_id: int,
    body: DepartmentUpdate,
    session: AsyncSession,
) -> DepartmentSchemas:
    db_department = await _get_department_by_id(department_id, session)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Департамент не найден")
    db_department.title = body.title
    db_department.is_active = body.is_active

    session.add(db_department)
    await session.commit()
    await session.refresh(db_department)
    return db_department


async def _delete_department(
    department_id: int,
    session: AsyncSession,
):
    db_department = await _get_department_by_id(department_id, session)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Департамент не найден")
    await session.delete(db_department)
    await session.commit()
    return db_department


async def _disable_department(
        department_id: int,
        session: AsyncSession,
):
    db_department = await _get_department_by_id(department_id, session)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Департамент не найден")

    if not db_department.is_active:
        raise HTTPException(status_code=400, detail="Департамент уже отключен")

    db_department.is_active = False
    await session.commit()
    return db_department



