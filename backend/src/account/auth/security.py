from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from jose.exceptions import JWTError

from backend.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT-токен на основе предоставленных данных.

    :param data: Словарь данных, которые будут включены в токен.
    :param expires_delta: Дополнительный срок действия токена (если не указан, используется значение из настроек).
    :return: Строка с JWT-токеном.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        # Обработка ошибок кодирования токена
        raise JWTError("Failed to encode JWT token") from e