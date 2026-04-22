from typing import List
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.course_student import GetCoursesByStudentServiceProtocol
from school_site.apps.students.services.students import StudentServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import CourseStudentWithCoursesSchema

class GetCoursesForStudentUseCaseProtocol(UseCaseProtocol[List[CourseStudentWithCoursesSchema]]):
    async def __call__(self, access_token: str) -> List[CourseStudentWithCoursesSchema]:
        ...

class GetCoursesForStudentUseCase(GetCoursesForStudentUseCaseProtocol):
    def __init__(self, course_student_service: GetCoursesByStudentServiceProtocol, auth_service: AuthAdminServiceProtocol,
                 student_service: StudentServiceProtocol):
        self.student_service = student_service
        self.course_student_service = course_student_service
        self.auth_service = auth_service
    
    async def __call__(self, access_token: str) -> List[CourseStudentWithCoursesSchema]:
        student_data = await self.auth_service.get_student_user(access_token)
        db_student = await self.student_service.get_by_user_id(student_data.user_id)
        return await self.course_student_service.get_courses_by_student_id(db_student.id)