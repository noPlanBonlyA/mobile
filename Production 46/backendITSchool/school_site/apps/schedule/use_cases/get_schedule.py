from typing import Protocol, Self
from school_site.core.enums import UserRole
from ..schemas import AllScheduleReadSchema
from ..services.schedule import ScheduleServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol

class GetScheduleUseCaseProtocol(Protocol):
    async def __call__(self: Self, access_token: str) -> AllScheduleReadSchema:
        ...

class GetScheduleUseCase(GetScheduleUseCaseProtocol):
    def __init__(self: Self, schedule_service: ScheduleServiceProtocol, auth_service: AuthServiceProtocol):
        self.schedule_service = schedule_service
        self.auth_service = auth_service

    async def __call__(self: Self, access_token: str) -> AllScheduleReadSchema:
        token_data = await self.auth_service.decode_acess_token(access_token)
        if token_data.role == UserRole.STUDENT:
            return await self.schedule_service.get_student_schedule(token_data.user_id)
        elif token_data.role == UserRole.TEACHER:
            return await self.schedule_service.get_teacher_schedule(token_data.user_id)
        else:
            return await self.schedule_service.get_all_groups_schedule() 