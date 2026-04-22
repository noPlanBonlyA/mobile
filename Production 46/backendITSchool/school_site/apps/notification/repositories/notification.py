from typing import Self
from uuid import UUID

from school_site.apps.students.models import Student
from school_site.apps.groups.models import Group

from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Notification, NotificationRecipients, ReadStatus
from school_site.apps.notification.schemas import (
    NotificationCreateSchema,
    NotificationUpdateSchema,
    NotificationWithStatusSchema,
    NotificationRecipientCreateSchema,
    NotificationRecipientReadSchema,
    NotificationReadSchema,
    PaginationResultSchema,
    RecipientType
)
import sqlalchemy as sa
from datetime import datetime
from school_site.apps.notification.exceptions import (
    NotificationNotFoundException,
    NotificationRecipientAlreadyExistsError,
    ReadStatusAlreadyExistsError
)


class NotificationRepositoryProtocol(BaseRepositoryImpl[Notification, NotificationReadSchema, NotificationCreateSchema, NotificationUpdateSchema]):
    async def get_student_notifications(
        self: Self,
        student_id: UUID,
        limit: int,
        offset: int
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        ...

    async def update_read_status(
        self: Self,
        notification_id: UUID,
        student_id: UUID,
        is_read: bool
    ) -> NotificationWithStatusSchema:
        ...

    async def add_recipient(
        self: Self,
        notification_id: UUID,
        recipient_data: NotificationRecipientCreateSchema
    ) -> NotificationRecipientReadSchema:
        ...


class NotificationRepository(NotificationRepositoryProtocol):
    async def create(self, create_object: NotificationCreateSchema) -> NotificationReadSchema:
        async with self.session as session:
            stmt = (
                sa.insert(self.model_type)
                .values(**create_object.model_dump(exclude={'id'}))
                .returning(self.model_type)
            )
            model = (await session.execute(stmt)).scalar_one()
            await session.commit()
            return NotificationReadSchema.model_validate(model, from_attributes=True)
    
    async def get_student_notifications(
        self: Self,
        student_id: UUID,
        limit: int = 10,
        offset: int = 0
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        async with self.session as session:
            # Подзапрос для получения group_id студента
            group_subquery = (
                sa.select(Group.id)
                .join(Student.groups)
                .where(Student.id == student_id)
            )

            # Запрос для подсчета общего количества уведомлений
            count_query = sa.select(sa.func.count(self.model_type.id)).join(NotificationRecipients).where(
                sa.or_(
                    sa.and_(
                        NotificationRecipients.recipient_type == RecipientType.STUDENT,
                        NotificationRecipients.recipient_id == student_id
                    ),
                    sa.and_(
                        NotificationRecipients.recipient_type == RecipientType.GROUP,
                        NotificationRecipients.recipient_id.in_(group_subquery)
                    )
                )
            )
            total_count = (await session.execute(count_query)).scalar_one()

            # Основной запрос для получения уведомлений
            data_query = (
                sa.select(
                    self.model_type,
                    ReadStatus.is_read,
                    ReadStatus.read_at
                )
                .join(NotificationRecipients)
                .outerjoin(
                    ReadStatus,
                    sa.and_(
                        ReadStatus.notification_id == self.model_type.id,
                        ReadStatus.student_id == student_id
                    )
                )
                .where(
                    sa.or_(
                        sa.and_(
                            NotificationRecipients.recipient_type == RecipientType.STUDENT,
                            NotificationRecipients.recipient_id == student_id
                        ),
                        sa.and_(
                            NotificationRecipients.recipient_type == RecipientType.GROUP,
                            NotificationRecipients.recipient_id.in_(group_subquery)
                        )
                    )
                )
                .order_by(self.model_type.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            
            results = (await session.execute(data_query)).all()
            
            notifications = []
            for notification, is_read, read_at in results:
                notification_data = NotificationWithStatusSchema(
                    **NotificationReadSchema.model_validate(notification, from_attributes=True).model_dump(),
                    is_read=is_read or False,
                    read_at=read_at
                )
                notifications.append(notification_data)

            return PaginationResultSchema[NotificationWithStatusSchema](
                count=total_count,
                objects=notifications
            )
        
    async def update_read_status(
        self: Self,
        notification_id: UUID,
        student_id: UUID,
        is_read: bool = True
    ) -> NotificationWithStatusSchema:
        async with self.session as session:
            # Проверяем существование уведомления
            notification = await self.get(notification_id)
            if notification is None:
                raise NotificationNotFoundException()

            # Проверяем существование статуса прочтения
            stmt = sa.select(ReadStatus).where(
                sa.and_(
                    ReadStatus.notification_id == notification_id,
                    ReadStatus.student_id == student_id
                )
            )
            read_status = (await session.execute(stmt)).scalar_one_or_none()

            if read_status:
                # Обновление существующего статуса
                stmt = (
                    sa.update(ReadStatus)
                    .where(
                        sa.and_(
                            ReadStatus.notification_id == notification_id,
                            ReadStatus.student_id == student_id
                        )
                    )
                    .values(
                        is_read=is_read,
                        read_at=datetime.now() if is_read else None
                    )
                    .returning(ReadStatus)
                )
                read_status = (await session.execute(stmt)).scalar_one()
            else:
                # Создание нового статуса
                read_status = ReadStatus(
                    notification_id=notification_id,
                    student_id=student_id,
                    is_read=is_read,
                    read_at=datetime.now() if is_read else None
                )
                session.add(read_status)
                await session.flush()

            await session.commit()

            return NotificationWithStatusSchema(
                **NotificationReadSchema.model_validate(notification, from_attributes=True).model_dump(),
                is_read=read_status.is_read,
                read_at=read_status.read_at
            )

    async def add_recipient(
        self: Self,
        notification_id: UUID,
        recipient_data: NotificationRecipientCreateSchema
    ) -> NotificationRecipientReadSchema:
        async with self.session as session:
            # Проверяем существование уведомления
            notification = await self.get(notification_id)
            if notification is None:
                raise NotificationNotFoundException()

            # Проверяем существование получателя
            stmt = sa.select(NotificationRecipients).where(
                sa.and_(
                    NotificationRecipients.notification_id == notification_id,
                    NotificationRecipients.recipient_id == recipient_data.recipient_id,
                    NotificationRecipients.recipient_type == recipient_data.recipient_type
                )
            )
            existing_recipient = (await session.execute(stmt)).scalar_one_or_none()
            if existing_recipient:
                raise NotificationRecipientAlreadyExistsError()

            # Создаем нового получателя
            new_recipient = NotificationRecipients(
                notification_id=notification_id,
                recipient_type=recipient_data.recipient_type,
                recipient_id=recipient_data.recipient_id
            )
            session.add(new_recipient)
            await session.commit()

            return NotificationRecipientReadSchema.model_validate(new_recipient, from_attributes=True)
        

    async def get_group_notifications(
        self: Self,
        group_id: UUID,
        limit: int = 10,
        offset: int = 0
    ) -> PaginationResultSchema[NotificationWithStatusSchema]:
        async with self.session as session:
            # Запрос для подсчета общего количества уведомлений
            count_query = sa.select(sa.func.count(self.model_type.id)).join(NotificationRecipients).where(
                sa.and_(
                    NotificationRecipients.recipient_type == RecipientType.GROUP,
                    NotificationRecipients.recipient_id == group_id
                )
            )
            total_count = (await session.execute(count_query)).scalar_one()

            # Основной запрос для получения уведомлений
            data_query = (
                sa.select(
                    self.model_type,
                    ReadStatus.is_read,
                    ReadStatus.read_at
                )
                .join(NotificationRecipients)
                .where(
                    sa.and_(
                        NotificationRecipients.recipient_type == RecipientType.GROUP,
                        NotificationRecipients.recipient_id == group_id
                    )
                )
                .order_by(self.model_type.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            results = (await session.execute(data_query)).all()

            notifications = []
            for notification, is_read, read_at in results:
                notification_data = NotificationWithStatusSchema(
                    **NotificationReadSchema.model_validate(notification, from_attributes=True).model_dump(),
                    is_read=is_read or False,
                    read_at=read_at
                )
                notifications.append(notification_data)

            return PaginationResultSchema[NotificationWithStatusSchema](
                count=total_count,
                objects=notifications
            )

    async def delete(self: Self, id: UUID) -> None:
        async with self.session as session:
            # Сначала удаляем связанные записи в notification_recipients
            stmt_recipients = sa.delete(NotificationRecipients).where(
                NotificationRecipients.notification_id == id
            )
            await session.execute(stmt_recipients)

            # Затем удаляем связанные записи в read_status
            stmt_read_status = sa.delete(ReadStatus).where(
                ReadStatus.notification_id == id
            )
            await session.execute(stmt_read_status)

            # И только потом удаляем само уведомление
            stmt = sa.delete(self.model_type).where(self.model_type.id == id)
            await session.execute(stmt)
            await session.commit()