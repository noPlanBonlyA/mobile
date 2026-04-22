from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from school_site.apps.students.services.students import StudentServiceProtocol
from school_site.apps.students.depends import get_students_services
from .repositories.points_history import PointsHistoryRepositoryProtocol, PointsHistoryRepository
from .services.points_history import PointsHistoryServiceProtocol, PointsHistoryService
from .services.auth import AuthAdminServiceProtocol, AuthService
from .use_cases.create_points_history_use_case import CreatePointsHistoryUseCaseProtocol, CreatePointsHistoryUseCase
from .use_cases.get_points_hystory_by_user_use_case import GetPointsHistoryByUserUseCaseProtocol, GetPointsHistoryByUserUseCase


def __get_points_history_repository(
    session: AsyncSession = Depends(get_async_session)
) -> PointsHistoryRepositoryProtocol:
    return PointsHistoryRepository(session)


def get_points_history_service(
    points_history_repository: PointsHistoryRepositoryProtocol = Depends(__get_points_history_repository),
    students_service: StudentServiceProtocol = Depends(get_students_services)
) -> PointsHistoryServiceProtocol:
    return PointsHistoryService(points_history_repository, students_service)


def get_auth_service(
    token_service: TokenServiceProtocol = Depends(get_token_service)
) -> AuthAdminServiceProtocol:
    return AuthService(token_service)


def get_create_points_history_use_case(
    points_history_service: PointsHistoryServiceProtocol = Depends(get_points_history_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> CreatePointsHistoryUseCaseProtocol:
    return CreatePointsHistoryUseCase(points_history_service, auth_service)

def get_get_points_history_by_user_use_case(
    points_history_service: PointsHistoryServiceProtocol = Depends(get_points_history_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> GetPointsHistoryByUserUseCaseProtocol:
    return GetPointsHistoryByUserUseCase(points_history_service, auth_service)