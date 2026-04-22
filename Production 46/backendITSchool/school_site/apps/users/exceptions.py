from typing import Any
from fastapi import status
from school_site.core.utils.exceptions import ModelAlreadyExistsError, CoreException, \
    ModelFieldNotFoundException
from school_site.apps.users.models import User, PasswordResetTokens

class UsernameAlreadyExistsError(ModelAlreadyExistsError):
    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            model=User,
            field="username",
            message="try another username for create",
            headers=headers,
        )


class UsernameNotExistsExceptions(ModelFieldNotFoundException):
    """
    Исключение, возникающее при поиске несуществующего username.
    """
    def __init__(
            self,
            value: Any,
            headers: dict[str, Any] | None = None
    ) -> None:
       super().__init__(
            model=User,
            field="username",
            value=value,
            headers=headers,
        )
 
class InvalidCredentialsError(CoreException):
    """
    Исключение, возникающее при неверных учетных данных (например, неверный пароль).
    """
    def __init__(
        self,
        detail: str = "Invalid credentials provided",
        headers: dict[str, Any] | None = None
    ) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)


class InvalidTokenError(CoreException):
    """
    Исключение, возникающее при недействительном или истекшем токене.
    """
    def __init__(
        self,
        detail: str = "Invalid or expired token",
        headers: dict[str, Any] | None = None
    ) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)


class TokenNotFoundError(ModelFieldNotFoundException):
    """
    Исключение, возникающее при отсутствии токена в запросе.
    """
    def __init__(
       self,
        value: Any,
        headers: dict[str, Any] | None = None
    ) -> None:
        super().__init__(
            model=PasswordResetTokens,
            field="hashed_token",
            value=value,
            headers=headers,
        )