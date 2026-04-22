from typing import List
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.courses import CourseServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from school_site.apps.courses.schemas import CourseWithPhotoReadSchema

class GetCoursesForTeacherUseCaseProtocol(UseCaseProtocol[List[CourseWithPhotoReadSchema]]):
    async def __call__(self, access_token: str) -> List[CourseWithPhotoReadSchema]:
        ...

class GetCoursesForTeacherUseCase(GetCoursesForTeacherUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol, auth_service: AuthAdminServiceProtocol,
                 teacher_service: TeacherServiceProtocol):
        self.teacher_service = teacher_service
        self.course_service = course_service
        self.auth_service = auth_service
    
    async def __call__(self, access_token: str) -> List[CourseWithPhotoReadSchema]:
        teacher_data = await self.auth_service.get_teacher_user(access_token)
        db_teacher = await self.teacher_service.get_by_user_id(teacher_data.user_id)
        return await self.course_service.get_courses_by_teacher_id(db_teacher.id)