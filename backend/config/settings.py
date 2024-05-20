import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = "media/file"


class Settings:
    PROJECT_NAME: str = "TSVS DATABASE License 🔥"
    PROJECT_VERSION: str = "1.0.0"


set = Settings()


SECRET_KEY: str = os.getenv("SECRET_KEY", default="secret_key")
ALGORITHM: str = os.getenv("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app.db"