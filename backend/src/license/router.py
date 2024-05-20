import shutil
import os
import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File as UploadFileType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db.session import get_db
# from backend.src.account.auth.auth import get_current_user_from_token
# from backend.src.account.user.models import User
from backend.src.license.models import Region, Item, QuantitySchool, FileModel
from backend.src.license.schemas import RegionOUT, RegionCreate, ItemSchemasOUT, ItemCreate, QuantitySchoolOUT, \
    QuantitySchoolCreate, FileOUT

router = APIRouter()


logger = logging.getLogger(__name__)
logging.basicConfig(filename='log/license.log', level=logging.INFO)


@router.post("/upload")
async def upload_files(files: List[UploadFile] = UploadFileType(...)):
    # Убедитесь, что папка media/file существует
    os.makedirs("media/file", exist_ok=True)

    for file in files:
        file_path = os.path.join("media/file", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"file_name": "200 ok"}


@router.post("/upload/{item_id}", response_model=List[FileOUT])
async def upload_files_for_item(
        item_id: int,
        files: List[UploadFile] = UploadFileType(...),
        session: AsyncSession = Depends(get_db),
):
    logger.info("Получен запрос на загрузку файлов для элемента с ID %s", item_id)

    # Проверяем, что указанный элемент существует
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Убедитесь, что папка media/file существует
    os.makedirs("media/file", exist_ok=True)

    file_models = []
    for file in files:
        file_path = os.path.join("media/file", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Создаем запись о файле в базе данных
        new_file = FileModel(filename=file.filename, filepath=file_path, item_id=item_id)
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file)
        file_models.append(new_file)

    logger.info("Файлы для элемента с ID %s успешно загружены", item_id)
    return file_models

#######################
# REGION ROUTER
#######################


@router.post("/regions/", response_model=RegionOUT)
async def create_region(
        region: RegionCreate,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового региона: %s", region.name)

    db_region = Region(**region.dict())
    session.add(db_region)
    await session.commit()
    await session.refresh(db_region)
    logger.info("Новый регион успешно создан: %s", db_region.name)
    return db_region


@router.get("/regions/", response_model=List[RegionOUT])
async def read_regions(
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    result = await session.execute(select(Region))
    regions = result.scalars().all()
    return regions


@router.get("/regions/{region_id}", response_model=RegionOUT)
async def read_region(
        region_id: int,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    region = await session.get(Region, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


@router.put("/regions/{region_id}", response_model=RegionOUT)
async def update_region(
        region_id: int,
        region_update: RegionCreate,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

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
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

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
# QuantitySchool ROUTER
#######################

@router.post("/quantitys/", response_model=QuantitySchoolOUT)
async def create_quantity(
        quantity: QuantitySchoolCreate,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    db_quantity = QuantitySchool(**quantity.dict())
    session.add(db_quantity)
    await session.commit()
    await session.refresh(db_quantity)
    return db_quantity


@router.get("/quantitys/", response_model=list[QuantitySchoolOUT])
async def read_quantity(
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    result = await session.execute(select(QuantitySchool))
    quantity = result.scalars().all()
    return quantity


@router.get("/quantitys/{quantity_id}", response_model=QuantitySchoolOUT)
async def read_quantity_id(
        quantity_id: int,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    quantity = await session.get(QuantitySchool, quantity_id)
    if quantity is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return quantity


@router.put("/quantitys/{quantity_id}", response_model=QuantitySchoolOUT)
async def update_quantity(
        quantity_id: int,
        quantity_update: QuantitySchoolCreate,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    # Получаем регион из базы данных
    quantity = await session.get(QuantitySchool, quantity_id)
    if quantity is None:
        raise HTTPException(status_code=404, detail="Region not found")

    # Обновляем поля региона
    quantity.name = quantity_update.name

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем обновленный регион
    return quantity


@router.delete("/quantitys/{quantity_id}", response_model=QuantitySchoolOUT)
async def delete_quantity(
        quantity_id: int,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    # Получаем регион из базы данных
    quantity = await session.get(QuantitySchool, quantity_id)
    if quantity is None:
        raise HTTPException(status_code=404, detail="Region not found")

    # Устанавливаем is_active в False
    quantity.is_active = False

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем удаленный регион
    return quantity


#######################
# LICENSE ROUTER
#######################

@router.post("/license/", response_model=ItemCreate)
async def create_item(
        item: ItemCreate,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")
    # Проверяем, что указанный region_id существует
    region = await session.get(Region, item.region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")

    # Проверяем, что указанный quantity_id существует
    quantity = await session.get(QuantitySchool, item.quantity_id)
    if quantity is None:
        raise HTTPException(status_code=404, detail="Quantity not found")

    # Создаем экземпляр элемента (Item)
    db_item = Item(
        number_register=item.number_register,
        name_entity=item.name_entity,
        tax_name=item.tax_name,
        entity_address=item.entity_address,
        address_program=item.address_program,
        cipher=item.cipher,
        title_school=item.title_school,
        quantity_school=item.quantity_school,
        forms_education=item.forms_education,
        full_name=item.full_name,
        contract_number=item.contract_number,
        issuing_license=item.issuing_license,
        data_license=item.data_license,
        form_number=item.form_number,
        form_number_suspended=item.form_number_suspended,
        form_number_start=item.form_number_start,
        form_number_stop=item.form_number_stop,
        data_address=item.data_address,
        form_number_data=item.form_number_data,

        region_id=item.region_id,
        quantity_id=item.quantity_id,
    )

    # Добавляем элемент в сессию и фиксируем изменения
    session.add(db_item)
    await session.commit()

    # Обновляем элемент в сессии для получения его идентификатора
    await session.refresh(db_item)

    # Возвращаем созданный элемент
    return db_item


@router.get("/license/", response_model=list[ItemSchemasOUT])
async def read_item(
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    result = await session.execute(select(Item))
    items = result.scalars().all()

    # Создаем список ItemOUT для возвращения
    items_out = []
    for item in items:
        # Получаем информацию о файлах для текущего элемента
        files_result = await session.execute(select(FileModel).filter(FileModel.item_id == item.id))
        files = files_result.scalars().all()

        # Создаем список файлов для текущего элемента
        files_out = [FileOUT(id=file.id, filename=file.filename, filepath=file.filepath) for file in files]

        # Добавляем элемент в список для возвращения
        items_out.append(
            ItemSchemasOUT(
                id=item.id,
                number_register=item.number_register,
                name_entity=item.name_entity,
                tax_name=item.tax_name,
                entity_address=item.entity_address,
                address_program=item.address_program,
                cipher=item.cipher,
                title_school=item.title_school,
                quantity_school=item.quantity_school,
                forms_education=item.forms_education,
                full_name=item.full_name,
                contract_number=item.contract_number,
                issuing_license=item.issuing_license,
                data_license=item.data_license,
                form_number=item.form_number,
                form_number_suspended=item.form_number_suspended,
                form_number_start=item.form_number_start,
                form_number_stop=item.form_number_stop,
                data_address=item.data_address,
                form_number_data=item.form_number_data,
                region_id=item.region_id,
                quantity_id=item.quantity_id,
                is_active=item.is_active,
                files=files_out,  # Прикрепляем информацию о файлах к текущему элементу
            )
        )

    return items_out


@router.get("/license/{license_id}", response_model=ItemSchemasOUT)
async def read_item_pk(
        item_id: int,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Проверяем, активен ли элемент
    if not item.is_active:
        raise HTTPException(status_code=404, detail="Item is not active")

    # Создаем объект ItemOUT для возвращения
    item_out = ItemOUT(
        id=item.id,
        number_register=item.number_register,
        name_entity=item.name_entity,
        tax_name=item.tax_name,
        entity_address=item.entity_address,
        address_program=item.address_program,
        cipher=item.cipher,
        title_school=item.title_school,
        quantity_school=item.quantity_school,
        forms_education=item.forms_education,
        full_name=item.full_name,
        contract_number=item.contract_number,
        issuing_license=item.issuing_license,
        data_license=item.data_license,
        form_number=item.form_number,
        form_number_suspended=item.form_number_suspended,
        form_number_start=item.form_number_start,
        form_number_stop=item.form_number_stop,
        data_address=item.data_address,
        form_number_data=item.form_number_data,
        region_id=item.region_id,
        quantity_id=item.quantity_id,
        is_active=item.is_active
    )

    return item_out


@router.put("/license/{license_id}", response_model=ItemSchemasOUT)
async def update_item(
        item_id: int,
        item_update: ItemCreate,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

    # Получаем элемент из базы данных
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Обновляем поля элемента
    item.number_register = item_update.number_register
    item.name_entity = item_update.name_entity
    item.tax_name = item_update.tax_name
    item.entity_address = item_update.entity_address
    item.address_program = item_update.address_program
    item.cipher = item_update.cipher
    item.title_school = item_update.title_school
    item.quantity_school = item_update.quantity_school
    item.forms_education = item_update.forms_education
    item.full_name = item_update.full_name
    item.contract_number = item_update.contract_number
    item.issuing_license = item_update.issuing_license
    item.data_license = item_update.data_license
    item.form_number = item_update.form_number
    item.form_number_suspended = item_update.form_number_suspended
    item.form_number_start = item_update.form_number_start
    item.form_number_stop = item_update.form_number_stop
    item.data_address = item_update.data_address
    item.form_number_data = item_update.form_number_data

    item.region_id = item_update.region_id
    item.quantity_id = item_update.quantity_id
    item.is_active = item_update.is_active

    # Фиксируем изменения в сессии
    await session.commit()

    # Возвращаем обновленный элемент
    return item


@router.delete("/license/{license_id}", response_model=ItemSchemasOUT)
async def delete_item(
        item_id: int,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на создание нового элемента")

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
