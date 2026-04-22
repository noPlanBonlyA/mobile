from fastapi import APIRouter, Depends, Response, Query
from typing import List, Optional
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
from school_site.apps.notification.use_cases.create_notification import CreateNotificationUseCaseProtocol
from school_site.apps.notification.use_cases.get_student_notification import GetStudentNotificationsUseCaseProtocol
from school_site.apps.notification.use_cases.update_read_status import UpdateReadStatusUseCaseProtocol
from school_site.apps.notification.use_cases.delete_notification import DeleteNotificationUseCaseProtocol
from school_site.apps.notification.use_cases.add_recipient import AddRecipientUseCaseProtocol


from school_site.apps.notification.depends import (
    get_create_notification_use_case,
    get_student_notifications_use_case,
    get_update_read_status_use_case,
    get_delete_notification_use_case,
    get_add_recipient_use_case
)


router = APIRouter(prefix='/api/notifications', tags=['Notifications'])


@router.post('/', response_model=NotificationWithStatusSchema, status_code=201)
async def create_notification(
    notification_data: NotificationCreateSchema,
    recipient_type: RecipientType,
    recipient_id: UUID,
    create_notification_use_case: CreateNotificationUseCaseProtocol = Depends(get_create_notification_use_case)
) -> NotificationWithStatusSchema:
    """
    Создание нового уведомления.
    
    Args:
        notification_data: Данные уведомления
        recipient_type: Тип получателя (student или group)
        recipient_id: ID получателя
        create_notification_use_case: Use case для создания уведомления
        
    Returns:
        NotificationWithStatusSchema: Созданное уведомление
    """
    return await create_notification_use_case.execute(
        notification=notification_data,
        recipient_type=recipient_type,
        recipient_id=recipient_id
    )


@router.get('/student/{student_id}', response_model=PaginationResultSchema[NotificationWithStatusSchema])
async def get_student_notifications(
    student_id: UUID,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    get_notifications_use_case: GetStudentNotificationsUseCaseProtocol = Depends(get_student_notifications_use_case)
) -> PaginationResultSchema[NotificationWithStatusSchema]:
    """
    Получение уведомлений для студента.
    
    Args:
        student_id: ID студента
        limit: Количество уведомлений на странице
        offset: Смещение для пагинации
        get_notifications_use_case: Use case для получения уведомлений
        
    Returns:
        PaginationResultSchema[NotificationWithStatusSchema]: Пагинированный список уведомлений
    """
    return await get_notifications_use_case.execute(
        student_id=student_id,
        limit=limit,
        offset=offset
    )


@router.put('/{notification_id}/read', response_model=NotificationWithStatusSchema)
async def update_read_status(
    notification_id: UUID,
    student_id: UUID,
    is_read: bool = True,
    update_status_use_case: UpdateReadStatusUseCaseProtocol = Depends(get_update_read_status_use_case)
) -> NotificationWithStatusSchema:
    """
    Обновление статуса прочтения уведомления.
    
    Args:
        notification_id: ID уведомления
        student_id: ID студента
        is_read: Статус прочтения
        update_status_use_case: Use case для обновления статуса
        
    Returns:
        NotificationWithStatusSchema: Обновленное уведомление
    """
    return await update_status_use_case.execute(
        notification_id=notification_id,
        student_id=student_id,
        is_read=is_read
    )


@router.post('/{notification_id}/recipients', response_model=NotificationRecipientReadSchema)
async def add_recipient(
    notification_id: UUID,
    recipient_data: NotificationRecipientCreateSchema,
    add_recipient_use_case: AddRecipientUseCaseProtocol = Depends(get_add_recipient_use_case)
) -> NotificationRecipientReadSchema:
    """
    Добавление получателя к уведомлению.
    
    Args:
        notification_id: ID уведомления
        recipient_data: Данные получателя
        add_recipient_use_case: Use case для добавления получателя
        
    Returns:
        NotificationRecipientReadSchema: Добавленный получатель
    """
    return await add_recipient_use_case.execute(
        notification_id=notification_id,
        recipient_data=recipient_data
    )


@router.delete('/{notification_id}', status_code=204)
async def delete_notification(
    notification_id: UUID,
    delete_notification_use_case: DeleteNotificationUseCaseProtocol = Depends(get_delete_notification_use_case)
) -> None:
    """
    Удаление уведомления.
    
    Args:
        notification_id: ID уведомления
        delete_notification_use_case: Use case для удаления уведомления
    """
    await delete_notification_use_case.execute(notification_id)
    return None