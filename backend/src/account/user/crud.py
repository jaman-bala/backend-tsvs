from datetime import datetime
from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Union, List, Dict
from uuid import UUID

from backend.src.account.user.schemas import ShowUser
from backend.src.account.user.schemas import UserCreate
from backend.src.account.user.dals import UserDAL, logger
from backend.src.account.user.models import PortalRole
from backend.src.account.user.models import User
from backend.src.account.auth.hashing import Hasher


async def _get_all_users(session: AsyncSession) -> List[ShowUser]:
    qs = await session.execute(select(User))
    users = qs.scalars().all()
    return users


async def _get_as_active(session: AsyncSession) -> List[ShowUser]:
    query = select(User).where(User.is_active == True)
    res = await session.execute(query)
    return res.scalars().all()


async def _create_new_user(body: UserCreate, session: AsyncSession) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            middle_name=body.middle_name,
            birth_year=body.birth_year,

            email=body.email,
            inn=body.inn,
            avatar=body.avatar,
            job_title=body.job_title,

            hashed_password=Hasher.get_password_hash(body.password),
            roles=body.roles,
            # roles=[
            #     PortalRole.ROLE_PORTAL_USER,
            # ],

        )
        return ShowUser(
            user_id=user.user_id,

            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            birth_year=user.birth_year,

            email=user.email,
            inn=user.inn,
            avatar=user.avatar,
            job_title=user.job_title,

            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=user.roles,
        )


async def _delete_user(user_id: UUID, session: AsyncSession) -> Union[UUID, None]:
    user_dal = UserDAL(session)
    return await user_dal.delete_user(user_id=user_id)


async def _disabled(user_id, session) -> Union[UUID, None]:
    user_dal = UserDAL(session)
    disabled_user_id = await user_dal.disable_user(user_id=user_id)
    return disabled_user_id


async def _update_user(user_id: UUID, updated_user_data: Dict[str, any], session: AsyncSession) -> None:
    try:
        # Открываем сессию и получаем пользователя
        user = await session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Обновление данных пользователя
        for key, value in updated_user_data.items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()  # Обновляем дату изменения

        # Сохранение изменений
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")


async def _get_user_by_id(user_id: UUID, db: AsyncSession) -> Union[User, None]:
    async with db.begin():  # Начало транзакции
        query = select(User).where(User.user_id == user_id, User.is_active == True)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user


async def _save_file_to_static(file: UploadFile) -> str:
    try:
        file_location = f"static/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())
        return file_location
    except Exception as e:
        logger.error(f"Ошибка сохранения файла: {e}")
        raise HTTPException(status_code=500, detail="Не удалось сохранить файл")


def check_user_permissions(target_user: User, current_user: User) -> bool:
    if PortalRole.ROLE_PORTAL_SUPERADMIN in current_user.roles:
        return True  # Администратор с ролью "ROLE_PORTAL_SUPERADMIN" имеет права на удаление любых пользователей
    if PortalRole.ROLE_PORTAL_SUPERADMIN in target_user.roles:
        return False  # Пользователя с ролью "ROLE_PORTAL_SUPERADMIN" нельзя удалять
    if target_user.user_id != current_user.user_id:
        # Проверка роли текущего пользователя
        if not {
            PortalRole.ROLE_PORTAL_ADMIN,
            PortalRole.ROLE_PORTAL_SUPERADMIN,
        }.intersection(current_user.roles):
            return False
        # Проверка попытки администратора удалить пользователя с ролью "ROLE_PORTAL_SUPERADMIN"
        if PortalRole.ROLE_PORTAL_SUPERADMIN in target_user.roles:
            return False
        # Проверка попытки администратора удалить другого администратора
        if (
                PortalRole.ROLE_PORTAL_ADMIN in target_user.roles
                and PortalRole.ROLE_PORTAL_ADMIN in current_user.roles
        ):
            return False
    return True

