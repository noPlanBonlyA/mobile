from uuid import uuid4
from sqlalchemy import Column, ForeignKey, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from school_site.core.db import Base
from school_site.core.models import TimestampMixin


class Student(Base, TimestampMixin):
    __tablename__ = "students"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    points = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('points >= 0', name='positive_price_check'),
    )
    user_id = Column(
        PostgresUUID, 
        ForeignKey("users.id", ondelete="CASCADE"),  # ← CASCADE на уровне БД
        nullable=False,
        unique=True  # Уникальность для связи с пользователем
    )
    user = relationship("User", back_populates="student", foreign_keys="[Student.user_id]")
    groups = relationship("Group", secondary="group_student", back_populates="students")
    group_students = relationship("GroupStudent", back_populates="student", cascade="all, delete-orphan")
    
    lessons = relationship(
        "LessonStudent",
        back_populates="student",
        cascade="all, delete" 
    )
    courses = relationship(
    "CourseStudent",
    back_populates="student",
    cascade="all, delete-orphan"
)
    comments_students = relationship("CommentStudent", back_populates="student")

__all__ = ["Student"]
