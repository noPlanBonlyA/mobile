from uuid import UUID
from typing import Protocol, List, Optional
from school_site.core.schemas import PaginationSchema
from ..repositories.students import StudentRepositoryProtocol
from ..schemas import StudentCreateSchema, StudentReadSchema, StudentUpdateSchema, \
    StudentReadWithUserAndUsePhotoSchema, StudentPaginationWithUserResultSchema, \
    StudentPaginationWithUserAndUserPhotoResultSchema
from ..exceptions import StudentNotExistsExceptions
from school_site.apps.users.services.users import UserServiceProtocol

class StudentServiceProtocol(Protocol):
    async def create(self, student: StudentCreateSchema) -> StudentReadSchema:
        ...

    async def get(self, student_id: UUID) -> StudentReadWithUserAndUsePhotoSchema:
        ...

    async def update(self, student_id: UUID, student: StudentUpdateSchema) -> StudentReadSchema:
        ...

    async def delete(self, student_id: UUID) -> bool:
        ...

    async def list(self, pagination: PaginationSchema, sorting_by: Optional[str] = None) -> StudentPaginationWithUserResultSchema:
        ...

    async def get_by_user_id(self, user_id: UUID) -> StudentReadWithUserAndUsePhotoSchema:
        ...


class StudentService(StudentServiceProtocol):
    def __init__(self, student_repository: StudentRepositoryProtocol, user_service: UserServiceProtocol):
        self.student_repository = student_repository
        self.user_service = user_service

    async def create(self, student: StudentCreateSchema) -> StudentReadSchema:
        return await self.student_repository.create(student)
    
    async def get(self, student_id: UUID) -> StudentReadWithUserAndUsePhotoSchema:
        student =  await self.student_repository.get(student_id)
        user = await self.user_service.get_user_by_id(student.user_id)
        return StudentReadWithUserAndUsePhotoSchema(
            id=student.id,
            user_id=student.user_id,
            points=student.points,
            created_at=student.created_at,
            updated_at=student.updated_at,
            user=user
        )
    
    async def update(self, student_id: UUID, student: StudentUpdateSchema) -> StudentReadSchema:
        return await self.student_repository.update(student)
    
    async def delete(self, student_id: UUID) -> bool:
        return await self.student_repository.delete(student_id)
    
    async def list(self, pagination: PaginationSchema, sorting_by: Optional[str] = None) -> StudentPaginationWithUserResultSchema:
        sorting_by = sorting_by or "created_at"
        sorting_by = [sorting_by]
        students = await self.student_repository.paginate(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            sorting=sorting_by,
            policies=["can_view"]
        )
        students_users = [StudentReadWithUserAndUsePhotoSchema(
            id=student.id,
            user_id=student.user_id,
            points=student.points,
            created_at=student.created_at,
            updadet_at=student.updated_at,
            user=(await self.user_service.get_user_by_id(student.user_id))
        ) for student in students.objects]

        return StudentPaginationWithUserAndUserPhotoResultSchema(count=students.count, objects=students_users)
    
    async def get_by_user_id(self, user_id: UUID) -> StudentReadWithUserAndUsePhotoSchema:
        student = await self.student_repository.get_by_user_id(user_id)
        if not student:
            raise StudentNotExistsExceptions(user_id)
        user = await self.user_service.get_user_by_id(student.user_id)
        return StudentReadWithUserAndUsePhotoSchema(
            id=student.id,
            user_id=student.user_id,
            points=student.points,
            created_at=student.created_at,
            updadet_at=student.updated_at,
            user=user
        )
    
class StudentsByGroupServiceProtocol(Protocol):
    
    async def get_students_by_group_id(self, group_id: UUID) -> List[StudentReadSchema]:
        ...

class StudentsByGroupService(StudentsByGroupServiceProtocol):
    def __init__(self, repository: StudentRepositoryProtocol):
        self.repository = repository
    
    async def get_students_by_group_id(self, group_id: UUID) -> List[StudentReadSchema]:
        return await self.repository.get_students_by_group_id(group_id)