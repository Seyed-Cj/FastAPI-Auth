from pydantic import BaseSettings
from typing import Any

class Settings(BaseSettings):
    SECRET_KEY: str
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "fastapi_auth"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def SQL_DATABSE_URI(self) -> str:
        user = self.MYSQL_USER
        pw = self.MYSQL_PASSWORD
        host = self.MYSQL_HOST
        port = self.MYSQL_PORT
        db = self.MYSQL_DB
        return f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()