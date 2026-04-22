from school_site.core.schemas import TimestampMixin, BaseModel, CreateBaseModel, UpdateBaseModel
from uuid import UUID
from typing import TypeVar, Generic, List, Optional
from pydantic import Field, HttpUrl

T = TypeVar('T')

class PhotoBaseSchema(BaseModel):
    name: str = Field(..., description="Название фотографии новости")
    news_id: Optional[UUID] = None

class PhotoCreateSchema(CreateBaseModel, PhotoBaseSchema):
    pass

class PhotoCreateDBSchema(CreateBaseModel, PhotoBaseSchema):
    news_id: UUID
    path: str

class PhotoUpdateSchema(PhotoBaseSchema):
    id: Optional[UUID] = None

class PhotoUpdateDBSchema(UpdateBaseModel, PhotoBaseSchema):
    news_id: UUID

class PhotoReadDBSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    path: str

    class Config:
        from_attributes = True

class PhotoReadSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    url: HttpUrl


class PaginationResultSchema(BaseModel, Generic[T]):
    count: int
    objects: List[T]

class NewsBaseSchema(BaseModel):
    name: str
    description: str
    is_pinned: bool

class NewsCreateSchema(CreateBaseModel, NewsBaseSchema):
    photo: Optional[PhotoCreateSchema] = Field(None, description="Фотография новости (опционально)")

class NewsCreateDBSchema(CreateBaseModel, NewsBaseSchema):
    pass

class NewsReadSchema(NewsBaseSchema, TimestampMixin):
    id: UUID

class NewsWithPhotoReadDBSchema(NewsBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadDBSchema] = None


class NewsWithPhotoReadSchema(NewsBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadSchema] = None
    

class NewsUpdateSchema(NewsBaseSchema):
    photo: Optional[PhotoUpdateSchema] = None 


class NewsUpdateDBSchema(UpdateBaseModel, NewsBaseSchema):
    pass


class NewsWithPhotoPaginationResultDBSchema(PaginationResultSchema[NewsWithPhotoReadDBSchema]):
    pass


class NewsWithPhotoPaginationResultSchema(PaginationResultSchema[NewsWithPhotoReadSchema]):
    pass
