from typing import Protocol, Self
from uuid import UUID

from school_site.apps.notification.schemas import (
    NotificationCreateSchema,
    NotificationWithStatusSchema,
    RecipientType
)
from school_site.apps.notification.services.notification import NotificationServiceProtocol


class CreateNotificationUseCaseProtocol(Protocol):
    async def execute(
        self: Self,
        notification: NotificationCreateSchema,
        recipient_type: RecipientType,
        recipient_id: UUID
    ) -> NotificationWithStatusSchema:
        ...


class CreateNotificationUseCase(CreateNotificationUseCaseProtocol):
    def __init__(self: Self, notification_service: NotificationServiceProtocol):
        self.notification_service = notification_service

    async def execute(
        self: Self,
        notification: NotificationCreateSchema,
        recipient_type: RecipientType,
        recipient_id: UUID
    ) -> NotificationWithStatusSchema:
        return await self.notification_service.create_notification(
            notification=notification,
            recipient_type=recipient_type,
            recipient_id=recipient_id
        )