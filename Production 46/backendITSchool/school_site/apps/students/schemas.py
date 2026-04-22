from pydantic import Field
from uuid import UUID
from school_site.core.schemas import(
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
) 
from school_site.apps.users.schemas import UserReadSchema, UserWithPhotoReadSchema


class StudentBaseSchema(TimestampMixin):
    user_id: UUID
    points: int = Field(..., ge=0, description="Баллы студента, целое положительное число")


class StudentCreateSchema(CreateBaseModel, StudentBaseSchema):
    pass


class StudentUpdateSchema(UpdateBaseModel, StudentBaseSchema):
    pass


class StudentReadSchema(StudentBaseSchema):
    id: UUID


class StudentReadWithUserSchema(StudentBaseSchema):
    id: UUID
    user: UserReadSchema

class StudentReadWithUserAndUsePhotoSchema(StudentBaseSchema):
    id: UUID
    user: UserWithPhotoReadSchema


class StudentPaginationResultSchema(PaginationResultSchema[StudentReadSchema]):
    pass

class StudentPaginationWithUserResultSchema(PaginationResultSchema[StudentReadWithUserSchema]):
    pass

class StudentPaginationWithUserAndUserPhotoResultSchema(PaginationResultSchema[StudentReadWithUserAndUsePhotoSchema]):
    pass