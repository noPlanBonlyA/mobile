from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from school_site.core.db import Base
from school_site.core.models import TimestampMixin


class GroupStudent(Base):
    __tablename__ = "group_student"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    group_id = Column(PostgresUUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True)
    student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), primary_key=True)

    group = relationship("Group", back_populates="group_students")
    student = relationship("Student", back_populates="group_students")

    __table_args__ = (
        UniqueConstraint('group_id', 'student_id', name='uq_group_student'),
    )

class Group(Base, TimestampMixin):
    __tablename__ = "groups"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    teacher_id = Column(PostgresUUID(as_uuid=True), ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    group_students = relationship("GroupStudent", back_populates="group", cascade="all, delete-orphan")
    students = relationship("Student", secondary="group_student", back_populates="groups")
    teacher = relationship("Teacher", back_populates="groups")
    lessons = relationship(
        "LessonGroup", 
        back_populates="group",
        cascade="all, delete"  
    )

__all__ = ["GroupStudent", "Group"]