import logging
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.schemas import UserTokenDataReadSchema


logger = logging.getLogger(__name__)


class AuthAdminServiceProtocol(TokenServiceProtocol):
    async def decode_access_token(self, token: str) -> UserTokenDataReadSchema:
        ...
    async def get_admin_user(self, token: str) -> UserTokenDataReadSchema:
        ...

class AuthService(AuthAdminServiceProtocol):
    def __init__(self, auth_admin_service: TokenServiceProtocol):
        self.auth_admin_service = auth_admin_service

    async def decode_access_token(self, token: str) -> UserTokenDataReadSchema:
        return await self.auth_admin_service.decode_access_token(token)
    
    async def get_admin_user(self, token: str) -> UserTokenDataReadSchema:
        return await self.auth_admin_service.get_admin_user(token) 