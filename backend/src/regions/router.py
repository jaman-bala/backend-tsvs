import logging

from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.account.user.dals import User
from backend.src.account.auth.jwt import get_current_user_from_token
from backend.src.regions.crud import _create_region, _get_all_regions, _get_is_active, _get_region_by_id
from backend.src.regions.crud import _update_region, _delete_region, _disable_region
from backend.db.session import get_db
from backend.src.regions.schemas import RegionOUT, RegionCreate, RegionUpdate, Is_activeShemasOUT
from backend.src.regions.models import Region


router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log/regions.log', level=logging.INFO)

#######################
# REGION ROUTER
#######################


@router.post("/create/", response_model=RegionOUT)
async def create_region(
        body: RegionCreate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового региона: %s", body.title)
    new_region = await _create_region(body, session)
    return new_region


@router.get("/all/", response_model=List[RegionOUT])
async def read_regions(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на вывод всех пользователей")

    all_regions = await _get_all_regions(session)
    if not all_regions:
        raise HTTPException(status_code=404, detail="Регионов не найдено")
    return all_regions


@router.get("/is_active/", response_model=List[RegionOUT])
async def read_active_regions(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на вывод активных регионов")

    is_active_region = await _get_is_active(session)
    return is_active_region


@router.get("/id/{region_id}", response_model=RegionOUT)
async def get_regions_id(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос по id")

    region = await _get_region_by_id(region_id, session)
    return region


@router.put("/update/{region_id}", response_model=RegionOUT)
async def update_regions(
        region_id: int,
        region_update: RegionUpdate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на обновление региона")

    update_region = await _update_region(region_id, region_update, session)
    return update_region


@router.delete("/delete/{region_id}")
async def delete_region(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на удаление региона")

    await _delete_region(region_id, session)
    return {"message": f"Регион {region_id} удален"}


@router.delete("/disabled/{region_id}", response_model=Is_activeShemasOUT)
async def disable_regions(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на деактивацию региона")

    await _disable_region(region_id, session)
    update_region_disabled = await _get_region_by_id(region_id, session)

    if update_region_disabled is None:
        raise HTTPException(status_code=404, detail="Регион не найден")

    return update_region_disabled

