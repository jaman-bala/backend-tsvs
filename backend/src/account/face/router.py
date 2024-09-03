import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import timedelta

from backend.src.account.auth.security import create_access_token, create_refresh_token
from backend.src.account.face.utils import is_face_similar

router = APIRouter()


@router.post("/auth/face")
async def authenticate_face(image: UploadFile = File(...)):
    temp_dir = 'static/face-save/'
    os.makedirs(temp_dir, exist_ok=True)

    unique_filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(temp_dir, unique_filename)

    try:
        # Сохранение загруженного изображения во временную папку
        with open(file_path, "wb") as f:
            contents = await image.read()
            f.write(contents)

        # Проверка схожести лиц
        if is_face_similar(file_path, 'static/avatars/'):
            # Генерация токена, если лицо найдено
            token_data = {"sub": "user_id"}  # Замените на реальный идентификатор пользователя
            access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=480))
            refresh_token = create_refresh_token(data=token_data, expires_delta=timedelta(minutes=30))
            return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Face not recognized")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Такого пользователя нету: {e}")
    finally:
        os.remove(file_path)
