from pydantic_settings import BaseSettings
from pathlib import Path

# Ruta explícita al .env (seguro en Windows)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "technical_test"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    SECRET_KEY: str = "clave magica 123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

  
    INITIAL_USER_EMAIL: str = "admin@example.com"
    INITIAL_USER_PASSWORD: str = "admin123"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
