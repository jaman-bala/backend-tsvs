import logging

from logging import getLogger
from typing import Union, List, Dict
from uuid import UUID
from datetime import date, datetime
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.account.user.models import PortalRole
from backend.src.account.user.models import User

logger = getLogger(__name__)
logging.basicConfig(filename='log/user.log', level=logging.INFO)

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self,
            name: str,
            surname: str,
            middle_name: str,
            birth_year: date,

            email: str,
            inn: int,
            avatar: str,
            job_title: str,

            hashed_password: str,
            roles: List[PortalRole],

    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            middle_name=middle_name,
            birth_year=birth_year,

            email=email,
            inn=inn,
            avatar=avatar,
            job_title=job_title,

            hashed_password=hashed_password,
            roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        try:
            query = (
                delete(User)
                .where(User.user_id == user_id)
                .returning(User.user_id)
            )
            result = await self.db_session.execute(query)
            deleted_user_id_row = result.fetchone()
            if deleted_user_id_row:
                await self.db_session.commit()
                return deleted_user_id_row[0]
            else:
                await self.db_session.rollback()
                return None
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=500, detail=f"Database delete error: {str(e)}")

    async def disable_user(self, user_id: UUID) -> Union[UUID, None]:
        user = await self.db_session.get(User, user_id)
        if user:
            user.is_active = False
            await self.db_session.commit()
            return user_id
        return None

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, updated_user_data: Dict[str, any]) -> None:
        try:
            # Получение пользователя
          #  query = select(User).where(User.user_id == user_id, User.is_active == True) если нужно по is_active = True
            query = select(User).where(User.user_id == user_id, User.is_active == True)
            result = await self.db_session.execute(query)
            user = result.scalar_one_or_none()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            # Обновление данных пользователя
            for key, value in updated_user_data.items():
                setattr(user, key, value)
            user.updated_at = datetime.utcnow()  # Обновляем дату изменения

            # Сохранение изменений
            await self.db_session.commit()  # Коммит транзакции

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")

