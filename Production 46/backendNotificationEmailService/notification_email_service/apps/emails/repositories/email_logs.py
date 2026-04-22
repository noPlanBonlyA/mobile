from notification_email_service.core.repositories.base_repository import BaseRepositoryImpl
from notification_email_service.apps.emails.models import EmailLog
from notification_email_service.apps.emails.schemas import EmailLogCreateDB, EmailLogReadDB, EmailLogUpdateDB


class EmailLogRepositoryProtocol(BaseRepositoryImpl[
    EmailLog,
    EmailLogReadDB,
    EmailLogCreateDB,
    EmailLogUpdateDB
]):
    pass


class EmailLogRepository(EmailLogRepositoryProtocol):
    pass