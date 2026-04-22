from typing import Protocol, Self
from uuid import UUID

from school_site.apps.notification.schemas import NotificationWithStatusSchema
from school_site.apps.notification.services.notification import NotificationServiceProtocol


class UpdateReadStatusUseCaseProtocol(Protocol):
    async def execute(
        self: Self,
        notification_id: UUID,
        student_id: UUID,
        is_read: bool
    ) -> NotificationWithStatusSchema:
        ...


class UpdateReadStatusUseCase(UpdateReadStatusUseCaseProtocol):
    def __init__(self: Self, notification_service: NotificationServiceProtocol):
        self.notification_service = notification_service

    async def execute(
        self: Self,
        notification_id: UUID,
        student_id: UUID,
        is_read: bool = True
    ) -> NotificationWithStatusSchema:
        return await self.notification_service.update_read_status(
            notification_id=notification_id,
            student_id=student_id,
            is_read=is_read
        )