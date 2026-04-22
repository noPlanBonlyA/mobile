from uuid import uuid4
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from school_site.core.db import Base 
from school_site.core.models import TimestampMixin, FileMixin
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID


class News(Base, TimestampMixin):
    __tablename__ = 'news'
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    is_pinned = Column(Boolean)

    photo = relationship("PhotoNews", back_populates="news", uselist=False, cascade="all, delete-orphan")


    
class PhotoNews(Base, TimestampMixin, FileMixin):
    __tablename__ = 'photo_news'
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    news_id = Column(
        PostgresUUID(as_uuid=True),
        ForeignKey("news.id"),  # ← Добавлен внешний ключ
        nullable=False,
    )    
    news = relationship("News", back_populates="photo")

__all__ = ["News", "PhotoNews"]