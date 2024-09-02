import os
from deepface import DeepFace
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_face_similar(uploaded_img_path: str, user_images_folder: str, model_name: str = "Facenet") -> bool:
    """
    Проверяет схожесть лиц на загруженном изображении и всех изображениях из папки пользователя.
    """
    try:
        for file_name in os.listdir(user_images_folder):
            user_img_path = os.path.join(user_images_folder, file_name)
            try:
                result = DeepFace.verify(uploaded_img_path, user_img_path, model_name=model_name)
                if result['verified']:
                    return True
            except Exception as e:
                logger.error(f"Error comparing faces: {e}")
        return False
    except Exception as e:
        logger.error(f"Error reading user images folder: {e}")
        return False
