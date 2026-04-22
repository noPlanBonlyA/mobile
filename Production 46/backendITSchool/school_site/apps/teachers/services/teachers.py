from uuid import UUID
from typing import Protocol
from school_site.core.schemas import PaginationSchema
from ..repositories.teachers import TeacherRepositoryProtocol
from ..schemas import TeacherCreateSchema, TeacherReadSchema, TeacherUpdateSchema, TeacherReadWithUserAndUsePhotoSchema, \
    TeacherPaginationWithUserAndUserPhotoResultSchema, \
    TeacherReadWithUserSchema, TeacherPaginationWithUserResultSchema
from ..exceptions import TeacherNotExistsExceptions
from school_site.apps.users.services.users import UserServiceProtocol


class TeacherServiceProtocol(Protocol):
    async def create(self, teacher: TeacherCreateSchema) -> TeacherReadSchema:
        ...

    async def get(self, teacher_id: UUID) -> TeacherReadWithUserSchema:
        ...

    async def update(self, teacher_id: UUID, teacher: TeacherUpdateSchema) -> TeacherReadSchema:
        ...

    async def delete(self, teacher_id: UUID) -> bool:
        ...

    async def list(self, pagination: PaginationSchema) -> TeacherPaginationWithUserResultSchema:
        ...

    async def get_by_user_id(self, user_id: UUID) -> TeacherReadWithUserSchema:
        ...


class TeacherService(TeacherServiceProtocol):
    def __init__(self, teacher_repository: TeacherRepositoryProtocol, user_service: UserServiceProtocol):
        self.teacher_repository = teacher_repository
        self.user_service = user_service

    async def create(self, teacher: TeacherCreateSchema) -> TeacherReadSchema:
        return await self.teacher_repository.create(teacher)
    
    async def get(self, teacher_id: UUID) -> TeacherReadWithUserSchema:
        teacher = await self.teacher_repository.get(teacher_id)
        user = await self.user_service.get_user_by_id(teacher.user_id)
        return TeacherReadWithUserAndUsePhotoSchema(
            id=teacher.id,
            user_id=teacher.user_id,
            created_at=teacher.created_at,
            updated_at=teacher.updated_at,
            user=user
        )
    
    async def update(self, teacher_id: UUID, teacher: TeacherUpdateSchema) -> TeacherReadSchema:
        return await self.teacher_repository.update(teacher)
    
    async def delete(self, teacher_id: UUID) -> bool:
        return await self.teacher_repository.delete(teacher_id)
    
    async def list(self, pagination: PaginationSchema) -> TeacherPaginationWithUserAndUserPhotoResultSchema:
        teachers = await self.teacher_repository.paginate(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            sorting=["created_at", "id"],
            policies=["can_view"]
        )
        teachers_users = [TeacherReadWithUserAndUsePhotoSchema(
            id=teacher.id,
            user_id=teacher.user_id,
            created_at=teacher.created_at,
            updated_at=teacher.updated_at,
            user=(await self.user_service.get_user_by_id(teacher.user_id))
        ) for teacher in teachers.objects]

        return TeacherPaginationWithUserAndUserPhotoResultSchema(count=teachers.count, objects=teachers_users)
    
    async def get_by_user_id(self, user_id: UUID) -> TeacherReadWithUserSchema:
        teacher = await self.teacher_repository.get_by_user_id(user_id)
        if not teacher:
            raise TeacherNotExistsExceptions(user_id)
        user = await self.user_service.get_user_by_id(teacher.user_id)
        return TeacherReadWithUserAndUsePhotoSchema(
            id=teacher.id,
            user_id=teacher.user_id,
            created_at=teacher.created_at,
            updated_at=teacher.updated_at,
            user=user
        ) 