import logging

from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.account.auth.hashing import Hasher
from backend.src.account.auth.jwt import get_current_user_from_token
from backend.src.account.user.crud import _create_new_user
from backend.src.account.user.crud import _delete_user
from backend.src.account.user.crud import _disabled
from backend.src.account.user.crud import _get_user_by_id
from backend.src.account.user.crud import _get_as_active
from backend.src.account.user.crud import _get_all_users
from backend.src.account.user.crud import check_user_permissions
from backend.src.account.user.schemas import DeleteUserResponse, ResetPasswordRequest
from backend.src.account.user.schemas import ShowUser
from backend.src.account.user.schemas import UpdateUserRequest
from backend.src.account.user.schemas import UpdatedUserResponse
from backend.src.account.user.schemas import UserCreate
from backend.src.account.user.dals import User, UserDAL
from backend.db.session import get_db

logger = getLogger(__name__)
logging.basicConfig(filename='log/user.log', level=logging.INFO)

user_router = APIRouter()


@user_router.post("/create", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        db: AsyncSession = Depends(get_db),

) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"EMAIL уже существует!")


@user_router.get("/all/", response_model=List[ShowUser])
async def get_all(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> List[ShowUser]:
    all_users = await _get_all_users(db)
    if not all_users:
        raise HTTPException(
            status_code=404, detail=f"Колдонуучулар жок."
        )
    return all_users


@user_router.get("/is_active/", response_model=List[ShowUser])
async def get_is_active(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> List[ShowUser]:
    is_active_users = await _get_as_active(db)
    if not is_active_users:
        raise HTTPException(
            status_code=404, detail=f"Колдонучулар жок."
        )
    return is_active_users


@user_router.get("/{user_id}", response_model=ShowUser)
async def get_user_by_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@user_router.put("/update/{user_id}", response_model=ShowUser)
async def update_user(
    user_id: UUID,
    user_update: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    user_dal = UserDAL(db)  # Создание экземпляра UserDAL

    # Получите пользователя по user_id
    target_user = await user_dal.get_user_by_id(user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверьте разрешения
    if not check_user_permissions(target_user, current_user):
        raise HTTPException(status_code=403, detail="У Вас нет прав для изминения.")

    try:
        # Обновите пользователя
        await user_dal.update_user(user_id, user_update.dict())
        # Верните обновленные данные
        return await user_dal.get_user_by_id(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.delete("/delete/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
) -> DeleteUserResponse:
    user_dal = UserDAL(db)
    target_user = await user_dal.get_user_by_id(user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="Не найден пользователь")

    if not check_user_permissions(target_user, current_user):
        raise HTTPException(status_code=403, detail="У Вас нет прав для удаления.")

    try:
        deleted_user_id = await _delete_user(user_id, db)
        if deleted_user_id:
            return DeleteUserResponse(deleted_user_id=deleted_user_id)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.delete("/disabled/{user_id}", response_model=DeleteUserResponse)
async def disabled_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token))\
        -> DeleteUserResponse:
    if "ROLE_PORTAL_USER" in current_user.roles:
        raise HTTPException(status_code=403, detail="Вы не можете отключить пользователя, обратитесь к администратору.")

    try:
        disabled_user_id = await _disabled(user_id, db)
        return DeleteUserResponse(deleted_user_id=disabled_user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.post("/reset-password", response_model=UpdatedUserResponse)
async def reset_password(
        user_id: UUID,
        data: ResetPasswordRequest,
        current_user: User = Depends(get_current_user_from_token),
        db: AsyncSession = Depends(get_db)
):
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    # Получение пользователя по user_id
    user_dal = UserDAL(db)
    user_to_update = await user_dal.get_user_by_id(user_id)

    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Проверка прав текущего пользователя
    if not check_user_permissions(user_to_update, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to reset password for this user")

    # Хэширование нового пароля и обновление пользователя
    user_to_update.hashed_password = Hasher.get_password_hash(data.new_password)
    await db.commit()

    return UpdatedUserResponse(updated_user_id=user_id, message="Пароль изменен")
