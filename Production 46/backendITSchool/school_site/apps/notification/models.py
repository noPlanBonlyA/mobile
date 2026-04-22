from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from school_site.core.db import Base
from school_site.core.models import TimestampMixin
from sqlalchemy.sql.sqltypes import Text
from sqlalchemy.schema import CheckConstraint

class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    content = Column(Text, nullable=False)
    
class NotificationRecipients(Base, TimestampMixin):
    __tablename__ = "notification_recipients"

    notification_id = Column(PostgresUUID(as_uuid=True), ForeignKey("notifications.id"), primary_key=True)
    recipient_type = Column(String, nullable=False)
    recipient_id = Column(PostgresUUID(as_uuid=True), primary_key=True, nullable=False)
    
    __table_args__ = (
        CheckConstraint(
            "recipient_type IN ('student', 'group')",
            name="check_recipient_type"
        ),
    )


class ReadStatus(Base, TimestampMixin):
    __tablename__ = "read_status"

    notification_id = Column(PostgresUUID(as_uuid=True), ForeignKey("notifications.id"), primary_key=True)
    student_id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    is_read = Column(Boolean, nullable=False, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
