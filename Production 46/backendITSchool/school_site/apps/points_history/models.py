from uuid import uuid4
from sqlalchemy import ForeignKey, Integer, Enum, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import mapped_column
from school_site.core.db import Base
from school_site.core.models import TimestampMixin
from .enums import Reason

class PointsHistory(Base, TimestampMixin):
    __tablename__ = "points_history"

    id = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = mapped_column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("students.id", ondelete="CASCADE"), 
        nullable=False
    )
    reason = mapped_column(Enum(Reason), nullable=False)
    changed_points = mapped_column(Integer, nullable=False)
    description = mapped_column(String, nullable=True)
    
__all__ = ["PointsHistory"]