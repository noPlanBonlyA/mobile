from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.apps.users.depends import get_auth_service
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.apps.schedule.repositories.schedule import ScheduleRepositoryProtocol, ScheduleRepository
from school_site.apps.schedule.services.schedule import ScheduleServiceProtocol, ScheduleService
from school_site.apps.schedule.use_cases.get_schedule import GetScheduleUseCaseProtocol, GetScheduleUseCase
from school_site.apps.schedule.use_cases.get_filtered_schedule import GetFilteredScheduleUseCaseProtocol, GetFilteredScheduleUseCase

def __get_schedule_repository(
    session: AsyncSession = Depends(get_async_session)
) -> ScheduleRepositoryProtocol:
    return ScheduleRepository(session)

def __get_schedule_service(
    schedule_repository: ScheduleRepositoryProtocol = Depends(__get_schedule_repository)
) -> ScheduleServiceProtocol:
    return ScheduleService(schedule_repository)

def get_schedule_use_case(
    schedule_service: ScheduleServiceProtocol = Depends(__get_schedule_service),
    auth_service: AuthServiceProtocol = Depends(get_auth_service)
) -> GetScheduleUseCaseProtocol:
    return GetScheduleUseCase(schedule_service, auth_service)

def get_filtered_schedule_use_case(
    schedule_service: ScheduleServiceProtocol = Depends(__get_schedule_service),
    auth_service: AuthServiceProtocol = Depends(get_auth_service)
) -> GetFilteredScheduleUseCaseProtocol:
    return GetFilteredScheduleUseCase(schedule_service, auth_service)
