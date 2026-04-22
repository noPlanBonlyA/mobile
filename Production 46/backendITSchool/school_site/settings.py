import os
from typing import Annotated, Literal, List

from fastapi import Depends
from pydantic import BaseModel, field_validator, HttpUrl
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



class Minio(BaseModel):
    """
    Настройки Minio
    """

    endpoint: str
    access_key: str
    secret_key: str
    secure: bool = False
    url: HttpUrl
    


class Cache(BaseModel):
    """
    Настройки кеша.
    """

    prefix: str = 'boiler-plate'


class EmailService(BaseModel):
    url: HttpUrl
    token_algorithm: str
    token_lifetime_minutes: int
    secret_key: str


class ResetToken(BaseModel):
    token_lifetime_hours: int


class JWT(BaseModel):
    """
    Настройки JWT токена.
    """

    token_algorithm: str


class AccessToken(BaseModel):
    """
    Настройки Access JWT токена.
    """
    token_lifetime_minutes: int


class RefreshToken(BaseModel):
    """
    Настройки Refresh токена.
    """
    token_lifetime_days: int

class JWTCookie(BaseModel):
    """
    Настройки создания куки с JWT токеном.
    """

    token_lifetime: int
    cookie_name: str
    cookie_max_age: int
    cookie_path: str
    cookie_secure: bool
    cookie_samesite: Literal['lax', 'strict', 'none']


class Settings(BaseSettings):
    """
    Настройки модели.
    """

    debug: bool
    base_url: str
    frontend_url: str
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    secret_key: str
    cors_origins: Annotated[List[str], NoDecode] 
    
    email_service: EmailService

    reset_token: ResetToken

    @field_validator('cors_origins', mode='before')
    @classmethod
    def decode_cors_origins(cls, v: str) -> List[str]:
        return v.split(',')

    db: Db
    minio: Minio

    jwt: JWT
    access_token: AccessToken
    refresh_token: RefreshToken

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
        env_prefix='SCHOOL_SITE_APP_',
    )


def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

SettingsService = Annotated[Settings, Depends(get_settings)]