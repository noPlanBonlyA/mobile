from fastapi import BackgroundTasks
from typing import Protocol
from datetime import datetime, UTC
import logging
from notification_email_service.apps.emails.repositories.email_logs import EmailLogRepositoryProtocol
from notification_email_service.apps.emails.schemas import(
    EmailCreate, EmailLogReadDB, EmailLogCreateDB, EmailLogUpdateDB
) 
from .email_sender import EmailSenderServiceProtocol
from ..enums import EmailStatus


logger = logging.getLogger(__name__)

class EmailLogServiceProtocol(Protocol):
    repository: EmailLogRepositoryProtocol
    email_sender: EmailSenderServiceProtocol
    background_tasks: BackgroundTasks

    async def create_email_log(self, email_log: EmailLogCreateDB) -> EmailLogReadDB:
        ...
    
    async def update_email_log(self, email_log: EmailLogUpdateDB) -> EmailLogReadDB:
        ...

    async def save_and_send_email(self, email: EmailCreate) -> EmailLogReadDB:
        ...

    async def send_email_and_update_status(self, email: EmailLogReadDB) -> EmailLogReadDB:
        ...


class EmailLogService(EmailLogServiceProtocol):
    def __init__(self, repository: EmailLogRepositoryProtocol,
                 email_sender: EmailSenderServiceProtocol,
                 background_tasks: BackgroundTasks):
        self.repository = repository
        self.sender = email_sender
        self.tasks = background_tasks

    async def create_email_log(self, email_log: EmailLogCreateDB) -> EmailLogReadDB:
        return await self.repository.create(email_log)
    
    async def update_email_log(self, email_log: EmailLogUpdateDB) -> EmailLogReadDB:
        return await self.repository.update(email_log)

    async def save_and_send_email(self, email: EmailCreate) -> EmailLogReadDB:
        logger.info(f"Creating email log for recipient: {email.to_email}")
        email_log = EmailLogCreateDB(
            to_email=email.to_email,
            subject=email.subject,
            body=email.body,
            status=EmailStatus.QUEUED
        )
        created_email_log = await self.repository.create(email_log)
        logger.info(f"Email log created with ID: {created_email_log.id}")

        logger.info(f"Adding email send task to background for ID: {created_email_log.id}")
        self.tasks.add_task(
            self.send_email_and_update_status,
            email=created_email_log
        )

        return created_email_log
    
    async def send_email_and_update_status(self, email: EmailLogReadDB) -> EmailLogReadDB:
        logger.info(f"Starting to send email ID: {email.id} to {email.to_email}")
        
        email_to_send = EmailCreate(
            to_email=email.to_email,
            subject=email.subject,
            body=email.body
        )

        result = await self.sender.send_email(email_to_send)

        if result is True:
            logger.info(f"Email ID: {email.id} sent successfully")
            return await self._update_email_status(email, EmailStatus.SENT)
        else:
            error_msg = str(result)
            logger.error(f"Failed to send email ID: {email.id}. Error: {error_msg}")
            return await self._update_email_status(email, EmailStatus.FAILED, error_msg)

    async def _update_email_status(self, email: EmailLogReadDB, status: EmailStatus, error: str | None = None) -> EmailLogReadDB:
        logger.info(f"Updating email ID: {email.id} status to {status}")
        email_log_to_update = EmailLogUpdateDB(
            id=email.id,
            to_email=email.to_email,
            subject=email.subject,
            body=email.body,
            status=status,
            sent_at=datetime.now(UTC),
            error=error
        )
        updated_log = await self.update_email_log(email_log_to_update)
        logger.info(f"Email ID: {email.id} status updated successfully")
        return updated_log

