from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4
from sqlalchemy import DateTime, Column, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func



class CreationTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), server_default=func.now()
    )


class TimestampMixin(CreationTimeMixin):
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
        onupdate=datetime.now(UTC),
    )

class FileMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)