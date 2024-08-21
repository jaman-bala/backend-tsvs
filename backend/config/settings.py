import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = "media/file"
STATIC_FILES_DIR = BASE_DIR / "static"


class Settings:
    PROJECT_NAME: str = "TSVS DATABASE 🔥"
    PROJECT_VERSION: str = "1.0.0"

    class Config:
        env_file = BASE_DIR / ".env"


set = Settings()

# class Settings(BaseSettings):
#     PROJECT_NAME: str = "TSVS DATABASE 🔥"
#     PROJECT_VERSION: str = "1.0.0"
#
#     class Config:
#         env_file = BASE_DIR / ".env"
#
#
# settings = Settings()


SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default=30))


SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")