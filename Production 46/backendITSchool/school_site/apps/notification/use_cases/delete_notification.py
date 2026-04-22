from typing import Protocol, Self
from uuid import UUID

from school_site.apps.notification.services.notification import NotificationServiceProtocol


class DeleteNotificationUseCaseProtocol(Protocol):
    async def execute(self: Self, notification_id: UUID) -> bool:
        ...


class DeleteNotificationUseCase(DeleteNotificationUseCaseProtocol):
    def __init__(self: Self, notification_service: NotificationServiceProtocol):
        self.notification_service = notification_service

    async def execute(self: Self, notification_id: UUID) -> bool:
        return await self.notification_service.delete_notification(notification_id)