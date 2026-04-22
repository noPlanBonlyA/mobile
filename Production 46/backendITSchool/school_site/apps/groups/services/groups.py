import logging
from typing import Protocol
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from school_site.core.schemas import PaginationSchema
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.apps.teachers.models import Teacher 
from ..schemas import (
    GroupCreateSchema,
    GroupUpdateSchema,
    GroupUpdateDBSchema,
    GroupReadSchema,
    GroupReadHeadSchema,
    GroupPaginationResultSchema,
    GroupCreateDBSchema,
    GroupWithStudentsAndTeacherAndCoursesSchema
)
from ..repositories.groups import GroupRepositoryProtocol


logger = logging.getLogger(__name__)


class GroupServiceProtocol(Protocol):
    async def create(self, group: GroupCreateSchema) -> GroupReadSchema:
        ...

    async def get(self, group_id: UUID) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        ...

    async def update(self, group_id: UUID, group: GroupUpdateSchema) -> GroupReadSchema:
        ...

    async def delete(self, group_id: UUID) -> None:
        ...

    async def list(self, pagination: PaginationSchema) -> GroupPaginationResultSchema:
        ...


class GroupService(GroupServiceProtocol):
    def __init__(self, group_repository: GroupRepositoryProtocol):
        self.group_repository = group_repository

    async def create(self, group: GroupCreateSchema) -> GroupReadSchema:
        logger.info("Creating new group")
        group_db = GroupCreateDBSchema(
            name=group.name,
            description=group.description,
            start_date=group.start_date,
            end_date=group.end_date,
            teacher_id=group.teacher_id
        )
        try:
            new_group = await self.group_repository.create(group_db)
            return GroupReadSchema(
                id=new_group.id,
                name=new_group.name,
                description=new_group.description,
                start_date=new_group.start_date,
                end_date=new_group.end_date,
                teacher_id=new_group.teacher_id
            )
        except IntegrityError as e:
            if 'groups_teacher_id_fkey' in str(e):
                logger.error("Teacher not found for group creation")
                raise ModelNotFoundException(model=Teacher, model_id=group.teacher_id) from e
            else:
                logger.error("Data integrity error during group creation")
                raise ValueError("Ошибка целостности данных") from e
    async def get(self, group_id: UUID) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        logger.info(f"Fetching group {group_id}")
        try:
            group = await self.group_repository.get_with_students_and_teacher(group_id)
            logger.info(f"Group {group_id} fetched successfully")
            return group
        except Exception:
            logger.error(f"Failed to fetch group {group_id}")
            raise

    async def update(self, group_id: UUID, group: GroupUpdateSchema) -> GroupReadSchema:
        logger.info(f"Updating group {group_id}")
        group_db = GroupUpdateDBSchema(
            id=group_id,
            name=group.name,
            description=group.description,
            start_date=group.start_date,
            end_date=group.end_date,
            teacher_id=group.teacher_id
        )
        try:
            updated_group = await self.group_repository.update(group_db)
            logger.info(f"Group {group_id} updated successfully")
            return GroupReadSchema(
                id=updated_group.id,
                name=updated_group.name,
                description=updated_group.description,
                start_date=updated_group.start_date,
                end_date=updated_group.end_date,
                teacher_id=updated_group.teacher_id
            )
        except IntegrityError as e:
            if 'groups_teacher_id_fkey' in str(e):
                logger.error(f"Teacher not found for group {group_id}")
                raise ModelNotFoundException(model=Teacher, model_id=group.teacher_id) from e
            else:
                logger.error(f"Integrity error updating group {group_id}")
                raise ValueError("Ошибка целостности данных") from e


    async def delete(self, group_id: UUID) -> None:
        logger.info(f"Deleting group {group_id}")
        try:
            await self.group_repository.delete(group_id)
            logger.info(f"Group {group_id} deleted successfully")
        except Exception:
            logger.error(f"Failed to delete group {group_id}")
            raise

    async def list(self, pagination: PaginationSchema) -> GroupPaginationResultSchema:
        logger.info("Listing groups")
        try:
            groups_paginate = await self.group_repository.paginate(
                search=None,
                search_by=None,
                pagination=pagination,
                sorting=["created_at", "id"]
            )
            logger.info(f"Successfully retrieved {groups_paginate.count} groups")
            return GroupPaginationResultSchema(
                objects=[GroupReadHeadSchema(id=g.id, name=g.name) for g in groups_paginate.objects],
                count=groups_paginate.count
            ) 
        except Exception:
            logger.error("Failed to list groups")
            raise