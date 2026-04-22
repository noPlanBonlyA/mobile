from typing import Protocol, Union
from aiosmtplib import send
from email.message import EmailMessage
import logging
from notification_email_service.apps.emails.schemas import EmailCreate
from notification_email_service.settings import settings

logger = logging.getLogger(__name__)

class EmailSenderServiceProtocol(Protocol):
    async def send_email(self, email: EmailCreate) -> Union[bool, str]:
        pass

class EmailSenderService(EmailSenderServiceProtocol):
    async def send_email(self, email: EmailCreate) -> Union[bool, str]:
        logger.info(f"Preparing to send email to {email.to_email}")
        message = EmailMessage()
        message["From"] = settings.smtp.user
        message["To"] = email.to_email
        message["Subject"] = email.subject
        message.set_content("Ваш клиент не поддерживает HTML.")
        message.add_alternative(email.body, subtype="html")

        try:
            logger.info(f"Attempting to send email via SMTP to {settings.smtp.host}:{settings.smtp.port}")
            await send(
                message,
                hostname=settings.smtp.host,
                port=settings.smtp.port,
                username=settings.smtp.user,
                password=settings.smtp.password,
                start_tls=settings.smtp.use_tls
            )
            logger.info(f"Successfully sent email to {email.to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {email.to_email}. Error: {str(e)}")
            return str(e) 
