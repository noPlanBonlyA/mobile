from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from school_site.core.schemas import (
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
)
from school_site.apps.students.schemas import StudentReadWithUserSchema
from school_site.apps.teachers.schemas import TeacherReadWithUserSchema
from school_site.apps.courses.schemas import CourseReadSimpleSchema
from datetime import date

# ====== GROUP SCHEMAS =======

class GroupBaseSchema(BaseModel):
    name: str = Field(..., description="Название группы")
    description: str = Field(..., description="Описание группы")
    start_date: date = Field(..., description="Дата начала группы")
    end_date: date = Field(..., description="Дата окончания группы")
    teacher_id: Optional[UUID] = Field(
        None, description="ID преподавателя, ответственного за группу"
    )
class GroupCreateSchema(CreateBaseModel, GroupBaseSchema):
    pass


class GroupCreateDBSchema(CreateBaseModel, GroupBaseSchema):
    pass


class GroupUpdateSchema(GroupBaseSchema):
    pass


class GroupUpdateDBSchema(UpdateBaseModel, GroupBaseSchema):
    pass


class GroupReadSchema(GroupBaseSchema, TimestampMixin):
    id: UUID


class GroupReadDBSchema(GroupBaseSchema, TimestampMixin):
    id: UUID


class GroupReadSimpleSchema(BaseModel):
    id: UUID
    name: str


class GroupReadHeadSchema(GroupReadSimpleSchema):
    pass


class GroupReadDBHeadSchema(GroupReadSimpleSchema):
    pass


class GroupPaginationResultSchema(PaginationResultSchema[GroupReadHeadSchema]):
    pass


class GroupDBPaginationResultSchema(PaginationResultSchema[GroupReadDBHeadSchema]):
    pass

class GroupWithStudentsAndTeacherAndCoursesSchema(GroupReadSchema):
    students: list[StudentReadWithUserSchema] = Field(
        default_factory=list, description="Список студентов в группе"
    )
    teacher: Optional[TeacherReadWithUserSchema] = Field(
        default_factory=None, description="Список преподавателей в группе"
    )
    courses: list[CourseReadSimpleSchema] = []

# ====== GROUP STUDENTS SCHEMAS =======


class GroupStudentsBaseSchema(BaseModel):
    students_id: list[UUID] = Field(..., description="Список ID студентов для добавления в группу")


class GroupAddStudentsSchema(GroupStudentsBaseSchema):
    pass


class GroupAddStudentsDBSchema(GroupStudentsBaseSchema):
    pass


class GroupReadStudentsSchema(GroupReadSchema, GroupStudentsBaseSchema):
    pass


class GroupReadStudentsDBSchema(GroupReadDBSchema, GroupStudentsBaseSchema):
    pass


class GroupsForStudentReadSchema(BaseModel):
    id: UUID
    group_id: UUID
    student_id: UUID
    group: GroupReadDBSchema


class GroupUpdateStudentsSchema(GroupStudentsBaseSchema):
    pass


class GroupUpdateStudentsDBSchema(GroupStudentsBaseSchema):
    pass


# ====== GROUP TEACHER SCHEMAS =======


class GroupTeacherBaseSchema(BaseModel):
    teacher_id: UUID = Field(..., description="ID преподавателя для добавления в группу")


class GroupAddTeacherSchema(GroupTeacherBaseSchema):
    pass


class GroupAddTeacherDBSchema(GroupTeacherBaseSchema):
    pass


class GroupReadTeacherSchema(GroupReadSchema, GroupTeacherBaseSchema):
    pass


class GroupReadTeacherDBSchema(GroupReadDBSchema, GroupTeacherBaseSchema):
    pass


class GroupUpdateTeacherSchema(GroupTeacherBaseSchema):
    pass


class GroupUpdateTeacherDBSchema(GroupTeacherBaseSchema):
    pass



