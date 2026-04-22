from uuid import uuid4
from sqlalchemy import Column, String, Integer, Enum, CheckConstraint, ForeignKey, DateTime, Boolean, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PostgresUUID
from school_site.core.db import Base
from sqlalchemy.orm import relationship
from school_site.core.models import TimestampMixin, FileMixin
from .enums import AgeCategory


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    age_category = Column(ARRAY(Enum(AgeCategory)), nullable=False)
    price = Column(Integer, nullable=True)
    author_name = Column(String, nullable=True)
    lessons = relationship("Lesson", back_populates="course")
    students = relationship("CourseStudent", back_populates="course")
    photo = relationship("PhotoCourse", back_populates="course", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("price IS NULL OR price >= 0", name="positive_price_check"),
    )


class PhotoCourse(Base, TimestampMixin, FileMixin):
    __tablename__ = "photo_courses"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(PostgresUUID(as_uuid=True), ForeignKey("courses.id"), unique=True)
    course = relationship("Course", back_populates="photo")


class Homework(Base, TimestampMixin):
    __tablename__ = "homeworks"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(PostgresUUID(as_uuid=True), ForeignKey("file_homeworks.id"))
    file = relationship("FileHomework", back_populates="homework")
    students = relationship("LessonStudent", secondary="lesson_student_homework", back_populates="passed_homeworks")


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String, nullable=False)
    lesson_student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_students.id"))
    teacher_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("teachers.id", ondelete="CASCADE"), 
        nullable=False
    )
    lesson_student = relationship("LessonStudent", back_populates="comments")
    teacher = relationship("Teacher", back_populates="comments")


class CommentStudent(Base, TimestampMixin):
    __tablename__ = "comments_students"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String, nullable=False)
    lesson_student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_students.id"))
    student_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("students.id", ondelete="CASCADE"), 
        nullable=False
    )
    lesson_student = relationship("LessonStudent", back_populates="comments_students")
    student = relationship("Student", back_populates="comments_students")


class Lesson(Base, TimestampMixin):
    __tablename__ = "lessons"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(PostgresUUID(as_uuid=True), ForeignKey("courses.id"))
    name = Column(String, nullable=False)
    teacher_material_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"), nullable=True)
    teacher_additional_material_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"), nullable=True)
    student_material_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"), nullable=True)
    student_additional_material_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"), nullable=True)
    homework_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"), nullable=True)
    homework_additional_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_html_files.id"), nullable=True)

    course = relationship("Course", back_populates="lessons")
    groups = relationship("LessonGroup", back_populates="lesson")
    teacher_material = relationship("LessonHtmlFile", foreign_keys=[teacher_material_id])
    teacher_additional_material = relationship("LessonHtmlFile", foreign_keys=[teacher_additional_material_id])
    student_material = relationship("LessonHtmlFile", foreign_keys=[student_material_id])
    student_additional_material = relationship("LessonHtmlFile", foreign_keys=[student_additional_material_id])
    homework = relationship("LessonHtmlFile", foreign_keys=[homework_id])
    homework_additional_material = relationship("LessonHtmlFile", foreign_keys=[homework_additional_id])


class LessonHtmlFile(Base, TimestampMixin, FileMixin):
    __tablename__ = "lesson_html_files"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)


class FileHomework(Base, TimestampMixin, FileMixin):
    __tablename__ = "file_homeworks"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    homework = relationship("Homework", back_populates="file")


class LessonGroup(Base):
    __tablename__ = "lesson_groups"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    lesson_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"))
    group_id = Column(PostgresUUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"))
    start_datetime = Column(DateTime, nullable=False)  
    end_datetime = Column(DateTime, nullable=False)   
    is_opened = Column(Boolean, default=False)
    auditorium = Column(String, nullable=True)

    lesson = relationship("Lesson", back_populates="groups")
    group = relationship("Group", back_populates="lessons")
    students = relationship(
        "LessonStudent", 
        back_populates="lesson_group",
        cascade="all, delete"  
    )  
    __table_args__ = (
        UniqueConstraint('lesson_id', 'group_id', name='unique_lesson_group'),
    )


class LessonStudent(Base):
    __tablename__ = "lesson_students"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = Column(PostgresUUID(as_uuid=True), ForeignKey("students.id"))
    lesson_group_id = Column(PostgresUUID(as_uuid=True), ForeignKey("lesson_groups.id"))
    is_visited = Column(Boolean, nullable=True)
    is_excused_absence = Column(Boolean, nullable=True)
    is_compensated_skip = Column(Boolean, nullable=True)
    is_sent_homework = Column(Boolean, nullable=True)
    is_graded_homework = Column(Boolean, nullable=True)
    coins_for_visit = Column(Integer, nullable=True)
    grade_for_visit = Column(Integer, nullable=True)
    coins_for_homework = Column(Integer, nullable=True)
    grade_for_homework = Column(Integer, nullable=True)
    
    student = relationship("Student", back_populates="lessons")
    lesson_group = relationship("LessonGroup", back_populates="students")
    passed_homeworks = relationship("Homework", secondary="lesson_student_homework", back_populates="students")
    comments = relationship("Comment", back_populates="lesson_student")
    comments_students = relationship("CommentStudent", back_populates="lesson_student")

    __table_args__ = (
        UniqueConstraint('student_id', 'lesson_group_id', name='unique_student_lesson_group'),
    )


class LessonStudentHomework(Base):
    __tablename__ = "lesson_student_homework"

    lesson_student_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("lesson_students.id", ondelete="CASCADE"),  # Добавить каскадное удаление
        primary_key=True
    )
    homework_id = Column(
        PostgresUUID(as_uuid=True), 
        ForeignKey("homeworks.id", ondelete="CASCADE"),  # И здесь тоже
        primary_key=True
    )
    student_comment_id = Column(PostgresUUID(as_uuid=True), ForeignKey("comments_students.id", ondelete="SET NULL"), nullable=True)

class CourseStudent(Base):
    __tablename__ = "course_students"
    
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id = Column(
    PostgresUUID(as_uuid=True),
    ForeignKey("students.id", ondelete="CASCADE")
)

    course_id = Column(PostgresUUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"))
    progress = Column(Float, default=0.0)
    
    student = relationship("Student", back_populates="courses")
    course = relationship("Course", back_populates="students")


__all__ = [
    "Course", "PhotoCourse", "Homework", "Comment", "Lesson",
    "LessonHtmlFile", "FileHomework", "LessonGroup", "LessonStudent",
    "LessonStudentHomework", "CourseStudent"
]
