from typing import Protocol, Self
from uuid import UUID

from school_site.apps.notification.schemas import (
    NotificationWithStatusSchema,
    PaginationResultSchema
)
from school_site.apps.notification.services.notification import NotificationServiceProtocol


class GetStudentNotificationsUseCaseProtocol(Protocol):
    async def execute(
        self: Self,
        student_id: UUID,
        limit: int,
        offset: int 
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        ...


class GetStudentNotificationsUseCase(GetStudentNotificationsUseCaseProtocol):
    def __init__(self: Self, notification_service: NotificationServiceProtocol):
        self.notification_service = notification_service

    async def execute(
        self: Self,
        student_id: UUID,
        limit: int = 10,
        offset: int = 0
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        return await self.notification_service.get_student_notifications(
            student_id=student_id,
            limit=limit,
            offset=offset
        )