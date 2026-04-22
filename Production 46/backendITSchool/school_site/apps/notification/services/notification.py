import logging
from typing import Protocol, Self, List, Optional
from uuid import UUID

from school_site.apps.notification.schemas import (
    NotificationCreateSchema,
    NotificationReadSchema,
    NotificationWithStatusSchema,
    NotificationRecipientCreateSchema,
    NotificationRecipientReadSchema,
    PaginationResultSchema,
    RecipientType
)
from school_site.apps.notification.repositories.notification import NotificationRepositoryProtocol
from school_site.apps.notification.exceptions import (
    NotificationNotFoundException,
    NotificationRecipientAlreadyExistsError,
    ReadStatusAlreadyExistsError
)

logger = logging.getLogger(__name__)


class NotificationServiceProtocol(Protocol):
    async def create_notification(
        self: Self,
        notification: NotificationCreateSchema,
        recipient_type: RecipientType,
        recipient_id: UUID
    ) -> NotificationWithStatusSchema:
        ...

    async def get_student_notifications(
        self: Self,
        student_id: UUID,
        limit: int,
        offset: int = 0
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        ...

    async def update_read_status(
        self: Self,
        notification_id: UUID,
        student_id: UUID,
        is_read: bool = True
    ) -> NotificationWithStatusSchema:
        ...

    async def add_recipient(
        self: Self,
        notification_id: UUID,
        recipient_data: NotificationRecipientCreateSchema
    ) -> NotificationRecipientReadSchema:
        ...

    async def delete_notification(
        self: Self,
        notification_id: UUID
    ) -> bool:
        ...

    async def get_group_notifications(
        self: Self,
        group_id: UUID,
        limit: int = 10,
        offset: int = 0
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        ...

    async def send_notification_to_group(
        self: Self,
        notification: NotificationCreateSchema,
        group_id: UUID
    ) -> NotificationWithStatusSchema:
        ...


class NotificationService(NotificationServiceProtocol):
    def __init__(self: Self, notification_repository: NotificationRepositoryProtocol):
        self.notification_repository = notification_repository

    async def create_notification(
        self,
        notification: NotificationCreateSchema,
        recipient_type: RecipientType,
        recipient_id: UUID
    ) -> NotificationWithStatusSchema:
        # Создаем уведомление
        new_notification = await self.notification_repository.create(notification)
        
        # Создаем получателя
        recipient_data = NotificationRecipientCreateSchema(
            recipient_type=recipient_type,
            recipient_id=recipient_id
        )
        await self.notification_repository.add_recipient(
            notification_id=new_notification.id,
            recipient_data=recipient_data
        )
        
        return NotificationWithStatusSchema.model_validate(new_notification, from_attributes=True)

    async def get_student_notifications(self: Self, student_id: UUID, limit: int, offset: int = 0) -> PaginationResultSchema[NotificationWithStatusSchema]:
        logger.info(f"Fetching notifications for student: {student_id}")
        
        try:
            notifications = await self.notification_repository.get_student_notifications(
                student_id=student_id,
                limit=limit,
                offset=offset
            )
            
            logger.info(f"Successfully fetched {len(notifications.objects)} notifications")
            return notifications
        except Exception as e:
            logger.error(f"Failed to fetch notifications: {str(e)}")
            raise

    async def update_read_status(self: Self, notification_id: UUID, student_id: UUID, is_read: bool = True) -> NotificationWithStatusSchema:
        logger.info(f"Updating read status for notification: {notification_id}")
        
        try:
            # Проверяем существование уведомления
            notification = await self.notification_repository.get(notification_id)
            if notification is None:
                raise NotificationNotFoundException()

            updated_notification = await self.notification_repository.update_read_status(
                notification_id=notification_id,
                student_id=student_id,
                is_read=is_read
            )
            
            logger.info(f"Successfully updated read status for notification: {notification_id}")
            return updated_notification
        except ReadStatusAlreadyExistsError as e:
            logger.error(f"Failed to update read status: {str(e)}")
            raise
        except NotificationNotFoundException as e:
            logger.error(f"Failed to update read status: {str(e)}")
            raise

    async def add_recipient(
        self: Self,
        notification_id: UUID,
        recipient_data: NotificationRecipientCreateSchema
    ) -> NotificationRecipientReadSchema:
        logger.info(f"Adding recipient to notification: {notification_id}")
        
        try:
            # Проверяем существование уведомления
            notification = await self.notification_repository.get(notification_id)
            if notification is None:
                raise NotificationNotFoundException()

            recipient = await self.notification_repository.add_recipient(
                notification_id=notification_id,
                recipient_data=recipient_data
            )
            
            logger.info(f"Successfully added recipient to notification: {notification_id}")
            return recipient
        except NotificationRecipientAlreadyExistsError as e:
            logger.error(f"Failed to add recipient: {str(e)}")
            raise
        except NotificationNotFoundException as e:
            logger.error(f"Failed to add recipient: {str(e)}")
            raise

    async def delete_notification(self: Self, notification_id: UUID) -> bool:
        logger.info(f"Deleting notification: {notification_id}")
        
        try:
            # Проверяем существование уведомления
            notification = await self.notification_repository.get(notification_id)
            if notification is None:
                raise NotificationNotFoundException()

            await self.notification_repository.delete(notification_id)
            
            logger.info(f"Successfully deleted notification: {notification_id}")
            return True
        except NotificationNotFoundException as e:
            logger.error(f"Failed to delete notification: {str(e)}")
            raise 

    async def get_group_notifications(
        self: Self,
        group_id: UUID,
        limit: int = 10,
        offset: int = 0
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        logger.info(f"Fetching notifications for group: {group_id}")
        
        try:
            notifications = await self.notification_repository.get_group_notifications(
                group_id=group_id,
                limit=limit,
                offset=offset
            )
            
            logger.info(f"Successfully fetched {len(notifications.objects)} notifications")
            return notifications
        except Exception as e:
            logger.error(f"Failed to fetch notifications: {str(e)}")
            raise

    async def send_notification_to_group(
        self: Self,
        notification: NotificationCreateSchema,
        group_id: UUID
    ) -> NotificationWithStatusSchema:
        logger.info(f"Sending notification to group: {group_id}")
        
        try:
            # Создаем уведомление
            new_notification = await self.notification_repository.create(notification)
            
            # Добавляем группу как получателя
            recipient_data = NotificationRecipientCreateSchema(
                recipient_type=RecipientType.GROUP,
                recipient_id=group_id
            )
            await self.notification_repository.add_recipient(
                notification_id=new_notification.id,
                recipient_data=recipient_data
            )
            
            logger.info(f"Successfully sent notification to group: {group_id}")
            return NotificationWithStatusSchema.model_validate(new_notification, from_attributes=True)
        except Exception as e:
            logger.error(f"Failed to send notification to group: {str(e)}")
            raise


        