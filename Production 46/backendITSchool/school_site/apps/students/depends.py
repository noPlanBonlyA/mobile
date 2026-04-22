from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from school_site.apps.users.depends import get_user_service
from school_site.apps.users.services.users import UserServiceProtocol
from .repositories.students import StudentRepositoryProtocol, StudentRepository
from .services.students import StudentServiceProtocol, StudentService, StudentsByGroupServiceProtocol, StudentsByGroupService
from .services.auth import AuthAdminAndStudentServiceProtocol, AuthService
from .use_cases.create_student import CreateStudentUseCaseProtocol, CreateStudentUseCase
from .use_cases.update_student import UpdateStudentUseCaseProtocol, UpdateStudentUseCase
from .use_cases.delete_student import DeleteStudentUseCaseProtocol, DeleteStudentUseCase
from .use_cases.get_student import GetStudentUseCaseProtocol, GetStudentUseCase 
from .use_cases.list_student import GetListStudentUseCaseProtocol, GetListStudentUseCase
from .use_cases.get_me_student import GetMeStudentUseCaseProtocol, GetMeStudentUseCase


def __get_students_repository(
        session: AsyncSession = Depends(get_async_session)
) -> StudentRepositoryProtocol:
    return StudentRepository(session)


def get_students_services(student_repository: StudentRepositoryProtocol = Depends(__get_students_repository),
                          user_service: UserServiceProtocol = Depends(get_user_service)) -> \
    StudentServiceProtocol:
    return StudentService(student_repository, user_service)


def get_auth_admin_and_students_service(auth_service: TokenServiceProtocol = Depends(get_token_service)) -> AuthAdminAndStudentServiceProtocol:
    return AuthService(auth_service)

def get_student_by_group_service(student_repository:StudentRepositoryProtocol = Depends(__get_students_repository)) -> StudentsByGroupServiceProtocol:
    return StudentsByGroupService(student_repository)

def get_student_create_use_case(auth_service: AuthAdminAndStudentServiceProtocol = Depends(get_auth_admin_and_students_service),
                                student_service: StudentServiceProtocol = Depends(get_students_services),
                                ) -> \
                                    CreateStudentUseCaseProtocol:
    return CreateStudentUseCase(auth_service, student_service)


def get_student_update_use_case(auth_service: AuthAdminAndStudentServiceProtocol = Depends(get_auth_admin_and_students_service),
                                student_service: StudentServiceProtocol = Depends(get_students_services),
                                ) -> \
                                    UpdateStudentUseCaseProtocol:
    return UpdateStudentUseCase(auth_service, student_service)


def get_student_delete_use_case(auth_service: AuthAdminAndStudentServiceProtocol = Depends(get_auth_admin_and_students_service),
                                student_service: StudentServiceProtocol = Depends(get_students_services),
                                ) -> \
                                    DeleteStudentUseCaseProtocol:
    return DeleteStudentUseCase(auth_service, student_service)


def get_student_get_use_case(auth_service: AuthAdminAndStudentServiceProtocol = Depends(get_auth_admin_and_students_service),
                                student_service: StudentServiceProtocol = Depends(get_students_services),
                                ) -> \
                                    GetStudentUseCaseProtocol:
    return GetStudentUseCase(auth_service, student_service)


def get_student_list_use_case(auth_service: AuthAdminAndStudentServiceProtocol = Depends(get_auth_admin_and_students_service),
                                student_service: StudentServiceProtocol = Depends(get_students_services),
                                ) -> \
                                    GetListStudentUseCaseProtocol:
    return GetListStudentUseCase(auth_service, student_service)


def get_student_get_me_use_case(auth_service: AuthAdminAndStudentServiceProtocol = Depends(get_auth_admin_and_students_service),
                                student_service: StudentServiceProtocol = Depends(get_students_services),
                                ) -> \
                                    GetMeStudentUseCaseProtocol:
    return GetMeStudentUseCase(auth_service, student_service)