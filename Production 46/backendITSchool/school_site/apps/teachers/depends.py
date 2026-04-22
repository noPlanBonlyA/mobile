from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from school_site.apps.users.depends import get_user_service
from school_site.apps.users.services.users import UserServiceProtocol
from .repositories.teachers import TeacherRepositoryProtocol, TeacherRepository
from .services.teachers import TeacherServiceProtocol, TeacherService
from .services.auth import AuthAdminAndTeacherServiceProtocol, AuthService
from .use_cases.create_teacher import CreateTeacherUseCaseProtocol, CreateTeacherUseCase
from .use_cases.update_teacher import UpdateTeacherUseCaseProtocol, UpdateTeacherUseCase
from .use_cases.delete_teacher import DeleteTeacherUseCaseProtocol, DeleteTeacherUseCase
from .use_cases.get_teacher import GetTeacherUseCaseProtocol, GetTeacherUseCase
from .use_cases.list_teacher import GetListTeacherUseCaseProtocol, GetListTeacherUseCase
from .use_cases.get_me_teacher import GetMeTeacherUseCaseProtocol, GetMeTeacherUseCase


def __get_teachers_repository(
        session: AsyncSession = Depends(get_async_session)
) -> TeacherRepositoryProtocol:
    return TeacherRepository(session)


def get_teachers_services(teacher_repository: TeacherRepositoryProtocol = Depends(__get_teachers_repository),
                          user_service: UserServiceProtocol = Depends(get_user_service)) -> \
    TeacherServiceProtocol:
    return TeacherService(teacher_repository, user_service)


def get_auth_admin_and_teachers_service(auth_service: TokenServiceProtocol = Depends(get_token_service)) -> AuthAdminAndTeacherServiceProtocol:
    return AuthService(auth_service)


def get_teacher_create_use_case(auth_service: AuthAdminAndTeacherServiceProtocol = Depends(get_auth_admin_and_teachers_service),
                                teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
                                ) -> \
                                    CreateTeacherUseCaseProtocol:
    return CreateTeacherUseCase(auth_service, teacher_service)


def get_teacher_update_use_case(auth_service: AuthAdminAndTeacherServiceProtocol = Depends(get_auth_admin_and_teachers_service),
                                teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
                                ) -> \
                                    UpdateTeacherUseCaseProtocol:
    return UpdateTeacherUseCase(auth_service, teacher_service)


def get_teacher_delete_use_case(auth_service: AuthAdminAndTeacherServiceProtocol = Depends(get_auth_admin_and_teachers_service),
                                teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
                                ) -> \
                                    DeleteTeacherUseCaseProtocol:
    return DeleteTeacherUseCase(auth_service, teacher_service)


def get_teacher_get_use_case(auth_service: AuthAdminAndTeacherServiceProtocol = Depends(get_auth_admin_and_teachers_service),
                                teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
                                ) -> \
                                    GetTeacherUseCaseProtocol:
    return GetTeacherUseCase(auth_service, teacher_service)


def get_teacher_list_use_case(auth_service: AuthAdminAndTeacherServiceProtocol = Depends(get_auth_admin_and_teachers_service),
                                teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
                                ) -> \
                                    GetListTeacherUseCaseProtocol:
    return GetListTeacherUseCase(auth_service, teacher_service)


def get_teacher_get_me_use_case(auth_service: AuthAdminAndTeacherServiceProtocol = Depends(get_auth_admin_and_teachers_service),
                                teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
                                ) -> \
                                    GetMeTeacherUseCaseProtocol:
    return GetMeTeacherUseCase(auth_service, teacher_service) 