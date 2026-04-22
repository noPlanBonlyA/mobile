from fastapi import UploadFile
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks_files import FileHomeworkServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import FileHomeworkCreateSchema, FileHomeworkReadSchema


class CreateHomeworkFileUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, homework: FileHomeworkCreateSchema, file: UploadFile,
          access_token: str
    ) -> FileHomeworkReadSchema:
        ...


class CreateHomeworkFileUseCase(CreateHomeworkFileUseCaseProtocol):
    def __init__(
        self,
        homework_service: FileHomeworkServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.homework_service = homework_service
        self.auth_service = auth_service

    async def __call__(
        self, homework: FileHomeworkCreateSchema, file: UploadFile, access_token: str
    ) -> FileHomeworkReadSchema:
        await self.auth_service.get_student_user(access_token)
        return await self.homework_service.create(homework, file)