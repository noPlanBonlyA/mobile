from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session

from school_site.apps.notification.repositories.notification import (
    NotificationRepositoryProtocol,
    NotificationRepository
)
from school_site.apps.notification.services.notification import (
    NotificationServiceProtocol,
    NotificationService
)
from school_site.apps.notification.use_cases import (
    CreateNotificationUseCase,
    CreateNotificationUseCaseProtocol,
    GetStudentNotificationsUseCase,
    GetStudentNotificationsUseCaseProtocol,
    UpdateReadStatusUseCase,
    UpdateReadStatusUseCaseProtocol,
    DeleteNotificationUseCase,
    DeleteNotificationUseCaseProtocol,
    AddRecipientUseCase,
    AddRecipientUseCaseProtocol
)


def __get_notification_repository(
    session: AsyncSession = Depends(get_async_session)
) -> NotificationRepositoryProtocol:
    """
    Создает и возвращает экземпляр репозитория уведомлений.
    
    Args:
        session: Асинхронная сессия SQLAlchemy
        
    Returns:
        NotificationRepositoryProtocol: Экземпляр репозитория уведомлений
    """
    return NotificationRepository(session)


def get_notification_service(
    notification_repository: NotificationRepositoryProtocol = Depends(__get_notification_repository)
) -> NotificationServiceProtocol:
    """
    Создает и возвращает экземпляр сервиса уведомлений.
    
    Args:
        notification_repository: Репозиторий уведомлений
        
    Returns:
        NotificationServiceProtocol: Экземпляр сервиса уведомлений
    """
    return NotificationService(notification_repository)


def get_create_notification_use_case(
    notification_service: NotificationServiceProtocol = Depends(get_notification_service)
) -> CreateNotificationUseCaseProtocol:
    """
    Создает и возвращает экземпляр use case для создания уведомления.
    
    Args:
        notification_service: Сервис уведомлений
        
    Returns:
        CreateNotificationUseCaseProtocol: Экземпляр use case
    """
    return CreateNotificationUseCase(notification_service)


def get_student_notifications_use_case(
    notification_service: NotificationServiceProtocol = Depends(get_notification_service)
) -> GetStudentNotificationsUseCaseProtocol:
    """
    Создает и возвращает экземпляр use case для получения уведомлений студента.
    
    Args:
        notification_service: Сервис уведомлений
        
    Returns:
        GetStudentNotificationsUseCaseProtocol: Экземпляр use case
    """
    return GetStudentNotificationsUseCase(notification_service)


def get_update_read_status_use_case(
    notification_service: NotificationServiceProtocol = Depends(get_notification_service)
) -> UpdateReadStatusUseCaseProtocol:
    """
    Создает и возвращает экземпляр use case для обновления статуса прочтения.
    
    Args:
        notification_service: Сервис уведомлений
        
    Returns:
        UpdateReadStatusUseCaseProtocol: Экземпляр use case
    """
    return UpdateReadStatusUseCase(notification_service)


def get_delete_notification_use_case(
    notification_service: NotificationServiceProtocol = Depends(get_notification_service)
) -> DeleteNotificationUseCaseProtocol:
    """
    Создает и возвращает экземпляр use case для удаления уведомления.
    
    Args:
        notification_service: Сервис уведомлений
        
    Returns:
        DeleteNotificationUseCaseProtocol: Экземпляр use case
    """
    return DeleteNotificationUseCase(notification_service)


def get_add_recipient_use_case(
    notification_service: NotificationServiceProtocol = Depends(get_notification_service)
) -> AddRecipientUseCaseProtocol:
    """
    Создает и возвращает экземпляр use case для добавления получателя.
    
    Args:
        notification_service: Сервис уведомлений
        
    Returns:
        AddRecipientUseCaseProtocol: Экземпляр use case
    """
    return AddRecipientUseCase(notification_service)