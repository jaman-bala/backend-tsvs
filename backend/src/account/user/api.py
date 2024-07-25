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

from backend.src.account.auth.jwt import get_current_user_from_token
from backend.src.account.user.crud import _create_new_user
from backend.src.account.user.crud import _delete_user
from backend.src.account.user.crud import _get_user_by_id
from backend.src.account.user.crud import _update_user
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


@user_router.get("/user", response_model=List[ShowUser])
async def get_all_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> List[ShowUser]:
    all_users = await _get_all_users(db)
    if not all_users:
        raise HTTPException(
            status_code=404, detail=f"Колдонучулар жок."
        )
    return all_users


@user_router.get("/user/{user_id}", response_model=ShowUser)
async def get_user_by_id(
        user_id: UUID, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@user_router.post("/user", response_model=ShowUser)
async def create_user(
        body: UserCreate,
        db: AsyncSession = Depends(get_db),

) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"EMAIL уже существует!")


@user_router.put("/user/{user_id}", response_model=ShowUser)
async def update_user(
        user_id: UUID,
        body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> ShowUser:
    user_to_update = await _get_user_by_id(user_id, db)
    if user_to_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(
            target_user=user_to_update,
            current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")

    try:
        # Собираем параметры для обновления
        updated_user_params = body.dict(exclude_unset=True)
        updated_user_id = await _update_user(updated_user_params, user_id, db)
        if updated_user_id is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")

        # Получаем обновленного пользователя для ответа
        updated_user = await _get_user_by_id(user_id, db)
        return ShowUser(**updated_user.__dict__)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(
            target_user=user_for_deletion,
            current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.patch("/admin_privilege, response_model=UpdatedUserResponse")
async def grand_admin_privilege(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manager privileges of itself"
        )
    user_for_promotion = await _get_user_by_id(user_id, db)
    if user_for_promotion.is_admin or user_for_promotion.is_superadmin:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} already promoted to admin / superadmin.",
        )
    if user_for_promotion is None:
        raise HTTPException(
            status_code=404,
            detail="User with id {user_id} not found.",
        )
    updated_user_params = {
        "roles": list(user_for_promotion.enrich_admin_roles_by_admin_role())
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete("/admin_privilege", response_model=UpdatedUserResponse)
async def revoke_admin_privilege(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_revoke_admin_privileges = await _get_user_by_id(user_id, db)
    if not user_for_revoke_admin_privileges.is_admin:
        raise HTTPException(
            status_code=409, detail=f"User with id {user_id} has no admin privileges."
        )
    if user_for_revoke_admin_privileges is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_revoke_admin_privileges.remove_admin_privileges_from_model()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.patch("/user", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    if user_id != current_user.user_id:
        if not check_user_permissions(
            target_user=user_for_update,
            current_user=current_user,
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        updated_user_id = await _update_user(
            user_id=user_id,
            updated_user_params=updated_user_params,
            session=db
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {err}",
        )
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.post("/reset-password/{user_id}", response_model=UpdatedUserResponse)
async def reset_password(
    user_id: UUID,
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    user_dal = UserDAL(db)
    if not (current_user.is_admin or current_user.is_superadmin):
        raise HTTPException(status_code=403, detail="Forbidden. Only admins can reset passwords.")
    try:
        updated_user_id = await user_dal.reset_password(user_id, request.new_password)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
