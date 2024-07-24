from typing import Union, List
from uuid import UUID
from datetime import date, datetime

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.account.auth.hashing import Hasher
from backend.src.account.user.models import PortalRole
from backend.src.account.user.models import User


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
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

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

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def reset_password(self, user_id: UUID, new_password: str) -> Union[UUID, None]:
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(hashed_password=Hasher.get_password_hash(new_password))
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        updated_user_id_row = res.fetchone()
        if updated_user_id_row is not None:
            return updated_user_id_row[0]
