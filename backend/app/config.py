from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):

    environment: str

    database_host: str
    database_name: str
    database_username: str
    database_password: str
    database_port: str

    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
