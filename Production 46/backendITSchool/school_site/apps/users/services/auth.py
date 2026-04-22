import logging
from typing import Protocol, Self
from uuid import UUID
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import PermissionDeniedError
from ..texts import HTML_EMAIL_BODY_TEMPLATE, HTML_EMAIL_SUBJECT_TEMPLATE
from ..schemas import (
    AuthReadSchema, PasswordChangeSchema, UserResetSchema, UserWithPhotoReadSchema, 
    ResetTokenSchema, ResetPasswordRequest, UserTokenDataReadSchema, TokenReadSchema
)
from .users import UserServiceProtocol
from .tokens import TokenServiceProtocol, ResetPasswordTokenServiceProtocol
from school_site.apps.emails.clients.emails import EmailClientProtocol
from school_site.apps.emails.schemas import EmailRequestDTO
from school_site.settings import settings

logger = logging.getLogger(__name__)


class AuthServiceProtocol(Protocol):
    async def login(self: Self, username: str, password: str) -> AuthReadSchema:
        ...
    
    async def refresh(self: Self, refresh_token: str) -> AuthReadSchema:
        ...

    async def logout(self: Self, refresh_token: str) -> None:
        ...

    async def change_password_authenticated(self: Self, access_token: str, password: PasswordChangeSchema) -> AuthReadSchema:
        ...

    async def reset_password_via_token(self: Self, user_id: UUID, new_password: str) -> AuthReadSchema:
        ...

    async def get_admin_user(self: Self, token: str) -> UserTokenDataReadSchema:
        ...

    async def get_super_admin_user(self: Self, token: str) -> UserTokenDataReadSchema:
        ...

    async def decode_acess_token(self: Self, token: str) -> UserTokenDataReadSchema:
        ...

class AuthService(AuthServiceProtocol):
    def __init__(
        self: Self,
        user_service: UserServiceProtocol,
        token_service: TokenServiceProtocol,
    ):
        self.user_service = user_service
        self.token_service = token_service
    
    async def change_password_authenticated(self: Self, access_token: str, password: PasswordChangeSchema) -> AuthReadSchema:
        user_data = await self.token_service.decode_access_token(access_token)
        await self.user_service.authenticate_user_by_id(user_data.user_id, password.old_password)
        return await self.reset_password_via_token(user_data.user_id, password.new_password)

    async def reset_password_via_token(self: Self, user_id: UUID, new_password: str) -> AuthReadSchema:
        updated_user = await self.user_service.change_password(user_id, new_password)
        await self.token_service.delete_all_by_user_id(updated_user.id)
        new_access_token, new_refresh_data = await self._create_tokens(updated_user.id, updated_user.role)

        user_with_photo = await self.user_service.get_user_by_id(updated_user.id)

        return AuthReadSchema(user=user_with_photo,
                              access_token=new_access_token,
                              refresh_token=new_refresh_data)
    
    async def login(self: Self, username: int, password: str) -> AuthReadSchema:
        logger.info(f"Login attempt for user: {username}")
        
        user_without_photo = await self.user_service.authenticate_user_without_photo(username, password)
        user = await self.user_service.get_user_by_id(user_without_photo.id)
        
        access_token, refresh_data = await self._create_tokens(user.id, user.role)
        
        logger.info(f"Login successful for user: {username}")
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=refresh_data)
    
    async def _create_tokens(self: Self, user_id: UUID, role: UserRole) -> tuple[str, str]:
        access_token = self.token_service.create_access_token(
            user_id=user_id, 
            role=role, 
        )
        
        refresh_data = await self.token_service.create_refresh_token(user_id)

        return access_token, refresh_data
    
    async def refresh(self: Self, refresh_token: str) -> AuthReadSchema:
        logger.info("Refreshing tokens")
        
        db_token = await self.token_service.verify_refresh_token(refresh_token)
        
        user = await self.user_service.get_user_by_id(db_token.user_id)
        
        await self.token_service.delete(db_token.id)
        
        access_token = self.token_service.create_access_token(
            user_id=user.id, 
            role=user.role, 
        )
        
        new_refresh_data = await self.token_service.create_refresh_token(user.id)
        
        logger.info(f"Tokens refreshed successfully for user: {user.id}")
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=new_refresh_data)
    
    
    async def logout(self: Self, refresh_token: str) -> None:
        db_token = await self.token_service.verify_refresh_token(refresh_token)
        user_id = db_token.user_id
        logger.info(f"Logout for user: {user_id}")
        if db_token:
            await self.token_service.delete(db_token.id)
            logger.info(f"Refresh token removed for user: {user_id}")
        
        logger.info(f"Logout successful for user: {user_id}")
    
    async def decode_acess_token(self: Self, token: str) -> UserTokenDataReadSchema:
        return await self.token_service.decode_access_token(token)

    async def get_admin_user(self: Self, token: str) -> UserTokenDataReadSchema:
        user_data = await self.decode_acess_token(token)
        if user_data.role not in {UserRole.ADMIN, UserRole.SUPERADMIN}:
            raise PermissionDeniedError()
        return user_data
        
    async def get_super_admin_user(self: Self, token: str) -> UserTokenDataReadSchema:
        user_data = await self.decode_acess_token(token)
        if user_data.role != UserRole.SUPERADMIN:
            raise PermissionDeniedError()
        return user_data
    
    

class ResetPasswordServiceProtocol(Protocol):
    async def reset_password(self: Self, user: UserResetSchema) -> bool:
        ...
    
    async def confirm_reset_password(self: Self, passwordResetSchema: ResetPasswordRequest) -> AuthReadSchema:
        ...


class ResetPasswordService(ResetPasswordServiceProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol,
                 mail_sender: EmailClientProtocol,
                reset_password_token_service: ResetPasswordTokenServiceProtocol,
                auth_service: AuthServiceProtocol):
        self.user_service = user_service
        self.reset_password_token_service = reset_password_token_service
        self.mail_sender = mail_sender
        self.auth_service = auth_service


    async def reset_password(self: Self, user: UserResetSchema) -> bool:
        logger.info(f"Resetting password for user: {user.email}")
        user_data = await self.user_service.get_user_by_username(user.username)
        if user_data:
            if user_data.email == user.email:
                token = await self.reset_password_token_service.generate_reset_token(user_data.id)
                message = self._generate_email_message(user_data, token)
                logger.info(f"Reset password email sent to user: {user.email}")
                await self.mail_sender.send_email(message)
            else:
                logger.warning(f"Input email: {user.email} does not match with email in database: {user_data.email}")
        else:
            logger.warning(f"User with username: {user.username} does not exist. Not sent message to email")
        return True


    async def confirm_reset_password(self: Self, passwordResetSchema: ResetPasswordRequest) -> AuthReadSchema:
        logger.debug(f"Confirming password reset for user: {passwordResetSchema.token}")
        token = passwordResetSchema.token
        token_data = await self.reset_password_token_service.get_by_token(token)
        new_user = await self.auth_service.reset_password_via_token(token_data.user_id, passwordResetSchema.new_password)
        await self.reset_password_token_service.delete(token_data.id)
        return new_user


    def _generate_email_message(self: Self, user: UserWithPhotoReadSchema, token: ResetTokenSchema) -> str:
        name = user.first_name or user.username
        
        body =  HTML_EMAIL_BODY_TEMPLATE.format(
            name=name,
            url=settings.frontend_url,
            token=token.token,
            duration=token.hours
        )

        subject = HTML_EMAIL_SUBJECT_TEMPLATE.strip()

        return EmailRequestDTO(
            to_email=user.email,
            body=body,
            subject=subject
        )


class AuthByAnotherUserServiceProtocol(Protocol):
    async def auth_by_another_user(self: Self, user_id: UUID) -> AuthReadSchema:
        ...

class AuthByAnotherUserService(AuthByAnotherUserServiceProtocol):
    def __init__(self: Self, user_service: UserServiceProtocol, token_service: TokenServiceProtocol):
        self.user_service = user_service
        self.token_service = token_service

    async def auth_by_another_user(self: Self, user_id: UUID) -> AuthReadSchema:
        user = await self.user_service.get_user_by_id(user_id)
        access_token, refresh_data = await self._create_tokens(user.id, user.role)
        
        return AuthReadSchema(user=user,
                              access_token=access_token,
                              refresh_token=refresh_data)
    
    async def _create_tokens(self: Self, user_id: UUID, role: UserRole) -> tuple[TokenReadSchema, TokenReadSchema]:
        access_token = self.token_service.create_access_token(
            user_id=user_id, 
            role=role, 
        )
        
        refresh_data = await self.token_service.create_refresh_token(user_id)

        return access_token, refresh_data