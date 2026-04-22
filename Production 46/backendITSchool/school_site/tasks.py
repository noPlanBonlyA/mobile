import logging
from school_site.apps.users.repositories.reset_tokens import ResetTokenRepositoryProtocol, ResetTokenRepository
from school_site.apps.users.services.passwords import PasswordServiceProtocol, PasswordService
from school_site.apps.users.services.tokens import ResetPasswordTokenService
from .core.db import AsyncSessionFactory

logger = logging.getLogger(__name__)

async def cleanup_reset_password_expired_tokens():
    logger.info("Start delete all expired tokens")
    async with AsyncSessionFactory() as session:
        repository: ResetTokenRepositoryProtocol = ResetTokenRepository(session)
        password_service: PasswordServiceProtocol = PasswordService()

        token_service: ResetPasswordTokenService = ResetPasswordTokenService(repository, password_service)
        await token_service.delete_all_expired_tokens()    