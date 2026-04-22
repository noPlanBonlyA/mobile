from fastapi import UploadFile
import asyncio
import logging
from typing import Protocol, Optional, List
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from ..schemas import (
    CourseCreateSchema,
    CourseUpdateSchema,
    CourseCreateDBSchema,
    CourseUpdateDBSchema,
    CourseWithPhotoReadSchema,
    CourseWithPhotoReadDBSchema,
    CourseWithPhotoPaginationResultSchema,
    PhotoCreateSchema,
    PhotoUpdateSchema,
    PhotoReadSchema,
    PhotoReadDBSchema,
    CourseReadDBSchema
)
from ..repositories.courses import CourseRepositoryProtocol
from .photo_courses import PhotoServiceProtocol

logger = logging.getLogger(__name__)


class CourseServiceProtocol(Protocol):
    async def create(self, course: CourseCreateSchema, image: Optional[UploadFile]) -> CourseWithPhotoReadSchema:
        ...

    async def get(self, course_id: UUID) -> CourseWithPhotoReadSchema:
        ...

    async def update(self, course_id: UUID, course: CourseUpdateSchema, image: Optional[UploadFile]) -> CourseWithPhotoReadSchema:
        ...

    async def delete(self, course_id: UUID) -> None:
        ...

    async def list(self, pagination: PaginationSchema) -> CourseWithPhotoPaginationResultSchema:
        ...

    async def get_courses_by_teacher_id(self, teacher_id: UUID) -> List[CourseWithPhotoReadSchema]:
        ...

class CourseService(CourseServiceProtocol):
    def __init__(self, course_repository: CourseRepositoryProtocol,
                 photo_service: PhotoServiceProtocol):
        self.course_repository = course_repository
        self.photo_service = photo_service


    async def create(self, course: CourseCreateSchema, image: Optional[UploadFile]) -> CourseWithPhotoReadSchema:
        course_db = CourseCreateDBSchema(
            name=course.name,
            description=course.description,
            age_category=course.age_category,
            price=course.price,
            author_name=course.author_name
        )
        new_course = await self.course_repository.create(course_db)
        photo = None
        if course.photo and image:
            photo = await self.photo_service.create(
                PhotoCreateSchema(name=course.photo.name, course_id=new_course.id),
                image
            )
        return CourseWithPhotoReadSchema(
            id=new_course.id,
            name=new_course.name,
            description=new_course.description,
            age_category=new_course.age_category,
            price=new_course.price,
            author_name=new_course.author_name,
            photo=photo,
            created_at=new_course.created_at,
            updated_at=new_course.updated_at
        )

    async def get(self, course_id: UUID) -> CourseWithPhotoReadSchema:
        course = await self.get_with_photo(course_id)
        photo_read = None
        if course.photo:
            image_url = await self.photo_service.get_photo_url(course.photo.path)
            photo_read = PhotoReadSchema(
                id=course.photo.id,
                name=course.photo.name,
                course_id=course.id,
                url=image_url,
                created_at=course.photo.created_at,
                updated_at=course.photo.updated_at
            )
        return CourseWithPhotoReadSchema(
            id=course.id,
            name=course.name,
            description=course.description,
            age_category=course.age_category,
            price=course.price,
            author_name=course.author_name,
            created_at=course.created_at,
            updated_at=course.updated_at,
            photo=photo_read
        )

    async def get_with_photo(self, course_id: UUID) -> CourseWithPhotoReadSchema:
        course = await self.course_repository.get_with_photo(course_id)
        return course
    
    async def update(self, course_id: UUID, course: CourseUpdateSchema, image: Optional[UploadFile]) -> CourseWithPhotoReadSchema:
        upd_course_db = CourseUpdateDBSchema(
            id=course_id,
            name=course.name,
            description=course.description,
            age_category=course.age_category,
            price=course.price,
            author_name=course.author_name
        )
        updated_course = await self.course_repository.update(upd_course_db)
        photo = None
        is_updated = False

        if course.photo and image:
            if not course.photo.id:
                course_with_photo = await self.get_with_photo(course_id)
                if not course_with_photo.photo:
                    photo_create = PhotoCreateSchema(
                        name=course.photo.name,
                        course_id=course_id
                    )
                    photo = await self.photo_service.create(photo_create, image)
                    is_updated = True
                else:
                    photo_id = course_with_photo.photo.id

            else:
                photo_id = course.photo.id

            if not is_updated:
                photo = await self.photo_service.update(
                    photo_id,
                    PhotoUpdateSchema(
                        course_id=course_id,
                        name=course.photo.name
                    ),
                    image
                )
        else:
            return await self.get(course_id)

        return CourseWithPhotoReadSchema(
            id=updated_course.id,
            name=updated_course.name,
            description=updated_course.description,
            age_category=updated_course.age_category,
            price=updated_course.price,
            created_at=updated_course.created_at,
            updated_at=updated_course.updated_at,
            author_name=updated_course.author_name,
            photo=photo
        )

    async def delete(self, course_id: UUID) -> bool:
        course = await self.get_with_photo(course_id)
        if course.photo:
            await self.photo_service.delete(course.photo.id)
        await self.course_repository.delete(course_id)

    async def list(self, pagination: PaginationSchema) -> CourseWithPhotoPaginationResultSchema:
        courses_paginate = await self.course_repository.paginate(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            sorting=["created_at", "id"],
            policies=["can_view"]
        )
        converted_products = await self._convert_courses_path_to_url(courses_paginate.objects)

        converted_products_paginate = CourseWithPhotoPaginationResultSchema(objects=converted_products,
                                                           count=courses_paginate.count)
        
        return converted_products_paginate
    
    async def _convert_courses_path_to_url(
    self, 
    courses: List[CourseWithPhotoReadDBSchema]
) -> List[CourseWithPhotoReadSchema]:
    
        async def process_photo(photo: PhotoReadDBSchema) -> PhotoReadSchema:
            if not photo:
                return None
            url = await self.photo_service.get_photo_url(photo.path)
            return PhotoReadSchema(
                id=photo.id,
                name=photo.name,
                course_id=photo.course_id,
                url=url,
                created_at=photo.created_at,
                updated_at=photo.updated_at
        )
    
        async def process_course(course: CourseWithPhotoReadDBSchema) -> CourseWithPhotoReadSchema:
            photo = course.photo
            conv_photo = await process_photo(photo) if photo else None
            
            return CourseWithPhotoReadSchema(
                id=course.id,
                name=course.name,
                description=course.description,
                price=course.price,
                photo=conv_photo,
                created_at=course.created_at,
                author_name=course.author_name,
                age_category=course.age_category,
                updated_at=course.updated_at
            )
    
        return await asyncio.gather(*[process_course(p) for p in courses])
    
    async def get_courses_by_teacher_id(self, teacher_id: UUID) -> List[CourseWithPhotoReadSchema]:
        courses = await self.course_repository.get_courses_by_teacher_id(teacher_id)
        converted_courses = await self._convert_courses_path_to_url(courses)
        return converted_courses