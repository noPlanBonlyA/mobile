import logging
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.apps.users.schemas import UserTokenDataReadSchema
from school_site.core.enums import UserRole


logger = logging.getLogger(__name__)


class AuthAdminAndTeacherServiceProtocol(TokenServiceProtocol):
    async def get_teacher_user(self, token: str) -> UserTokenDataReadSchema:
        ...


class AuthService(AuthAdminAndTeacherServiceProtocol):
    def __init__(self, auth_admin_service: TokenServiceProtocol):
        self.auth_admin_service = auth_admin_service

    async def decode_access_token(self, token: str) -> UserTokenDataReadSchema:
        return await self.auth_admin_service.decode_access_token(token)
    
    async def get_admin_user(self, token: str) -> UserTokenDataReadSchema:
        return await self.auth_admin_service.get_admin_user(token)
    
    async def get_teacher_user(self, token):
        user_data = await self.decode_access_token(token)
        if user_data.role != UserRole.TEACHER:
            logger.error("User is not a teacher")
            raise PermissionDeniedError()
        return user_data 