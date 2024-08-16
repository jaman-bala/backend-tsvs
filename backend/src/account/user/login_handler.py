from datetime import timedelta
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.src.account.auth.jwt import authenticate_user
from backend.src.account.auth.schemas import Token
from backend.src.account.user.models import User
from backend.db.session import get_db
from backend.src.account.auth.security import create_access_token
from backend.src.account.auth.jwt import get_current_user_from_token

login_router = APIRouter()


@login_router.get("/protected-resource")
async def protected_resource(current_user: User = Depends(get_current_user_from_token)):
    return {
        "message": "This is a protected resource",
        "user_email": current_user.email,
        "user_role": current_user.roles,
    }


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "roles": user.roles},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
