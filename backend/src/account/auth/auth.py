import logging
from typing import Union, List
from jose import jwt
from jose import JWTError
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import status

from backend.config import settings

from backend.src.account.user.dals import UserDAL
from backend.src.account.user.models import User
from backend.db.session import get_db
from backend.src.account.auth.hashing import Hasher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

logger = logging.getLogger(__name__)


async def _get_user_by_email_for_auth(email: str, db: AsyncSession):
    user_dal = UserDAL(db)
    return await user_dal.get_user_by_email(email=email)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def authenticate_user_by_token(token: str, db: AsyncSession) -> Union[User, None]:
    payload = decode_token(token)
    email: str = payload.get("sub")
    if email is None:
        return None

    # Получение пользователя по email
    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        return None

    return user


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        raise credentials_exception

    user.roles = roles
    return user
