from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import UUID
from school_site.core.schemas import(
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
) 

# ====== PHOTO SCHEMAS =======

class PhotoBaseSchema(BaseModel):
    name: str = Field(..., description="Название фотографии товара")
    product_id: Optional[UUID] = None

class PhotoCreateSchema(CreateBaseModel, PhotoBaseSchema):
    pass

class PhotoCreateDBSchema(CreateBaseModel, PhotoBaseSchema):
    product_id: UUID
    path: str

class PhotoUpdateSchema(PhotoBaseSchema):
    id: Optional[UUID] = None

class PhotoUpdateDBSchema(UpdateBaseModel, PhotoBaseSchema):
    product_id: UUID

class PhotoReadDBSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    path: str

    class Config:
        from_attributes = True

class PhotoReadSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    url: HttpUrl
# --------------------------------

class ProductBaseSchema(BaseModel):
    name: str = Field(..., description="Название товара")
    description: Optional[str] = Field(None, description="Описание товара")
    price: int = Field(..., ge=0, description="Цена товара, целое положительное число")
    is_pinned: bool = Field(False, description="Флаг закрепления товара на главной странице")

class ProductCreateDBSchema(CreateBaseModel, ProductBaseSchema):
    pass

class ProductCreateSchema(ProductCreateDBSchema):
    photo: Optional[PhotoCreateSchema] = Field(None, description="Фотография товара (опционально)")

class ProductUpdateDBSchema(UpdateBaseModel, ProductBaseSchema):
    pass

class ProductUpdateSchema(ProductBaseSchema):
    photo: Optional[PhotoUpdateSchema] = None


class ProductReadDBSchema(ProductBaseSchema, TimestampMixin):
    id: UUID


class ProductWithPhotoDBReadSchema(ProductBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadDBSchema] = None

class ProductReadSchema(ProductBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadSchema] = None




class ProductDBPaginationResultSchema(PaginationResultSchema[ProductWithPhotoDBReadSchema]):
    pass


class ProductPaginationResultSchema(PaginationResultSchema[ProductReadSchema]):
    pass