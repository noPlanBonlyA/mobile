import logging
from school_site.apps.groups.services.groups import GroupServiceProtocol
from sqlalchemy.exc import IntegrityError
from typing import Protocol
from uuid import UUID
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from school_site.core.utils.exceptions import ModelAlreadyExistsError, ModelNotFoundException
from ..repositories.group_teachers import GroupTeachersRepositoryProtocol
from ..schemas import GroupReadTeacherSchema
from school_site.apps.teachers.models import Teacher
from school_site.apps.groups.models import Group
logger = logging.getLogger(__name__)


class GroupTeacherServiceProtocol(Protocol):
    async def add_teacher(self, group_id: UUID, teacher_id: UUID) -> GroupReadTeacherSchema:
        ...

    async def delete_teacher(self, group_id: UUID, teacher_id: UUID) -> bool:
        ...

    async def get_by_teacher_id(self, teacher_id: UUID) -> list[GroupReadTeacherSchema]:
        ...


class GroupTeacherService(GroupTeacherServiceProtocol):
    def __init__(
        self,
        group_teachers_repository: GroupTeachersRepositoryProtocol,
        group_service: GroupServiceProtocol,
        teacher_service: TeacherServiceProtocol
    ):
        self.group_teachers_repository = group_teachers_repository
        self.group_service = group_service
        self.teacher_service = teacher_service

    async def add_teacher(self, group_id: UUID, teacher_id: UUID) -> GroupReadTeacherSchema:
        group = await self.group_service.get(group_id)
        if await self.group_teachers_repository.has_teacher(group_id):
            raise ModelAlreadyExistsError(
                model=Group,
                field="teacher_id",
                message="Group already has a teacher"
            )
        try:
            await self.group_teachers_repository.add_teacher(group_id, teacher_id)
            return GroupReadTeacherSchema(
                id=group.id,
                name=group.name,
                description=group.description,
                start_date=group.start_date,
                end_date=group.end_date,
                teacher_id=teacher_id
            )
        except IntegrityError as e:
            logger.error(f"Error adding teacher to group: {str(e)}")
            raise ModelNotFoundException(
                model=Teacher,
                model_id=teacher_id
            )

    async def delete_teacher(self, group_id: UUID, teacher_id: UUID) -> bool:
        await self.group_teachers_repository.delete_teacher(group_id, teacher_id)
        return True
    
    async def get_by_teacher_id(self, teacher_id: UUID) -> list[GroupReadTeacherSchema]:
        groups = await self.group_teachers_repository.get_by_teacher_id(teacher_id)
        if not groups:
            raise ModelNotFoundException(
                model=Group,
                model_id=teacher_id
            )
        return [GroupReadTeacherSchema.model_validate(group, from_attributes=True) for group in groups]