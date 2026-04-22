from uuid import uuid4
from sqlalchemy import String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import mapped_column
from school_site.core.db import Base
from school_site.core.models import TimestampMixin

class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    start_datetime = mapped_column(DateTime, nullable=False)
    end_datetime = mapped_column(DateTime, nullable=False)
    auditorium = mapped_column(String, nullable=True)
    is_opened = mapped_column(Boolean, default=False, nullable=False)

class EventsUsers(Base):
    __tablename__ = "events_users"

    user_id = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key=True
    )
    event_id = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("events.id", ondelete="CASCADE"), 
        primary_key=True
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='unique_user_event'),
    )

__all__ = ["Event", "EventsUsers"]