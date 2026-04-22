from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.apps.emails.depends import get_email_client
from school_site.apps.emails.clients.emails import EmailClientProtocol
from school_site.core.depends import get_image_service
from school_site.core.services.files import FileServiceProtocol
from .schemas import CookieTokenSchema
from .repositories.users import UserRepositoryProtocol, UserRepository
from .repositories.refresh_tokens import RefreshTokenRepositoryProtocol, RefreshTokenRepository
from .repositories.reset_tokens import ResetTokenRepositoryProtocol, ResetTokenRepository
from .repositories.photo_user import PhotoUserRepositoryProtocol, PhotoUserRepository
from .services.passwords import PasswordServiceProtocol, PasswordService
from .services.users import UserServiceProtocol, UserService
from .services.photo_user import PhotoUserServiceProtocol, PhotoUserService
from .services.tokens import TokenServiceProtocol, TokenService, ResetPasswordTokenServiceProtocol, ResetPasswordTokenService
from .services.auth import AuthServiceProtocol, AuthService, ResetPasswordServiceProtocol, ResetPasswordService, AuthByAnotherUserServiceProtocol, AuthByAnotherUserService
from .use_cases.login import LoginUseCaseProtocol, LoginUseCase
from .use_cases.refresh import RefreshUseCaseProtocol, RefreshUseCase
from .use_cases.logout import LogoutUseCaseProtocol, LogoutUseCase
from .use_cases.change_password import ChangePasswordUseCaseProtocol, ChangePasswordUseCase
from .use_cases.create_user import CreateUserUseCase, CreateUserUseCaseProtocol
from .use_cases.get_all_users import GetAllUsersUseCase, GetAllUsersUseCaseProtocol
from .use_cases.get_user_by_id import GetUserByIdUseCase, GetUserByIdUseCaseProtocol
from .use_cases.update_user import UpdateUserUseCase, UpdateUserUseCaseProtocol
from .use_cases.delete_user import DeleteUserUseCase, DeleteUserUseCaseProtocol
from .use_cases.reset_password import ResetPasswordUseCaseProtocol, ResetPasswordUseCase
from .use_cases.confirm_reset_password import ConfirmResetPasswordUseCaseProtocol, ConfirmResetPasswordUseCase
from .use_cases.get_me import GetMeByUserIdUseCaseProtocol, GetMeByUserIdUseCase 
from .use_cases.auth_by_another_user import AuthByAnotherUserUseCaseProtocol, AuthByAnotherUserUseCase

def __get_user_repository(
        session: AsyncSession = Depends(get_async_session)
) -> UserRepositoryProtocol:
    return UserRepository(session)


def __get_refresh_tokens_repository(
        session: AsyncSession = Depends(get_async_session)
) -> RefreshTokenRepositoryProtocol:
    return RefreshTokenRepository(session)

def __get_reset_password_repository(
    session: AsyncSession = Depends(get_async_session)
) -> ResetTokenRepositoryProtocol:
    return ResetTokenRepository(session)

def __get_photo_user_repository(
    session: AsyncSession = Depends(get_async_session)
) -> PhotoUserRepositoryProtocol:
    return PhotoUserRepository(session)


def get_password_service() -> PasswordServiceProtocol:
    return PasswordService()

def get_photo_user_service(
    photo_repository: PhotoUserRepositoryProtocol = Depends(__get_photo_user_repository),
    file_service: FileServiceProtocol = Depends(lambda: get_image_service("users-photos"))
) -> PhotoUserServiceProtocol:
    return PhotoUserService(photo_repository, file_service)

def get_user_service(
    user_repository: UserRepositoryProtocol = Depends(__get_user_repository),
    password_service: PasswordServiceProtocol = Depends(get_password_service),
    photo_service: PhotoUserServiceProtocol = Depends(get_photo_user_service)
) -> UserServiceProtocol:
    return UserService(user_repository, password_service, photo_service)


def get_token_service(token_repository: RefreshTokenRepositoryProtocol = Depends(__get_refresh_tokens_repository)) -> \
    TokenServiceProtocol:
    return TokenService(token_repository)


def get_auth_service(user_service: UserServiceProtocol = Depends(get_user_service),
                     token_service: TokenServiceProtocol = Depends(get_token_service)) -> AuthServiceProtocol:
    return AuthService(user_service, token_service)

def get_login_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> LoginUseCaseProtocol:
    return LoginUseCase(auth_service)


def get_refresh_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> RefreshUseCaseProtocol:
    return RefreshUseCase(auth_service)


def get_logout_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> LogoutUseCaseProtocol:
    return LogoutUseCase(auth_service)

def get_change_password_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> ChangePasswordUseCaseProtocol:
    return ChangePasswordUseCase(auth_service)

def get_create_user_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service), user_service: UserServiceProtocol = Depends(get_user_service)) -> CreateUserUseCaseProtocol:
    return CreateUserUseCase(auth_service, user_service)

def get_all_users_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service), user_service: UserServiceProtocol = Depends(get_user_service)) -> GetAllUsersUseCaseProtocol:
    return GetAllUsersUseCase(auth_service, user_service)

def get_get_user_by_id_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service), user_service: UserServiceProtocol = Depends(get_user_service)) -> GetUserByIdUseCaseProtocol:
    return GetUserByIdUseCase(auth_service, user_service)

def get_update_user_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service), user_service: UserServiceProtocol = Depends(get_user_service)) -> UpdateUserUseCaseProtocol:
    return UpdateUserUseCase(auth_service, user_service)

def get_delete_user_use_case(auth_service: AuthServiceProtocol = Depends(get_auth_service), user_service: UserServiceProtocol = Depends(get_user_service)) -> DeleteUserUseCaseProtocol:
    return DeleteUserUseCase(auth_service, user_service)

def get_reset_password_token_service(token_repository: ResetTokenRepositoryProtocol = Depends(__get_reset_password_repository),
                                     password_service: PasswordServiceProtocol = Depends(get_password_service)
                                     ) -> ResetPasswordTokenServiceProtocol:
    return ResetPasswordTokenService(token_repository, password_service)

def get_reset_password_service(user_service: UserServiceProtocol = Depends(get_user_service),
                               mail_sender: EmailClientProtocol = Depends(get_email_client),
                               reset_password_service: ResetPasswordTokenServiceProtocol = Depends(get_reset_password_token_service),
                               auth_service: AuthServiceProtocol = Depends(get_auth_service)) -> \
    ResetPasswordServiceProtocol:
    return ResetPasswordService(user_service, mail_sender, reset_password_service, auth_service)

def get_auth_by_another_user_service(
    user_service: UserServiceProtocol = Depends(get_user_service),
    token_service: TokenServiceProtocol = Depends(get_token_service)
) -> AuthByAnotherUserServiceProtocol:
    return AuthByAnotherUserService(user_service, token_service)

def get_reset_password_use_case(reset_password_service: ResetPasswordServiceProtocol = Depends(get_reset_password_service)) -> \
    ResetPasswordUseCaseProtocol:
    return ResetPasswordUseCase(reset_password_service)

def get_confirm_reset_password_use_case(reset_password_service: ResetPasswordServiceProtocol = Depends(get_reset_password_service)) -> \
    ConfirmResetPasswordUseCaseProtocol:
    return ConfirmResetPasswordUseCase(reset_password_service)

def get_me_by_user_id_use_case(token_service: TokenServiceProtocol = Depends(get_token_service),
                               user_service: UserServiceProtocol = Depends(get_user_service)) -> \
    GetMeByUserIdUseCaseProtocol:
    return GetMeByUserIdUseCase(token_service, user_service)

def get_auth_by_another_user_use_case(
    auth_service: AuthServiceProtocol = Depends(get_auth_service),
    auth_by_another_user_service: AuthByAnotherUserServiceProtocol = Depends(get_auth_by_another_user_service)
) -> AuthByAnotherUserUseCaseProtocol:
    return AuthByAnotherUserUseCase(auth_service, auth_by_another_user_service)

access_token_schema = CookieTokenSchema(cookie_name="access_token")
refresh_token_schema = CookieTokenSchema(cookie_name="refresh_token")
