from uuid import uuid4
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from school_site.core.db import Base
from school_site.core.models import TimestampMixin


class Teacher(Base, TimestampMixin):
    __tablename__ = "teachers"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        PostgresUUID, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    comments = relationship("Comment", back_populates="teacher")
    user = relationship("User", back_populates="teacher", foreign_keys="[Teacher.user_id]")
    groups = relationship("Group", back_populates="teacher")

__all__ = ["Teacher"]