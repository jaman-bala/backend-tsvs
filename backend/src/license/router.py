import shutil
import os
import logging
import uuid
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File as UploadFileType, Form
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

@router.post("/license", response_model=ItemCreate)
async def create_item(
    number_register: str = Form(...),
    name_entity: str = Form(...),
    tax_name: str = Form(...),
    entity_address: str = Form(...),
    address_program: str = Form(...),
    cipher: str = Form(...),
    title_school: str = Form(...),
    quantity_school: str = Form(...),
    forms_education: str = Form(...),
    full_name: str = Form(...),
    contract_number: str = Form(...),
    issuing_license: str = Form(...),
    data_license: str = Form(...),
    form_number: str = Form(...),
    form_number_suspended: str = Form(...),
    form_number_start: str = Form(...),
    form_number_stop: str = Form(...),
    data_address: str = Form(...),
    form_number_data: str = Form(...),
    issuing_authority: str = Form(...),
    region_id: int = Form(...),
    quantity_id: int = Form(...),
    # files: List[UploadFile] = UploadFileType(...),
    session: AsyncSession = Depends(get_db),
):
    logger.info("Получен запрос на создание нового элемента")

    # Проверяем, что указанный region_id существует
    result = await session.execute(select(Region).filter_by(id=region_id))
    region = result.scalar_one_or_none()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")

    # Проверяем, что указанный quantity_id существует
    result = await session.execute(select(QuantitySchool).filter_by(id=quantity_id))
    quantity = result.scalar_one_or_none()
    if quantity is None:
        raise HTTPException(status_code=404, detail="Quantity not found")

    # Создаем экземпляр элемента (Item)
    db_item = Item(
        number_register=number_register,
        name_entity=name_entity,
        tax_name=tax_name,
        entity_address=entity_address,
        address_program=address_program,
        cipher=cipher,
        title_school=title_school,
        quantity_school=quantity_school,
        forms_education=forms_education,
        full_name=full_name,
        contract_number=contract_number,
        issuing_license=issuing_license,
        data_license=data_license,
        form_number=form_number,
        form_number_suspended=form_number_suspended,
        form_number_start=form_number_start,
        form_number_stop=form_number_stop,
        data_address=data_address,
        form_number_data=form_number_data,
        issuing_authority=issuing_authority,
        region_id=region_id,
        quantity_id=quantity_id,
    )

    # Обработка файлов
    # os.makedirs("media/file", exist_ok=True)
    # file_models = []
    # if files:
    #     for file in files:
    #         unique_suffix = str(uuid.uuid4())
    #         unique_filename = f"{unique_suffix}_{file.filename}"
    #         file_path = os.path.join("media/file", unique_filename)
    #         with open(file_path, "wb") as buffer:
    #             shutil.copyfileobj(file.file, buffer)
    #
    #         # Создаем запись о файле в базе данных
    #         new_file = FileModel(filename=unique_filename, filepath=file_path, item_id=db_item.id)
    #         session.add(new_file)
    #         await session.commit()
    #         await session.refresh(new_file)
    #         file_models.append(new_file)
    #
    # # Обновляем db_item с файлами
    # db_item.files = file_models
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)

    # Возвращаем созданный элемент с файлами
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
                issuing_authority=item.issuing_authority,
                region_id=item.region_id,
                quantity_id=item.quantity_id,
                is_active=item.is_active,
                files=files_out,  # Прикрепляем информацию о файлах к текущему элементу
            )
        )

    return items_out


@router.get("/license/{item_id}", response_model=ItemSchemasOUT)
async def read_item_pk(
        item_id: int,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на чтение элемента по ID")

    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Проверяем, активен ли элемент
    if not item.is_active:
        raise HTTPException(status_code=404, detail="Item is not active")

    # Получаем связанные файлы
    result = await session.execute(select(FileModel).filter_by(item_id=item.id))
    files = result.scalars().all()

    # Преобразуем файлы в формат для вывода
    file_out_list = [
        FileOUT(
            id=file.id,
            filename=file.filename,
            filepath=file.filepath,
            item_id=file.item_id
        )
        for file in files
    ]

    # Создаем объект ItemOUT для возвращения
    item_out = ItemSchemasOUT(
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
        issuing_authority=item.issuing_authority,
        region_id=item.region_id,
        quantity_id=item.quantity_id,
        files=file_out_list,  # Добавлено
        is_active=item.is_active
    )

    return item_out


@router.put("/license/{item_id}", response_model=ItemSchemasOUT)
async def update_item(
        item_id: int,
        item_update: ItemCreate,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на обновление элемента")

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
    item.issuing_authority = item_update.issuing_authority
    item.region_id = item_update.region_id
    item.quantity_id = item_update.quantity_id

    # Фиксируем изменения в сессии
    await session.commit()

    # Получаем связанные файлы
    result = await session.execute(select(FileModel).filter_by(item_id=item.id))
    files = result.scalars().all()

    # Преобразуем файлы в формат для вывода
    file_out_list = [
        FileOUT(
            id=file.id,
            filename=file.filename,
            filepath=file.filepath,
            item_id=file.item_id
        )
        for file in files
    ]

    # Возвращаем обновленный элемент
    item_out = ItemSchemasOUT(
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
        issuing_authority=item.issuing_authority,
        region_id=item.region_id,
        quantity_id=item.quantity_id,
        files=file_out_list,
        is_active=item.is_active
    )

    return item_out


@router.delete("/license/{item_id}", response_model=ItemSchemasOUT)
async def delete_item(
        item_id: int,
        session: AsyncSession = Depends(get_db),
        # current_user: User = Depends(get_current_user_from_token),
):
    logger.info("Получен запрос на удаление элемента")

    # Получаем элемент из базы данных
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Устанавливаем флаг is_active в False
    item.is_active = False

    # Фиксируем изменения в сессии
    await session.commit()

    # Получаем связанные файлы
    result = await session.execute(select(FileModel).filter_by(item_id=item.id))
    files = result.scalars().all()

    # Преобразуем файлы в формат для вывода
    file_out_list = [
        FileOUT(
            id=file.id,
            filename=file.filename,
            filepath=file.filepath,
            item_id=file.item_id
        )
        for file in files
    ]

    # Создаем объект ItemSchemasOUT для возвращения
    item_out = ItemSchemasOUT(
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
        issuing_authority=item.issuing_authority,
        region_id=item.region_id,
        quantity_id=item.quantity_id,
        files=file_out_list,  # Добавлено
        is_active=item.is_active
    )

    return item_out
