from notification_email_service.core.use_cases import UseCaseProtocol 
from ..schemas import EmailCreate, EmailLogReadDB
from ..services.email_logs import EmailLogServiceProtocol
from ..services.auth import TokenServiceProtocol


class SendAndSaveEmailUseCaseProtocol(UseCaseProtocol[EmailLogReadDB]):
    async def __call__(self, token: str, email: EmailCreate) -> EmailLogReadDB:
        ...


class SendAndSaveEmailUseCase(SendAndSaveEmailUseCaseProtocol):
    def __init__(self, token_service: TokenServiceProtocol,
                  email_log_service: EmailLogServiceProtocol):
        self.token_service = token_service
        self.email_log_service = email_log_service

    async def __call__(self, token: str, email: EmailCreate) -> EmailLogReadDB:
        self.token_service.decode_access_token(token)
        return await self.email_log_service.save_and_send_email(email)
