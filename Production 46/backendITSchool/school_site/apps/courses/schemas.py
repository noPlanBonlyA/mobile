from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from .enums import AgeCategory
from school_site.core.schemas import (
    CreateBaseModel, UpdateBaseModel, TimestampMixin, PaginationResultSchema
)
from school_site.apps.students.schemas import StudentReadWithUserSchema, StudentReadSchema

# ====== PHOTO SCHEMAS =======

class PhotoBaseSchema(BaseModel):
    name: str = Field(..., description="Название фотографии курса")
    course_id: Optional[UUID] = None

class PhotoCreateSchema(CreateBaseModel, PhotoBaseSchema):
    pass

class PhotoCreateDBSchema(CreateBaseModel, PhotoBaseSchema):
    course_id: UUID
    path: str

class PhotoUpdateSchema(PhotoBaseSchema):
    id: Optional[UUID] = None

class PhotoUpdateDBSchema(UpdateBaseModel, PhotoBaseSchema):
    course_id: UUID

class PhotoReadDBSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    path: str

    class Config:
        from_attributes = True

class PhotoReadSchema(PhotoBaseSchema, TimestampMixin):
    id: UUID
    url: HttpUrl

# --------------------------------
# ====== COURSE SCHEMAS =======

class CourseBaseSchema(BaseModel):
    name: str = Field(..., description="Название курса")
    description: str = Field(..., description="Описание курса")
    age_category: list[AgeCategory] = Field(..., description="Возрастная категория курса")
    price: Optional[int] = Field(None, ge=0, description="Цена курса, целое положительное число или null")
    author_name: Optional[str] = Field(None, description="Имя автора курса")


class CourseCreateSchema(CreateBaseModel, CourseBaseSchema):
    photo: Optional[PhotoCreateSchema] = Field(None, description="Фотография курса (опционально)")


class CourseCreateDBSchema(CreateBaseModel, CourseBaseSchema):
    pass


class CourseUpdateSchema(CourseBaseSchema):
    photo: Optional[PhotoUpdateSchema] = None


class CourseUpdateDBSchema(CourseBaseSchema, UpdateBaseModel):
    pass


class CourseReadSchema(CourseBaseSchema, TimestampMixin):
    id: UUID


class CourseReadDBSchema(CourseBaseSchema, TimestampMixin):
    id: UUID


class CourseWithPhotoReadDBSchema(CourseBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadDBSchema] = None


class CourseWithPhotoReadSchema(CourseBaseSchema, TimestampMixin):
    id: UUID
    photo: Optional[PhotoReadSchema] = None


class CourseWithPhotoPaginationResultDBSchema(PaginationResultSchema[CourseWithPhotoReadDBSchema]):
    pass


class CourseWithPhotoPaginationResultSchema(PaginationResultSchema[CourseWithPhotoReadSchema]):
    pass


class CourseReadSimpleSchema(BaseModel):
    id: UUID
    name: str


class CourseReadHeadSchema(CourseReadSimpleSchema):
    pass


class CourseReadDBHeadSchema(CourseReadSimpleSchema):
    pass


class CoursePaginationResultSchema(PaginationResultSchema[CourseReadHeadSchema]):
    pass


class CourseDBPaginationResultSchema(PaginationResultSchema[CourseReadDBHeadSchema]):
    pass

# ====== MATERIAL SCHEMAS =======
class MaterialDataSchema(BaseModel):
    name: str



# ====== LESSON SCHEMAS =======

class LessonBaseSchema(BaseModel):
    name: str
    teacher_material_id: Optional[UUID] = Field(None, description="ID материала для учителя")
    teacher_additional_material_id: Optional[UUID] = Field(None, description="ID дополнительного материала для учителя")
    student_material_id: Optional[UUID]  = Field(None, description="ID материала для студента")
    student_additional_material_id: Optional[UUID] = Field(None, description="ID дополнительного материала для студента")
    homework_id: Optional[UUID]  = Field(None, description="ID домашнего задания")
    homework_additional_id: Optional[UUID] = Field(None, description="ID дополнительного домашнего задания")


class LessonCreateSchema(CreateBaseModel, LessonBaseSchema):
    pass


class LessonCreateDBSchema(CreateBaseModel, LessonBaseSchema):
    course_id: UUID


class LessonUpdateSchema(LessonBaseSchema):
    pass


class LessonUpdateDBSchema(UpdateBaseModel, LessonBaseSchema):
    course_id: UUID


class LessonReadSchema(LessonBaseSchema, TimestampMixin):
    id: UUID
    course_id: UUID


class LessonReadDBSchema(LessonReadSchema):
    pass


class LessonReadSimpleSchema(BaseModel):
    id: UUID
    name: str
    course_id: UUID


class LessonReadHeadSchema(LessonReadSimpleSchema):
    pass


class LessonReadDBHeadSchema(LessonReadSimpleSchema):
    pass


class LessonPaginationResultSchema(PaginationResultSchema[LessonReadHeadSchema]):
    pass


class LessonPaginationResultDBSchema(PaginationResultSchema[LessonReadDBHeadSchema]):
    pass


class LessonWithMaterialsBaseSchema(BaseModel):
    name: str
    teacher_material_name: Optional[str] = None
    teacher_material_text: Optional[str] = None
    teacher_additional_material_name: Optional[str] = None
    student_material_name: Optional[str] = None
    student_material_text: Optional[str] = None
    student_additional_material_name: Optional[str] = None
    homework_material_name: Optional[str] = None
    homework_material_text: Optional[str] = None
    homework_additional_material_name: Optional[str] = None


class LessonWithMaterialsCreateSchema(CreateBaseModel, LessonWithMaterialsBaseSchema):
    pass

class LessonWithMaterialsUpdateSchema(CreateBaseModel, LessonWithMaterialsBaseSchema):
    teacher_material_id: Optional[UUID] = None
    teacher_additional_material_id: Optional[UUID] = None
    student_material_id: Optional[UUID] = None
    student_additional_material_id: Optional[UUID] = None
    homework_id: Optional[UUID] = None
    homework_additional_id: Optional[UUID] = None


class LessonWithMaterialsDeleteSchema(BaseModel):
    teacher_material_id: Optional[UUID] = None
    teacher_additional_material_id: Optional[UUID] = None
    student_material_id: Optional[UUID] = None 
    student_additional_material_id: Optional[UUID] = None
    homework_id: Optional[UUID] = None
    homework_additional_id: Optional[UUID] = None

class LessonWithMaterialsTextBaseSchema(BaseModel):
    name: str
    teacher_material_text: Optional[str] = None
    teacher_material_name: Optional[str] = None
    student_material_text: Optional[str]  = None
    student_material_name: Optional[str] = None
    homework_material_text: Optional[str] = None
    homework_material_name: Optional[str] = None

class LessonWithMaterialsTextCreateSchema(CreateBaseModel, LessonWithMaterialsTextBaseSchema):
    pass

class LessonWithMaterialsTextUpdateSchema(CreateBaseModel, LessonWithMaterialsTextBaseSchema):
    teacher_material_id: Optional[UUID] = None
    student_material_id: Optional[UUID] = None
    homework_id: Optional[UUID] = None


class LessonWithMaterialsReadSchema(LessonReadSchema, LessonBaseSchema):
    teacher_material_url: Optional[HttpUrl] = None
    teacher_additional_material_url: Optional[HttpUrl] = None
    student_material_url: Optional[HttpUrl] = None
    student_additional_material_url: Optional[HttpUrl] = None
    homework_material_url: Optional[HttpUrl] = None
    homework_additional_material_url: Optional[HttpUrl] = None

class LessonShortSchema(BaseModel):
    id: UUID
    name: str

class LessonStudentSchema(BaseModel):
    is_visited: bool
    is_excused_absence: bool
    is_compensated_skip: bool
    is_sent_homework: bool
    is_graded_homework: bool
    coins_for_visit: Optional[int] = None
    grade_for_visit: Optional[int] = None
    coins_for_homework: Optional[int] = None
    grade_for_homework: Optional[int] = None


# ====== LESSON HTML FILES SCHEMAS =======

class LessonHTMLBaseSchema(BaseModel):
    name: str

class LessonHTMLCreateSchema(CreateBaseModel, LessonHTMLBaseSchema):
    file: UploadFile

class LessonHTMLTextCreateSchema(CreateBaseModel, LessonHTMLBaseSchema):
    html_text: str

class LessonHTMLCreateDBSchema(CreateBaseModel, LessonHTMLBaseSchema):
    path: str

class LessonHTMLUpdateSchema(CreateBaseModel, LessonHTMLBaseSchema):
    file: UploadFile

class LessonHTMLTextUpdateSchema(CreateBaseModel, LessonHTMLBaseSchema):
    html_text: str

class LessonHTMLUpdateDBSchema(UpdateBaseModel, LessonHTMLBaseSchema):
    pass


class LessonHTMLReadSchema(LessonHTMLBaseSchema, TimestampMixin):
    id: UUID
    url: HttpUrl

class LessonHTMLReadDBSchema(LessonHTMLBaseSchema, TimestampMixin):
    id: UUID
    path: str

    class Config:
        from_attributes = True


# ====== FILE HOMEWORKS SCHEMAS =======
class FileHomeworkBaseSchema(BaseModel):
    name: str

class FileHomeworkCreateSchema(CreateBaseModel, FileHomeworkBaseSchema):
    text: Optional[str] = None

class FileHomeworkCreateDBSchema(CreateBaseModel, FileHomeworkBaseSchema):
    path: str

class FileHomeworkUpdateSchema(CreateBaseModel, FileHomeworkBaseSchema):
    text: Optional[str] = None


class FileHomeworkUpdateDBSchema(UpdateBaseModel, FileHomeworkBaseSchema):
    pass

class FileHomeworkReadDBSchema(FileHomeworkBaseSchema, TimestampMixin):
    id: UUID
    path: str

    class Config:
        from_attributes = True

class FileHomeworkReadSchema(FileHomeworkBaseSchema, TimestampMixin):
    id: UUID
    url: Optional[HttpUrl]
    
# ====== HOMEWORKS SCHEMAS =======

class HomeworkBaseSchema(BaseModel):
    file_id: UUID


class HomeworkCreateSchema(CreateBaseModel, HomeworkBaseSchema):
    pass


class HomeworkUpdateSchema(CreateBaseModel, HomeworkBaseSchema):
    pass


class HomeworkUpdateDBSchema(UpdateBaseModel, HomeworkBaseSchema):
    pass


class HomeworkReadDBSchema(HomeworkBaseSchema):
    id: UUID

class HomeworkReadWithFileDBSchema(HomeworkBaseSchema):
    id: UUID
    file: FileHomeworkReadDBSchema

class HomeworkReadSchema(HomeworkBaseSchema):
    id: UUID
    file_id: UUID
    homework: FileHomeworkReadSchema


class LessonWithHomeworkReadSchema(LessonReadSchema):
    homework: LessonHTMLReadSchema

# ====== LESSON GROUP SCHEMAS =======

class LessonGroupBaseSchema(BaseModel):
    lesson_id: UUID
    group_id: UUID
    start_datetime: datetime
    end_datetime: datetime
    is_opened: bool = False
    auditorium: str


class LessonGroupCreateSchema(CreateBaseModel, LessonGroupBaseSchema):
    pass


class LessonGroupUpdateSchema(CreateBaseModel, LessonGroupBaseSchema):
    pass

class LessonGroupUpdateDBSchema(UpdateBaseModel, LessonGroupBaseSchema):
    pass


class LessonGroupReadSchema(LessonGroupBaseSchema):
    id: UUID

    class Config:
        from_attributes = True

class LessonGroupReadWithLessonSchema(LessonGroupBaseSchema):
    id: UUID
    lesson: LessonReadDBSchema

    class Config:
        from_attributes = True

# ====== LESSON STUDENT SCHEMAS =======

class LessonStudentBaseSchema(BaseModel):
    student_id: UUID
    lesson_group_id: UUID
    is_visited: Optional[bool] = None
    is_excused_absence: Optional[bool] = None
    is_compensated_skip: Optional[bool] = None
    is_sent_homework: Optional[bool] = None
    is_graded_homework: Optional[bool] = None
    coins_for_visit: Optional[int] = None
    grade_for_visit: Optional[int] = None
    coins_for_homework: Optional[int] = None
    grade_for_homework: Optional[int] = None


class LessonStudentCreateSchema(CreateBaseModel, LessonStudentBaseSchema):
    pass


class LessonStudentUpdateSchema(CreateBaseModel, LessonStudentBaseSchema):
    pass

class LessonStudentUpdateDBSchema(UpdateBaseModel, LessonStudentBaseSchema):
    pass


class LessonStudentReadSchema(LessonStudentBaseSchema):
    id: UUID

    class Config:
        from_attributes = True

class LessonStudentWithLessonGroupReadSchema(LessonStudentReadSchema):
    lesson_group: LessonGroupReadSchema

class LessonStudentReadWithStudentDBSchema(LessonStudentReadSchema):
    student: StudentReadSchema

    class Config:
        from_attributes = True

class LessonStudentReadWithStudentSchema(LessonStudentBaseSchema):
    id: UUID
    student: StudentReadWithUserSchema

    class Config:
        from_attributes = True

# ====== LESSON STUDENT HOMEWORK SCHEMAS =======

class LessonStudentHomeworkBaseSchema(BaseModel):
    lesson_student_id: UUID
    homework_id: UUID
    student_comment_id: Optional[UUID] = None

class LessonStudentHomeworkCreateSchema(CreateBaseModel, LessonStudentHomeworkBaseSchema):
    pass

class LessonStudentHomeworkUpdateDBSchema(UpdateBaseModel, LessonStudentHomeworkBaseSchema):
    pass

class LessonStudentHomeworkUpdateSchema(CreateBaseModel, LessonStudentHomeworkBaseSchema):
    pass

class LessonStudentHomeworkReadSchema(LessonStudentHomeworkBaseSchema):
    pass

# ====== ADD HOMEWORK SCHEMAS =======

class AddHomeworkReadSchema(BaseModel):
    lesson_id: UUID
    homework: FileHomeworkReadSchema
    lesson_student_homework: LessonStudentHomeworkReadSchema
    student_comment: Optional[str] = None


# ====== COMENTS SCHEMAS =======

class CommentBaseSchema(BaseModel):
    text: str
    lesson_student_id: UUID

class CommentCreateSchema(CreateBaseModel, CommentBaseSchema):
    pass

class CommentCreateDBSchema(CreateBaseModel, CommentBaseSchema):
    teacher_id: UUID

class CommentUpdateSchema(CreateBaseModel, CommentBaseSchema):
    pass

class CommentUpdateDBSchema(UpdateBaseModel, CommentBaseSchema):
    teacher_id: UUID

class CommentReadSchema(CommentBaseSchema, TimestampMixin):
    id: UUID
    teacher_id: UUID


    class Config:
        from_attributes = True


# ====== COMENTS STUDENTS SCHEMAS =======
class CommentStudentBaseSchema(BaseModel):
    text: Optional[str] = None
    lesson_student_id: UUID
    student_id: UUID


class CommentStudentCreateSchema(CreateBaseModel, CommentStudentBaseSchema):
    pass

class CommentStudentCreateDBSchema(CreateBaseModel, CommentStudentBaseSchema):
    pass

class CommentStudentUpdateSchema(CreateBaseModel, CommentStudentBaseSchema):
    pass

class CommentStudentUpdateDBSchema(UpdateBaseModel, CommentStudentBaseSchema):
    pass

class CommentStudentReadSchema(CommentStudentBaseSchema, TimestampMixin):
    id: UUID

    class Config:
        from_attributes = True

class LessonSimpleReadSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class LessonStudentDetailReadDBSchema(LessonStudentReadSchema):
    passed_homeworks: Optional[List[HomeworkReadWithFileDBSchema]] = None
    comments: Optional[List[CommentReadSchema]] = None
    comments_students: Optional[List[CommentStudentReadSchema]] = None

    class Config:
        from_attributes = True

class LessonGroupDetailDBBaseSchema(LessonGroupBaseSchema):
    students: Optional[List[LessonStudentDetailReadDBSchema]] = None

    class Config:
        from_attributes = True

class LessonDetailReadDBSchema(BaseModel):
    id: UUID
    name: str
    course_id: UUID
    homework: Optional[LessonHTMLReadDBSchema] = None
    homework_additional_material: Optional[LessonHTMLReadDBSchema] = None
    groups: List[LessonGroupDetailDBBaseSchema] = []

    class Config:
        from_attributes = True

class LessonStudentMaterialDetailReadDBSchema(LessonDetailReadDBSchema):
    student_material: Optional[LessonHTMLReadDBSchema] = None
    student_additional_material: Optional[LessonHTMLReadDBSchema] = None

    class Config:
        from_attributes = True

class LessonTeacherMaterialDetailReadDBSchema(LessonDetailReadDBSchema):
    teacher_material: Optional[LessonHTMLReadDBSchema] = None
    teacher_additional_material: Optional[LessonHTMLReadDBSchema] = None
    
    class Config:
        from_attributes = True


class LessonStudentDetailReadSchema(LessonStudentReadSchema):
    passed_homeworks: Optional[List[HomeworkReadSchema]] = None
    comments: Optional[List[CommentReadSchema]] = None
    comments_students: Optional[List[CommentStudentReadSchema]] = None
    
    class Config:
        from_attributes = True

class LessonGroupDetailBaseSchema(LessonGroupBaseSchema):
    students: Optional[List[LessonStudentDetailReadSchema]] = None

    class Config:
        from_attributes = True

class LessonDetailReadSchema(BaseModel):
    id: UUID
    name: str
    course_id: UUID
    homework: Optional[LessonHTMLReadSchema] = None
    homework_additional_material: Optional[LessonHTMLReadSchema] = None
    groups: List[LessonGroupDetailBaseSchema] = []

    class Config:
        from_attributes = True

class LessonStudentMaterialDetailReadSchema(LessonDetailReadSchema):
    student_material: Optional[LessonHTMLReadSchema] = None
    student_additional_material: Optional[LessonHTMLReadSchema] = None
    class Config:
        from_attributes = True

class LessonTeacherMaterialDetailReadSchema(LessonDetailReadSchema):
    teacher_material: Optional[LessonHTMLReadSchema] = None
    
    class Config:
        from_attributes = True


class LessonInfoTeacherReadDBSchema(BaseModel):
    id: UUID
    name: str
    course_id: UUID
    homework: Optional[LessonHTMLReadDBSchema] = None
    homework_additional_material: Optional[LessonHTMLReadDBSchema] = None
    teacher_material: Optional[LessonHTMLReadDBSchema] = None
    teacher_additional_material: Optional[LessonHTMLReadDBSchema] = None

    class Config:
        from_attributes = True

class LessonInfoTeacherReadSchema(BaseModel):
    id: UUID
    name: str
    course_id: UUID
    homework: Optional[LessonHTMLReadSchema] = None
    homework_additional_material: Optional[LessonHTMLReadSchema] = None
    teacher_material: Optional[LessonHTMLReadSchema] = None
    teacher_additional_material: Optional[LessonHTMLReadSchema] = None


# ====== COURSE STUDENTS SCHEMAS =======

class CourseStudentBaseSchema(BaseModel):
    student_id: UUID
    course_id: UUID
    progress: float = 0.0

class CourseStudentCreateSchema(CreateBaseModel, CourseStudentBaseSchema):
    pass

class CourseStudentUpdateSchema(CreateBaseModel, CourseStudentBaseSchema):
    pass

class CourseStudentUpdateDBSchema(UpdateBaseModel, CourseStudentBaseSchema):
    pass

class CourseStudentReadSchema(CourseStudentBaseSchema):
    id: UUID


class CourseStudentWithCoursesDBSchema(CourseStudentReadSchema):
    course: CourseWithPhotoReadDBSchema

    class Config:
        from_attributes = True

class CourseStudentWithCoursesSchema(CourseStudentReadSchema):
    course: CourseWithPhotoReadSchema

    class Config:
        from_attributes = True