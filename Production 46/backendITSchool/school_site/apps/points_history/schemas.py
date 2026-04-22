from pydantic import BaseModel, Field
from uuid import UUID
from school_site.core.schemas import CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
from .enums import Reason

class PointsHistoryBaseSchema(BaseModel):
    student_id: UUID = Field(..., description="ID of the student whose points are being changed")
    reason: Reason = Field(..., description="Reason for the points change")
    changed_points: int = Field(..., description="Number of points changed")
    description: str | None = Field(None, description="Optional description of the points change")

class PointsHistoryCreateSchema(CreateBaseModel, PointsHistoryBaseSchema):
    pass

class PointsHistoryUpdateSchema(PointsHistoryBaseSchema):
    pass

class PointsHistoryUpdateDBSchema(UpdateBaseModel, PointsHistoryBaseSchema):
    pass

class PointsHistoryReadSchema(TimestampMixin, PointsHistoryBaseSchema):
    id: UUID = Field(..., description="Unique identifier for the points history entry")

    class Config:
        from_attributes = True


class PointsHistoryPaginationSchema(PaginationResultSchema[PointsHistoryReadSchema]):
    pass