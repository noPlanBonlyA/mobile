from uuid import uuid4
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from notification_email_service.core.db import Base
from notification_email_service.core.models import CreationTimeMixin
from .enums import EmailStatus


class EmailLog(Base, CreationTimeMixin):
    __tablename__ = 'email_logs'

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    to_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(Enum(EmailStatus), nullable=False)
    error = Column(Text, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, default=0)