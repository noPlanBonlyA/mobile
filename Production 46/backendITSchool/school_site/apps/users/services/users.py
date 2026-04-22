import logging
from typing import Protocol, Self, List, Optional
from uuid import UUID
from fastapi import UploadFile
import asyncio
from school_site.apps.users.schemas import(
    UserCreateSchema, UserReadSchema, RegisterRequestSchema, UserReadDBSchema,
    UserUpdateSchema, UserUpdateDBSchema, UserUpdateRequestSchema, UserUpdateNoPasswordSchema, UserUpdateDBNoPasswordHashSchema, 
    PaginationResultSchema, UserWithPhotoReadSchema, UserWithPhotoReadDBSchema, UserWithPhotoPaginationResultSchema,
    UserWithPhotoPaginationResultDBSchema, PhotoUserReadSchema, PhotoUserReadDBSchema, PhotoUserCreateSchema, PhotoUserUpdateSchema
) 
from school_site.apps.users.repositories.users import UserRepositoryProtocol
from school_site.apps.users.services.passwords import PasswordServiceProtocol
from school_site.apps.users.services.photo_user import PhotoUserServiceProtocol
from school_site.apps.users.exceptions import (
    InvalidCredentialsError, UsernameNotExistsExceptions
)
from ..schemas import PasswordSchema
from school_site.core.enums import UserRole
from school_site.core.schemas import PaginationSchema


logger = logging.getLogger(__name__)


class UserServiceProtocol(Protocol):
    async def create_user(self: Self, user: RegisterRequestSchema, image: Optional[UploadFile] = None) -> UserWithPhotoReadSchema:
        ...
    
    async def get_user_by_id(self: Self, user_id: UUID) -> UserWithPhotoReadSchema:
        ...
    
    async def _get_user_by_username(self: Self, username: int) -> UserReadDBSchema | None:
        ...

    async def get_user_by_username(self: Self, username: int) -> UserReadDBSchema | None:
        ...
    
    async def authenticate_user(self: Self, username: int, password: str) -> UserWithPhotoReadSchema:
        ...

    async def authenticate_user_without_photo(self: Self, username: int, password: str) -> UserReadSchema:
        ...

    async def authenticate_user_by_id(self: Self, user_id: UUID, password: str) -> UserReadSchema:
        ...

    async def update_user(self: Self, user: UserUpdateSchema) -> UserReadSchema:
        ...

    async def update_user_by_router(self: Self, url_user_id: UUID, user_data: UserUpdateRequestSchema, image: Optional[UploadFile] = None) -> UserWithPhotoReadSchema:
      ...

    async def change_password(self: Self, record_id: UUID, new_password: str) -> UserWithPhotoReadSchema:
        ...

    async def get_all_users(self: Self, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0) -> PaginationResultSchema[UserWithPhotoReadSchema]:
        ...

    async def delete_user(self:Self, user_id: UUID) -> bool:
        ...

    async def get_by_email_or_none(self: Self, email: str) -> Optional[UserReadDBSchema]:
      ...

    async def get_me(self: Self, user_id: UUID) -> UserWithPhotoReadSchema:
        ...

    async def list(self, pagination: PaginationSchema) -> UserWithPhotoPaginationResultSchema:
        ...

class UserService(UserServiceProtocol):
    def __init__(
        self: Self,
        user_repository: UserRepositoryProtocol,
        password_service: PasswordServiceProtocol,
        photo_service: PhotoUserServiceProtocol
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.photo_service = photo_service
    
    async def create_user(self: Self, user: RegisterRequestSchema, image: Optional[UploadFile] = None) -> UserWithPhotoReadSchema:
        
        password_hash = self.password_service.get_password_hash(user.password)
        username = await self.user_repository.generate_username()
        username_str = str(username)
        username_str = "0" * (3-len(username_str)) + username_str
        user_create = UserCreateSchema(
            username=username,
            first_name=user.first_name,
            surname=user.surname,
            patronymic=user.patronymic,
            email=user.email,
            phone_number=user.phone_number,
            password_hash=password_hash,
            role=user.role,
            birth_date=user.birth_date
        )
        new_user = await self.user_repository.create(user_create)
        
        photo = None
        if image:
            photo = await self.photo_service.create(
                PhotoUserCreateSchema(name=f"photo_{new_user.username}", user_id=new_user.id),
                image
            )
        
        logger.info(f"Successfully created user with id: {new_user.id}")
        return UserWithPhotoReadSchema(
            id=new_user.id,
            username=new_user.username,
            first_name=new_user.first_name,
            surname=new_user.surname,
            patronymic=new_user.patronymic,
            email=new_user.email,
            phone_number=new_user.phone_number,
            role=new_user.role,
            birth_date=new_user.birth_date,
            photo=photo,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at
        )
    
    async def update_user(self: Self, user: UserUpdateSchema) -> UserReadSchema:
        db_user = UserUpdateDBSchema(
            first_name=user.first_name,
            surname=user.surname,
            patronymic=user.patronymic,
            email=user.email,
            phone_number=user.phone_number,
            role=user.role,
            birth_date=user.birth_date
        )
        updated_user = await self.user_repository.update(db_user)
        return UserReadSchema(**updated_user.model_dump(exclude={'password_hash'}))

    async def update_user_by_router(self: Self, url_user_id: UUID, user_data: UserUpdateRequestSchema, image: Optional[UploadFile] = None) -> UserWithPhotoReadSchema:

        update_data = UserUpdateNoPasswordSchema(
            id=url_user_id,
            **user_data.model_dump()
        )
        
        db_user = UserUpdateDBNoPasswordHashSchema(
            id=url_user_id,
            first_name=update_data.first_name,
            surname=update_data.surname,
            patronymic=update_data.patronymic,
            email=update_data.email,
            phone_number=update_data.phone_number,
            role=update_data.role,
            birth_date=update_data.birth_date
        )
    
        updated_user = await self.user_repository.update(db_user)
        photo = None

        if image:
            user_with_photo = await self.get_with_photo(url_user_id)
            if user_with_photo.photo:
                photo = await self.photo_service.update(
                    user_with_photo.photo.id,
                    PhotoUserUpdateSchema(
                        user_id=url_user_id,
                        name=f"photo_{updated_user.username}"
                    ),
                    image
                )
            else:
                photo = await self.photo_service.create(
                    PhotoUserCreateSchema(name=f"photo_{updated_user.username}", user_id=url_user_id),
                    image
                )
        else:
            return await self.get_user_by_id(url_user_id)

        return UserWithPhotoReadSchema(
            id=updated_user.id,
            username=updated_user.username,
            first_name=updated_user.first_name,
            surname=updated_user.surname,
            patronymic=updated_user.patronymic,
            email=updated_user.email,
            phone_number=updated_user.phone_number,
            role=updated_user.role,
            birth_date=updated_user.birth_date,
            photo=photo,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )

    async def change_password(self: Self, record_id: UUID, new_password: str) -> UserWithPhotoReadSchema:
        password_hash = self.password_service.get_password_hash(new_password)
        password_schema = PasswordSchema(
            password_hash=password_hash
        )
        updated_user =  await self.user_repository.change_password(record_id, password_schema)
        return await self.get_user_by_id(updated_user.id)

    
    async def get_user_by_id(self: Self, user_id: UUID) -> UserWithPhotoReadSchema:
        logger.info(f"Fetching user with id: {user_id}")
        user = await self.get_with_photo(user_id)
        photo_read = None
        if user.photo:
            image_url = await self.photo_service.get_photo_url(user.photo.path)
            photo_read = PhotoUserReadSchema(
                id=user.photo.id,
                name=user.photo.name,
                user_id=user.id,
                url=image_url,
                created_at=user.photo.created_at,
                updated_at=user.photo.updated_at
            )
        return UserWithPhotoReadSchema(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            surname=user.surname,
            patronymic=user.patronymic,
            email=user.email,
            phone_number=user.phone_number,
            role=user.role,
            birth_date=user.birth_date,
            photo=photo_read,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    async def get_with_photo(self, user_id: UUID) -> UserWithPhotoReadDBSchema:
        user = await self.user_repository.get_with_photo(user_id)
        return user
     
    async def _get_user_by_id(self: Self, user_id: UUID) -> UserReadDBSchema:
        logger.info(f"Fetching user schema with password with id: {user_id}")
        return await self.user_repository.get(user_id)

    
    async def _get_user_by_username(self: Self, username: int) -> UserReadDBSchema | None:
        user = await self.user_repository.get_by_username(username)
        return user
    

    async def get_user_by_username(self: Self, username: int) -> UserReadSchema:
        user = await self.user_repository.get_by_username(username)
        if not user:
            logger.error(f"user with username {username} not found")
            raise UsernameNotExistsExceptions(username)
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))
    

    async def authenticate_user(self: Self, username: int, password: str) -> UserWithPhotoReadSchema:
        logger.info(f"Authenticating user: {username}")
        
        user = await self._get_user_by_username(username)

        if not user:
            logger.error(f"User with username {username} not found")
            raise UsernameNotExistsExceptions(username)
        
        if not self.password_service.verify_password(password, user.password_hash):
            logger.error(f"Authentication failed: Invalid password for user {username}")
            raise InvalidCredentialsError()
        
        logger.info(f"Authentication successful for user: {username}")
        return await self.get_user_by_id(user.id)

    async def authenticate_user_by_id(self: Self, user_id: UUID, password: str) -> UserReadSchema:
        logger.info(f"Authenticating user: {user_id}")
        
        user = await self._get_user_by_id(user_id)

        if not self.password_service.verify_password(password, user.password_hash):
            logger.error(f"Authentication failed: Invalid password for user {user_id}")
            raise InvalidCredentialsError()
        
        logger.info(f"Authentication successful for user: {user_id}")
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))
    
    async def get_all_users(self: Self, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0) -> PaginationResultSchema[UserWithPhotoReadSchema]:
        logger.info(f"Fetching users with role={role}, limit={limit}, offset={offset}")
    
        paginated_users = await self.user_repository.get_all(
            role=role,
            limit=limit,
            offset=offset
        )
    
        user_schemas = []
        for user in paginated_users.objects:
            # Получаем пользователя с фото
            user_with_photo = await self.get_user_by_id(user.id)
            user_schemas.append(user_with_photo)
    
    
        return PaginationResultSchema[UserWithPhotoReadSchema](count=paginated_users.count, objects=user_schemas)

    

    async def delete_user(self: Self, user_id: UUID) -> bool:
        logger.info(f"Deleting user with id: {user_id}")
        
        user = await self.get_with_photo(user_id)
        if user.photo:
            await self.photo_service.delete(user.photo.id)
        
        await self.user_repository.delete(user_id)
        
        logger.info(f"Successfully deleted user with id: {user_id}")
        return True


    async def get_by_email_or_none(self: Self, email: str) -> Optional[UserReadDBSchema]:
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))


    async def get_me(self: Self, user_id: UUID) -> UserWithPhotoReadSchema:
        logger.info("Fetching myself user")
        return await self.get_user_by_id(user_id)

    async def list(self, pagination: PaginationSchema) -> UserWithPhotoPaginationResultSchema:
        user_paginate = await self.user_repository.paginate(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            sorting=["created_at", "id"],
            policies=["can_view"]
        )
        converted_users = await self._convert_users_path_to_url(user_paginate.objects)

        converted_users_paginate = UserWithPhotoPaginationResultSchema(objects=converted_users,
                                                           count=user_paginate.count)
        
        return converted_users_paginate
    
    async def _convert_users_path_to_url(
    self, 
    users: List[UserWithPhotoPaginationResultDBSchema]
) -> List[UserWithPhotoPaginationResultSchema]:
    
        async def process_photo(photo: PhotoUserReadDBSchema) -> PhotoUserReadSchema:
            if not photo:
                return None
            url = await self.photo_service.get_photo_url(photo.path)
            return PhotoUserReadSchema(
                id=photo.id,
                name=photo.name,
                user_id=photo.user_id,
                url=url,
                created_at=photo.created_at,
                updated_at=photo.updated_at
        )
    
        async def process_user(user: UserWithPhotoReadDBSchema) -> UserWithPhotoReadSchema:
            photo = user.photo
            conv_photo = await process_photo(photo) if photo else None
            
            return UserWithPhotoReadSchema(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                surname=user.surname,
                patronymic=user.patronymic,
                email=user.email,
                phone_number=user.phone_number,
                role=user.role,
                birth_date=user.birth_date,
                photo=conv_photo,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
    
        return await asyncio.gather(*[process_user(p) for p in users])

    async def authenticate_user_without_photo(self: Self, username: int, password: str) -> UserReadSchema:
        logger.info(f"Authenticating user without photo: {username}")
        
        user = await self._get_user_by_username(username)

        if not user:
            logger.error(f"User with username {username} not found")
            raise UsernameNotExistsExceptions(username)
        
        if not self.password_service.verify_password(password, user.password_hash):
            logger.error(f"Authentication failed: Invalid password for user {username}")
            raise InvalidCredentialsError()
        
        logger.info(f"Authentication successful for user: {username}")
        return UserReadSchema(**user.model_dump(exclude={'password_hash'}))
   