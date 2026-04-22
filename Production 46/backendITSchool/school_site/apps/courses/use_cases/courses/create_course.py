from fastapi import UploadFile
from typing import Optional
import json
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.courses import CourseServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import CourseWithPhotoReadSchema, CourseCreateSchema

class CreateCourseUseCaseProtocol(UseCaseProtocol[CourseWithPhotoReadSchema]):
    async def __call__(self, course_data: str, image: Optional[UploadFile], access_token: str) -> CourseWithPhotoReadSchema:
        ...

class CreateCourseUseCase(CreateCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.course_service = course_service
        self.auth_service = auth_service
    
    async def __call__(self, course_data: str, image: Optional[UploadFile], access_token: str) -> CourseWithPhotoReadSchema:
        await self.auth_service.get_admin_user(access_token)
        course = CourseCreateSchema(**json.loads(course_data))
        return await self.course_service.create(course, image)