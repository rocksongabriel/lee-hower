from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):

    environment: str

    dev_database_host: str
    dev_database_name: str
    dev_database_username: str
    dev_database_password: str
    dev_database_port: str

    test_database_name: str
    test_database_host: str
    test_database_username: str
    test_database_password: str
    test_database_port: str

    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
