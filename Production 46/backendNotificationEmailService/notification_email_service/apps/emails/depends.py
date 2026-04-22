from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from notification_email_service.core.db import get_async_session
from .repositories.email_logs import EmailLogRepositoryProtocol, EmailLogRepository
from .services.email_sender import EmailSenderServiceProtocol, EmailSenderService
from .services.email_logs import EmailLogServiceProtocol, EmailLogService
from .services.auth import TokenServiceProtocol, TokenService
from .use_cases.send_and_save_email import SendAndSaveEmailUseCaseProtocol, SendAndSaveEmailUseCase


def __get_email_log_repository(session: AsyncSession = Depends(get_async_session)
) -> EmailLogRepositoryProtocol:
    return EmailLogRepository(session)


def get_email_sender() -> EmailSenderServiceProtocol:
    return EmailSenderService()


def get_email_log_service(
        background_tasks: BackgroundTasks,
        repository: EmailLogRepositoryProtocol = Depends(__get_email_log_repository),
        email_sender: EmailSenderServiceProtocol = Depends(get_email_sender)
) -> EmailLogServiceProtocol:
    return EmailLogService(repository, email_sender, background_tasks)


def get_token_service() -> TokenServiceProtocol:
    return TokenService()

def get_send_and_save_email_use_case(
        token_service: TokenServiceProtocol = Depends(get_token_service), 
        email_log_service: EmailLogServiceProtocol = Depends(get_email_log_service)
) -> SendAndSaveEmailUseCaseProtocol:
    return SendAndSaveEmailUseCase(token_service, email_log_service)