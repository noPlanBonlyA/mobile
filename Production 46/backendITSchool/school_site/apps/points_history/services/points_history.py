from typing import Protocol
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from school_site.apps.students.services.students import StudentServiceProtocol
from school_site.apps.students.schemas import StudentUpdateSchema
from ..repositories.points_history import PointsHistoryRepositoryProtocol
from ..schemas import (
    PointsHistoryCreateSchema,
    PointsHistoryUpdateSchema,
    PointsHistoryUpdateDBSchema,
    PointsHistoryReadSchema,
    PointsHistoryPaginationSchema,
)
class PointsHistoryServiceProtocol(Protocol):
    """
    Интерфейс для сервиса истории баллов.
    """

    repository: PointsHistoryRepositoryProtocol

    async def create_points_history(self, data: PointsHistoryCreateSchema) -> PointsHistoryReadSchema:
        """
        Создает запись в истории баллов.
        """
        ...

    async def update_points_history(self, id: UUID, data: PointsHistoryUpdateSchema) -> PointsHistoryReadSchema:
        """
        Обновляет запись в истории баллов.
        """
        ...

    async def get_points_history(self, id: UUID) -> PointsHistoryReadSchema:
        """
        Получает запись в истории баллов по ID.
        """
        ...

    async def paginate_points_history_by_user_id(self, user_id: UUID, pagination: PaginationSchema) -> PointsHistoryPaginationSchema:
        """
        Пагинация записей истории баллов.
        """
        ...

    async def delete_points_history(self, id: UUID) -> None:
        """
        Удаляет запись в истории баллов по ID.
        """
        ...

class PointsHistoryService(PointsHistoryServiceProtocol):
    """
    Реализация сервиса истории баллов.
    """

    def __init__(self, repository: PointsHistoryRepositoryProtocol,
                 students_service: StudentServiceProtocol):
        self.repository = repository
        self.students_service = students_service

    async def create_points_history(self, data: PointsHistoryCreateSchema) -> PointsHistoryReadSchema:
        students = await self.students_service.get(data.student_id)
        
        student_data = students.model_dump()
        student_data['points'] = students.points + data.changed_points
        
        student_update = StudentUpdateSchema(**student_data)
        await self.students_service.update(students.id, student_update)
        return await self.repository.create(data)

    async def update_points_history(self, id: UUID, data: PointsHistoryUpdateSchema) -> PointsHistoryReadSchema:
        # Если этот метод надо использовать, то нужно будет реализовать логику обновления баллов студента
        # Например, можно получить текущего студента и обновить его баллы на основе измененных данных
        db_update = PointsHistoryUpdateDBSchema(id=id, **data.model_dump())
        return await self.repository.update(db_update)

    async def get_points_history(self, id: UUID) -> PointsHistoryReadSchema:
        return await self.repository.get(id)

    async def paginate_points_history_by_user_id(self, user_id: UUID, pagination: PaginationSchema) -> PointsHistoryPaginationSchema:
        student = await self.students_service.get_by_user_id(user_id)
        return await self.repository.paginate(
            search=str(student.id),
            search_by=["student_id"],
            sorting=["-created_at"],
            pagination=pagination,
            user=None,
            policies=["can_view_points_history"]
                                              )

    async def delete_points_history(self, id: UUID) -> None:
        # Если этот метод надо использовать, то нужно будет реализовать логику обновления баллов студента
        # Например, можно получить текущего студента и обновить его баллы на основе измененных данных
        await self.repository.delete(id)