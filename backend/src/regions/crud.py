from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Union
from fastapi import HTTPException

from backend.src.regions.schemas import RegionCreate
from backend.src.regions.schemas import RegionSchemas
from backend.src.regions.schemas import RegionUpdate
from backend.src.regions.models import Region


async def _create_region(
        body: RegionCreate,
        session: AsyncSession,
        ) -> RegionSchemas:
    db_region = Region(**body.dict())
    session.add(db_region)
    await session.commit()
    await session.refresh(db_region)
    return db_region


async def _get_all_regions(session: AsyncSession):
    result = await session.execute(select(Region))
    regions = result.scalars().all()
    return regions


async def _get_is_active(session: AsyncSession):
    query = select(Region).where(Region.is_active == True)
    res = await session.execute(query)
    return res.scalars().all()


async def _get_region_by_id(
        region_id: int,
        session: AsyncSession,
        ) -> Union[RegionSchemas, HTTPException]:
    query = select(Region).where(Region.id == region_id)
    res = await session.execute(query)
    if res is None:
        raise HTTPException(status_code=404, detail="Регион не найден")
    return res.scalar_one_or_none()


async def _update_region(
        region_id: int,
        body: RegionUpdate,
        session: AsyncSession,
) -> RegionSchemas:
    db_region = await _get_region_by_id(region_id, session)
    if db_region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")
    db_region.title = body.title
    db_region.is_active = body.is_active

    session.add(db_region)
    await session.commit()
    await session.refresh(db_region)
    return db_region


async def _delete_region(
        region_id: int,
        session: AsyncSession,
):
    db_region = await _get_region_by_id(region_id, session)
    if db_region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")
    await session.delete(db_region)
    await session.commit()
    return db_region


async def _disable_region(
        region_id: int,
        session: AsyncSession,
):
    db_region = await _get_region_by_id(region_id, session)
    if db_region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")

    if not db_region.is_active:
        raise HTTPException(status_code=400, detail="Регион уже отключен")

    db_region.is_active = False
    await session.commit()
    return db_region
