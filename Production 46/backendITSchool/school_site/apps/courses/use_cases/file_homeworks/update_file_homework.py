from uuid import UUID
from fastapi import UploadFile
from typing import Optional
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks_files import FileHomeworkServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import FileHomeworkUpdateSchema, FileHomeworkReadSchema


class UpdateHomeworkUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, homework_id: UUID, homework: FileHomeworkUpdateSchema, file: Optional[UploadFile],
          access_token: str
    ) -> FileHomeworkReadSchema:
        ...


class UpdateHomeworkUseCase(UpdateHomeworkUseCaseProtocol):
    def __init__(
        self,
        homework_service: FileHomeworkServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.homework_service = homework_service
        self.auth_service = auth_service

    async def __call__(
        self, homework_id: UUID, homework: FileHomeworkUpdateSchema, file: Optional[UploadFile], access_token: str
    ) -> FileHomeworkReadSchema:
        await self.auth_service.get_student_user(access_token)
        return await self.homework_service.update(homework_id, homework, file)