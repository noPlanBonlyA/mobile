from uuid import uuid4
from school_site.core.db import Base
from school_site.core.models import CreationTimeMixin, TimestampMixin, FileMixin
from school_site.core.enums import UserRole
from sqlalchemy import Column, ForeignKey, String, Enum, DateTime, Integer, Sequence, Date
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

users_seq = Sequence("users_username_seq")

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    phone_number = Column(String(20), index=True, nullable=True)
    email = Column(String(255), index=True, nullable=False)
    password_hash = Column(String)
    role = Column(Enum(UserRole))
    birth_date = Column(Date, nullable=False)
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    photo = relationship("PhotoUser", back_populates="user", uselist=False, cascade="all, delete-orphan")


class RefreshToken(Base, CreationTimeMixin):
    __tablename__ = "refresh_tokens"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    hashed_refresh_token = Column(String, index=True)
    
    user = relationship("User", back_populates="refresh_tokens")


class PasswordResetTokens(Base, CreationTimeMixin):
    __tablename__ = "password_reset_tokens"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    token_hash = Column(String(128), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)


class PhotoUser(Base, TimestampMixin, FileMixin):
    __tablename__ = 'photo_users'
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )    
    user = relationship("User", back_populates="photo")


__all__ = ["User", "RefreshToken", "PasswordResetTokens", "PhotoUser"]