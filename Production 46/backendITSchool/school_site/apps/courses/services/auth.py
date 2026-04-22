import logging
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.apps.users.schemas import UserTokenDataReadSchema
from school_site.core.enums import UserRole


logger = logging.getLogger(__name__)


class AuthAdminServiceProtocol(TokenServiceProtocol):
    async def get_admin_user(self, token: str) -> UserTokenDataReadSchema:
        ...

    async def get_student_user(self, token: str) -> UserTokenDataReadSchema:
        ...
    
    async def get_teacher_user(self, token: str) -> UserTokenDataReadSchema:
        ...

class AuthService(AuthAdminServiceProtocol):
    def __init__(self, auth_admin_service: TokenServiceProtocol):
        self.auth_admin_service = auth_admin_service

    async def decode_access_token(self, token: str) -> UserTokenDataReadSchema:
        return await self.auth_admin_service.decode_access_token(token)
    
    async def get_admin_user(self, token: str) -> UserTokenDataReadSchema:
        user_data = await self.decode_access_token(token)
        if user_data.role not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
            logger.error("User is not an admin or superadmin")
            raise PermissionDeniedError()
        return user_data 
    
    async def get_student_user(self, token: str) -> UserTokenDataReadSchema:
        user_data = await self.decode_access_token(token)
        if user_data.role not in [UserRole.STUDENT]:
            logger.error("User is not a student")
            raise PermissionDeniedError()
        return user_data 
    
    async def get_teacher_user(self, token: str) -> UserTokenDataReadSchema:
        user_data = await self.decode_access_token(token)
        if user_data.role not in [UserRole.TEACHER]:
            logger.error("User is not a teacher")
            raise PermissionDeniedError()
        return user_data 