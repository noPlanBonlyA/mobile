from fastapi import Request
from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field, HttpUrl
import re
from uuid import UUID
from datetime import datetime, date
from school_site.core.schemas import CreateBaseModel, UpdateBaseModel, TimestampMixin
from school_site.core.enums import UserRole
from .exceptions import InvalidTokenError


class UserIdSchema(BaseModel):
    user_id: UUID

    
class UsernameRelatedMixin(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError('Username должен содержать только цифры.')
        if len(v) < 3:
            raise ValueError('Username должен быть не менее 3 символов.')
        return v
    

class LoginRequestSchema(UsernameRelatedMixin):
    password: str


class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str

class PasswordSchema(BaseModel):
    password_hash: str

class PhoneValidatedMixin(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        pattern = r"^\+?[0-9]{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Неверный формат номера телефона. Пример: +79991234567")
        return v

    class Config:
        arbitrary_types_allowed = True


class UserInfoMixin(BaseModel):
    first_name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    email: EmailStr
    birth_date: date
    role: UserRole
    

class RegisterRequestSchema(PhoneValidatedMixin, UserInfoMixin):
    password: str


class UserCreateSchema(PhoneValidatedMixin, UserInfoMixin, UsernameRelatedMixin, CreateBaseModel):
    password_hash: str


class UserUpdateDBSchema(PhoneValidatedMixin, UserInfoMixin, UpdateBaseModel):
    password_hash: str


class UserUpdateSchema(PhoneValidatedMixin, UserInfoMixin, UpdateBaseModel):
    password: str


class UserReadSchema(PhoneValidatedMixin, UserInfoMixin, UsernameRelatedMixin):
    id: UUID


class UserReadDBSchema(PhoneValidatedMixin, UserInfoMixin, UsernameRelatedMixin, TimestampMixin):
    id: UUID
    password_hash: str

    class Config:
        from_attributes = True


class UserTokenDataReadSchema(BaseModel):
    user_id: UUID
    role: UserRole
    expiration: datetime


class TokenReadSchema(BaseModel):
    token: str
    expiration: datetime


class RefreshTokenReadDBSchema(BaseModel):
    id: UUID
    user_id: UUID
    hashed_refresh_token: str
    created_at: datetime


class RefreshTokenUpdateDBSchema(BaseModel):
    id: UUID
    user_id: UUID
    hashed_refresh_token: str


class RefreshTokenCreateDBSchema(CreateBaseModel):
    user_id: UUID
    hashed_refresh_token: str


class UserUpdateRequestSchema(PhoneValidatedMixin, UserInfoMixin, BaseModel):  
    ...

class UserUpdateNoPasswordSchema(PhoneValidatedMixin, UserInfoMixin, UpdateBaseModel):
   ...

class UserUpdateDBNoPasswordHashSchema(PhoneValidatedMixin, UserInfoMixin, UpdateBaseModel):
    ...

class UserResetSchema(UsernameRelatedMixin):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ResetTokenSchema(BaseModel):
    token: str
    hours: int

class ResetTokenBaseSchema(BaseModel):
    user_id: UUID
    token_hash: str
    expires_at: datetime

class ResetTokenCreateSchema(CreateBaseModel, ResetTokenBaseSchema):
    pass

class ResetTokenUpdateSchema(UpdateBaseModel, ResetTokenBaseSchema):
    pass

class ResetTokenReadSchema(ResetTokenBaseSchema):
    id: UUID

class CookieTokenSchema:
    def __init__(self, cookie_name: str, auto_error: bool = True):
        self.cookie_name = cookie_name
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        token = request.cookies.get(self.cookie_name)
        if not token and self.auto_error:
            raise InvalidTokenError()
        return token

T = TypeVar('T')

class PaginationResultSchema(BaseModel, Generic[T]):
    
    model_config = ConfigDict(from_attributes=True)
    count: int  
    objects: List[T]  

# --- Схемы для фото пользователя ---
class PhotoUserBaseSchema(BaseModel):
    name: str = Field(..., description="Название фотографии пользователя")
    user_id: Optional[UUID] = None

class PhotoUserCreateSchema(CreateBaseModel, PhotoUserBaseSchema):
    pass

class PhotoUserCreateDBSchema(CreateBaseModel, PhotoUserBaseSchema):
    user_id: UUID
    path: str

class PhotoUserUpdateSchema(PhotoUserBaseSchema):
    id: Optional[UUID] = None

class PhotoUserUpdateDBSchema(UpdateBaseModel, PhotoUserBaseSchema):
    user_id: UUID

class PhotoUserReadDBSchema(PhotoUserBaseSchema, TimestampMixin):
    id: UUID
    path: str
    class Config:
        from_attributes = True

class PhotoUserReadSchema(PhotoUserBaseSchema, TimestampMixin):
    id: UUID
    url: HttpUrl

# --- Схемы для пользователя с фото ---
class UserWithPhotoReadDBSchema(PhoneValidatedMixin, UserInfoMixin, UsernameRelatedMixin, TimestampMixin):
    id: UUID
    photo: Optional[PhotoUserReadDBSchema] = None

class UserWithPhotoReadSchema(PhoneValidatedMixin, UserInfoMixin, UsernameRelatedMixin, TimestampMixin):
    id: UUID
    photo: Optional[PhotoUserReadSchema] = None

class UserWithPhotoPaginationResultDBSchema(PaginationResultSchema[UserWithPhotoReadDBSchema]):
    pass

class UserWithPhotoPaginationResultSchema(PaginationResultSchema[UserWithPhotoReadSchema]):
    pass

# --- Схемы для создания и обновления пользователей с фото ---
class UserCreateWithPhotoSchema(PhoneValidatedMixin, UserInfoMixin):
    password: str
    photo: Optional[PhotoUserCreateSchema] = Field(None, description="Фотография пользователя (опционально)")

class UserUpdateWithPhotoSchema(PhoneValidatedMixin, UserInfoMixin):
    photo: Optional[PhotoUserUpdateSchema] = None

# --- Схемы для аутентификации (определены после UserWithPhotoReadSchema) ---
class AuthReadSchema(BaseModel):
    user: UserWithPhotoReadSchema
    access_token: TokenReadSchema
    refresh_token: TokenReadSchema