import logging

from logging import getLogger
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.account.auth.jwt import get_current_user_from_token
from backend.src.account.user.crud import _get_user_by_id
from backend.src.account.user.crud import _update_user
from backend.src.account.user.schemas import UpdatedUserResponse
from backend.src.account.user.dals import User
from backend.db.session import get_db

admin_router = APIRouter()

logger = getLogger(__name__)
logging.basicConfig(filename='log/admin.log', level=logging.INFO)


@admin_router.patch("/update", response_model=UpdatedUserResponse)
async def grand_admin_privilege(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Вы не супер администратор.")
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Нельзя управлять собственными привилегиями"
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
        return UpdatedUserResponse(updated_user_id=updated_user_id)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@admin_router.delete("/delete", response_model=UpdatedUserResponse)
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