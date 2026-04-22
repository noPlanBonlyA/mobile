import os
from typing import Annotated, Literal, List

from fastapi import Depends
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode

__all__ = (
    'get_settings',
    'Settings',
    'settings',
)


class Db(BaseModel):
    """
    Настройки для подключения к базе данных.
    """

    host: str
    port: int
    user: str
    password: str
    name: str
    scheme: str = 'public'

    provider: str = 'postgresql+psycopg_async'

    @property
    def dsn(self) -> str:
        return f'{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'
    

class SMTP(BaseModel):
    """
    Настройки для подключения с email-сервисом
    """

    user: EmailStr
    password: str
    host: str
    port: int
    use_tls: bool
    use_ssl: bool



class JWT(BaseModel):
    """
    Настройки JWT токена.
    """

    token_algorithm: str


class Settings(BaseSettings):
    """
    Настройки модели.
    """

    debug: bool
    base_url: str
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    secret_key: str
    cors_origins: Annotated[List[str], NoDecode] 
    

    @field_validator('cors_origins', mode='before')
    @classmethod
    def decode_cors_origins(cls, v: str) -> List[str]:
        return v.split(',')

    db: Db

    jwt: JWT
    smtp: SMTP

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
        env_prefix='NOTIFICATION_EMAIL_APP_',
    )


def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

SettingsService = Annotated[Settings, Depends(get_settings)]