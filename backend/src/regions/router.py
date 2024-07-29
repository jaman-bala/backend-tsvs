import logging

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.src.account.user.dals import User
from backend.src.account.auth.jwt import get_current_user_from_token
from backend.db.session import get_db
from backend.src.regions.schemas import RegionOUT, RegionCreate, RegionUpdate
from backend.src.regions.models import Region


router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log/regions.log', level=logging.INFO)

#######################
# REGION ROUTER
#######################


@router.post("/create/", response_model=RegionOUT)
async def create_region(
        region: RegionCreate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового региона: %s", region.title)

    db_region = Region(**region.dict())
    session.add(db_region)
    await session.commit()
    await session.refresh(db_region)
    logger.info("Новый регион успешно создан: %s", db_region.title)
    return db_region


@router.get("/all/", response_model=List[RegionOUT])
async def read_regions(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на вывод всех пользователей")

    result = await session.execute(select(Region))
    regions = result.scalars().all()
    return regions


@router.get("/is_active/", response_model=List[RegionOUT])
async def read_active_regions(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на вывод активных регионов")

    stmt = select(Region).filter(Region.is_active)
    result = await session.execute(stmt)
    regions = result.scalars().all()
    return regions


@router.get("/id/{region_id}", response_model=RegionOUT)
async def get_regions_id(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос по id")

    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")
    return region


@router.put("/update/{region_id}", response_model=RegionOUT)
async def update_region(
        region_id: int,
        region_update: RegionUpdate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на обновление региона")

    # Получаем регион из базы данных
    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")

    # Обновляем поля региона
    region.title = region_update.title

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем обновленный регион
    return region


@router.delete("/delete/{region_id}")
async def delete_region(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на удаление региона")

    # Получаем регион из базы данных
    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")

    # Удаляем регион из базы данных
    await session.delete(region)
    await session.commit()

    # Возвращаем удаленный регион
    return {"message": f"Регион {region_id} удален"}


@router.delete("/disabled/{region_id}")
async def is_active(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на удаление региона")
    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")
    region.is_active = False
    await session.commit()
    return {"message": f"Регион {region_id} не активный"}
