import logging
import hashlib
import secrets
from jose import jwt, JWTError
from typing import Protocol, Optional, Self, List
from uuid import UUID
from ..exceptions import TokenNotFoundError
from ..schemas import UserTokenDataReadSchema, ResetTokenSchema, ResetTokenCreateSchema
from .passwords import PasswordServiceProtocol
from ..repositories.reset_tokens import ResetTokenRepositoryProtocol
from datetime import datetime, timedelta, timezone, UTC
from school_site.core.enums import UserRole
from school_site.apps.users.schemas import (
    TokenReadSchema, RefreshTokenCreateDBSchema, RefreshTokenReadDBSchema,
    ResetTokenReadSchema
)
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.apps.users.exceptions import InvalidTokenError
from school_site.apps.users.repositories.refresh_tokens import RefreshTokenRepositoryProtocol
from school_site.settings import settings


logger = logging.getLogger(__name__)


class TokenServiceProtocol(Protocol):
    def create_access_token(self: Self, user_id: UUID, role: UserRole, expires_delta: Optional[timedelta] = None) -> TokenReadSchema:
        ...
    
    async def create_refresh_token(self: Self, user_id: UUID) -> TokenReadSchema:
        ...
    
    async def verify_refresh_token(self: Self, refresh_token: str) -> RefreshTokenReadDBSchema:
        ...
    
    async def delete(self: Self, id: UUID) -> bool:
        ...

    async def delete_all_by_user_id(self: Self, user_id: UUID) -> bool:
        ...

    async def get_admin_user(self: Self, access_token: str) -> UserTokenDataReadSchema:
        ...

    async def decode_access_token(self: Self, token: str) -> UserTokenDataReadSchema:
        ...

    async def generate_reset_token(self: Self) -> str:
        ...

class TokenService(TokenServiceProtocol):
    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepositoryProtocol,
    ):
        self.refresh_token_repository = refresh_token_repository
    

    async def delete(self: Self, id: UUID) -> bool:
        return await self.refresh_token_repository.delete(id)
    
    async def delete_all_by_user_id(self: Self, user_id: UUID) -> bool:
        return await self.refresh_token_repository.delete_all_by_user_id(user_id)

    def create_access_token(
        self: Self, 
        user_id: UUID, 
        role: UserRole, 
        expires_delta: Optional[timedelta] = None
    ) -> TokenReadSchema:
        logger.info(f"Creating access token for user: {user_id}")
        
        to_encode = {"user_id": str(user_id), "role": role}
        expiration = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token.token_lifetime_minutes))
        to_encode.update({"exp": expiration})
        
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt.token_algorithm)
        logger.info(f"Access token created for user: {user_id}")
        
        return TokenReadSchema(token=encoded_jwt,
                               expiration=expiration)
    
    async def create_refresh_token(self: Self, user_id: UUID) -> TokenReadSchema:
        logger.info(f"Creating refresh token for user: {user_id}")
        
        refresh_token = secrets.token_hex(32)

        expiration = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token.token_lifetime_days)
        
        hashed_refresh_token = hashlib.sha256(refresh_token.encode('utf-8')).hexdigest()
                
        token_count = await self.refresh_token_repository.count_by_user_id(user_id)
        logger.info(f"User {user_id} has {token_count} refresh tokens")
        
        if token_count >= 5:
            logger.info(f"User {user_id} has reached maximum refresh tokens, removing oldest")
            oldest_token = await self.refresh_token_repository.get_oldest_by_user_id(user_id)
            if oldest_token:
                await self.delete(oldest_token.id)
        
        await self.refresh_token_repository.create(RefreshTokenCreateDBSchema(
            user_id=user_id,
            hashed_refresh_token=hashed_refresh_token
        ))
        logger.info(f"Refresh token created for user: {user_id}")
        
        return TokenReadSchema(
            token=refresh_token,
            expiration=expiration
        )


    async def verify_refresh_token(self: Self, refresh_token: str) -> RefreshTokenReadDBSchema:
        logger.info("Verifying refresh token")
        
        computed_hash = hashlib.sha256(refresh_token.encode('utf-8')).hexdigest()
        
        db_refresh_token = await self.refresh_token_repository.get_by_hashed_token(computed_hash)
        
        if not db_refresh_token:
            logger.error("No matching refresh token found")
            raise InvalidTokenError()
        
        expiration = db_refresh_token.created_at + timedelta(days=settings.refresh_token.token_lifetime_days)
        
        if datetime.now(timezone.utc) > expiration:
            logger.warning(f"Refresh token expired for user: {db_refresh_token.user_id}")
            await self.delete(db_refresh_token.id)
            raise InvalidTokenError()

        return db_refresh_token
    

    async def decode_access_token(self: Self, token: str) -> UserTokenDataReadSchema:
        logger.info("Decoding access token")

        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt.token_algorithm])
            user_id_str = payload.get("user_id")
            role = payload.get("role")
            exp = payload.get("exp")

            if user_id_str is None:
                logger.error("Invalid token: missing user_id")
                raise PermissionDeniedError()

            try:
                user_id = UUID(user_id_str)
            except ValueError:
                logger.error("Invalid token: user_id not a valid UUID")
                raise PermissionDeniedError()

            if exp is None:
                logger.error("Invalid token: missing expiration time")
                raise PermissionDeniedError()

            try:
                role_enum = UserRole(role)
            except ValueError:
                logger.error(f"Invalid token: unknown role {role}")
                raise PermissionDeniedError()

            token_data = UserTokenDataReadSchema(
                user_id=user_id,
                role=role_enum,
                expiration=datetime.fromtimestamp(exp)
            )
            logger.info(f"Token decoded successfully for user: {user_id}")

            return token_data

        except JWTError:
            logger.warning("Failed to decode token", exc_info=True)
            raise PermissionDeniedError()

    async def get_admin_user(self: Self, access_token: str) -> UserTokenDataReadSchema:
        user_data = await self.decode_access_token(access_token)
        if user_data.role != UserRole.ADMIN and user_data.role != UserRole.SUPERADMIN:
            logger.error("User is not an admin")
            raise PermissionDeniedError()
        return user_data
    
class ResetPasswordTokenServiceProtocol(Protocol):
    async def generate_reset_token(self: Self, user_id: int) -> ResetTokenSchema:
        ...

    async def get_all(self: Self) -> List[ResetTokenReadSchema]:
        ...

    async def get_by_token(self: Self, token: str) -> ResetTokenReadSchema:
        ...

    async def delete(self: Self, id: UUID) -> bool:
        ...

    async def delete_all_expired_tokens(self: Self) -> bool:
        ...

class ResetPasswordTokenService(ResetPasswordTokenServiceProtocol):
    def __init__(self: Self, password_reset_repository: ResetTokenRepositoryProtocol,
                  password_service: PasswordServiceProtocol):
        self.password_reset_repository = password_reset_repository
        self.password_service = password_service
    
    async def generate_reset_token(self: Self, user_id: int) -> ResetTokenSchema:
        TIME = settings.reset_token.token_lifetime_hours
        token = secrets.token_urlsafe(32)
        hashed_token = self.password_service.get_password_hash(token)
        expires_at = datetime.now(UTC) + timedelta(hours=TIME)
        token_to_create = ResetTokenCreateSchema(
            user_id=user_id,
            token_hash=hashed_token,
            expires_at=expires_at
        )
        await self.password_reset_repository.create(token_to_create)
        reset_schema = ResetTokenSchema(
            token=token,
            hours=TIME
        )
        return reset_schema
    
    async def get_all(self: Self) -> List[ResetTokenReadSchema]:
        return await self.password_reset_repository.get_all()
    
    async def get_by_token(self: Self, token: str) -> ResetTokenReadSchema:
        db_tokens = await self.get_all()
        for db_token in db_tokens:
            if self.password_service.verify_password(token, db_token.token_hash):
                if db_token.expires_at < datetime.now(UTC):
                    await self.password_reset_repository.delete(db_token.id)
                    raise TokenNotFoundError(value=token)                    
                return db_token
        raise TokenNotFoundError(value=token)

    async def delete(self: Self, id: UUID) -> bool:
        return await self.password_reset_repository.delete(id)
    
    async def delete_all_expired_tokens(self: Self) -> bool:
        return await self.password_reset_repository.delete_all_expired_tokens()