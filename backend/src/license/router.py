from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db.session import get_db
from backend.src.account.auth.auth import get_current_user_from_token
from backend.src.account.user.models import User
from backend.src.license.models import Region, Item
from backend.src.license.schemas import RegionOUT, RegionCreate, ItemOUT, ItemCreate

router = APIRouter()

#######################
# REGION ROUTER
#######################


@router.post("/regions/", response_model=RegionOUT)
async def create_region(
        region: RegionCreate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    db_region = Region(**region.dict())
    session.add(db_region)
    await session.commit()
    await session.refresh(db_region)
    return db_region


@router.get("/regions/", response_model=list[RegionOUT])
async def read_regions(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    result = await session.execute(select(Region))
    regions = result.scalars().all()
    return regions


@router.get("/regions/{region_id}", response_model=RegionOUT)
async def read_region(region_id: int, session: AsyncSession = Depends(get_db)):
    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


@router.put("/regions/{region_id}", response_model=RegionOUT)
async def update_region(region_id: int, region_update: RegionCreate, session: AsyncSession = Depends(get_db)):
    # Получаем регион из базы данных
    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")

    # Обновляем поля региона
    region.name = region_update.name

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем обновленный регион
    return region


@router.delete("/regions/{region_id}", response_model=RegionOUT)
async def delete_region(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    # Получаем регион из базы данных
    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")

    # Устанавливаем is_active в False
    region.is_active = False

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем удаленный регион
    return region

#######################
# LICENSE ROUTER
#######################


@router.post("/license/", response_model=ItemOUT)
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_db)):
    # Проверяем, что указанный region_id существует
    region = await session.get(Region, item.region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")

    # Создаем экземпляр элемента (Item)
    db_item = Item(
        name=item.name,
        full_name=item.full_name,
        contract_number=item.contract_number,
        region_id=item.region_id
    )

    # Добавляем элемент в сессию и фиксируем изменения
    session.add(db_item)
    await session.commit()

    # Обновляем элемент в сессии для получения его идентификатора
    await session.refresh(db_item)

    # Возвращаем созданный элемент
    return db_item


@router.get("/license/", response_model=list[ItemOUT])
async def read_item(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Item))
    items = result.scalars().all()

    # Создаем список ItemOUT для возвращения
    items_out = []
    for item in items:
        # Проверяем, что значение region_id не является None
        if item.region_id is not None:
            items_out.append(
                ItemOUT(
                    id=item.id,
                    name=item.name,
                    full_name=item.full_name,
                    contract_number=item.contract_number,
                    region_id=item.region_id,
                    is_active=item.is_active
                )
            )
    return items_out


@router.get("/license/{license_id}", response_model=ItemOUT)
async def read_item(item_id: int, session: AsyncSession = Depends(get_db)):
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Создаем объект ItemOUT для возвращения
    item_out = ItemOUT(
        id=item.id,
        name=item.name,
        full_name=item.full_name,
        contract_number=item.contract_number,
        region_id=item.region_id,
        is_active=item.is_active
    )
    return item_out


@router.put("/license/{license_id}", response_model=ItemOUT)
async def update_item(item_id: int, item_update: ItemCreate, session: AsyncSession = Depends(get_db)):
    # Получаем элемент из базы данных
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Обновляем поля элемента
    item.name = item_update.name
    item.full_name = item_update.full_name
    item.contract_number = item_update.contract_number
    item.region_id = item_update.region_id
    item.is_active = item_update.is_active

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем обновленный элемент
    return item


@router.delete("/license/{license_id}", response_model=ItemOUT)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_db)):
    # Получаем элемент из базы данных
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Устанавливаем флаг is_active в False
    item.is_active = False

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем обновленный элемент
    return item
