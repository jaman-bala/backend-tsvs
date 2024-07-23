import logging

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.src.account.user.dals import User
#from backend.src.account.auth.auth import get_current_user_from_token
from backend.db.session import get_db
from backend.src.regions.schemas import RegionOUT, RegionCreate, RegionUpdate
from backend.src.regions.models import Region


router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log/regions.log', level=logging.INFO)

#######################
# REGION ROUTER
#######################


@router.post("/regions/", response_model=RegionOUT)
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


@router.get("/regions/", response_model=List[RegionOUT])
async def read_regions(
        session: AsyncSession = Depends(get_db),
    #    current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    result = await session.execute(select(Region))
    regions = result.scalars().all()
    return regions


@router.get("/regions/{region_id}", response_model=RegionOUT)
async def get_regions(
        region_id: int,
        session: AsyncSession = Depends(get_db),
    #    current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")
    return region


@router.put("/regions/{region_id}", response_model=RegionOUT)
async def update_region(
        region_id: int,
        region_update: RegionUpdate,
        session: AsyncSession = Depends(get_db),
   #     current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

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


@router.delete("/regions/{region_id}", response_model=RegionOUT)
async def delete_region(
        region_id: int,
        session: AsyncSession = Depends(get_db),
   #     current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    # Получаем регион из базы данных
    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")

    # Устанавливаем is_active в False
    region.is_active = False

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем удаленный регион
    return region
