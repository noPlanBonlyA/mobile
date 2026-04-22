from typing import Self
from school_site.core.enums import UserRole
from school_site.apps.users.schemas import UserTokenDataReadSchema
from school_site.core.utils.exceptions import PermissionDeniedError



class PermissionsService:
    def __init__(self):
        self.operations ={
            "get_user": self._check_get_user,
            "get_all_users": self._check_get_all_users,
            "update_user": self._check_update_user,
            "create_user": self._check_create_user,
            "delete_user": self._check_delete_user,
        }
    
    def check(self: Self, operation: str, current_user: UserTokenDataReadSchema, **context) -> bool:
        if operation not in self.operations:
            raise ValueError(f"Unknown permission operation: {operation}")
        return self.operations[operation](current_user, **context)

    def _check_get_user(self: Self, current_user: UserTokenDataReadSchema, **context) -> bool:
        target_user = context.get('target_user')
        if not target_user:
            raise ValueError("Target user is required for get_user check")
        
        if current_user.role == UserRole.ADMIN and target_user.role != UserRole.STUDENT:
            raise PermissionDeniedError()
        return True
    
    def _check_get_all_users(self: Self, current_user: UserTokenDataReadSchema, **context) -> bool:
        return current_user.role == UserRole.ADMIN
    
    def _check_update_user(self: Self, current_user: UserTokenDataReadSchema, **context) -> bool:
        target_user = context.get('target_user')
        target_user_id = context.get('target_user_id')
        
        if not target_user:
            raise ValueError("Target user is required for update_user check")
        
        # Проверка прав для разных ролей
        if (
            # Администратор может редактировать:
            # - только студентов
            # - или свой собственный аккаунт
            (current_user.role == UserRole.ADMIN and 
            not (target_user.role in [UserRole.STUDENT, UserRole.TEACHER] or 
                (target_user.role == UserRole.ADMIN and current_user.user_id == target_user_id))) 
            or
            # Студент может редактировать только свой профиль
            (current_user.role == UserRole.STUDENT and target_user.role != UserRole.STUDENT) 
            or 
            # Учитель может редактировать только учительский профиль
            (current_user.role == UserRole.TEACHER and target_user.role != UserRole.TEACHER)
        ):
            raise PermissionDeniedError()
        
        return True
    
    def _check_create_user(self: Self, current_user: UserTokenDataReadSchema, **context) -> bool:
        user_data = context.get('user_data')
        
        if current_user.role == UserRole.ADMIN and user_data.role not in [UserRole.STUDENT, UserRole.TEACHER]:
            raise PermissionDeniedError()
        
        return True

    def _check_delete_user(self, current_user: UserTokenDataReadSchema, **context) -> bool:
        target_user = context.get('target_user')
        if not target_user:
            raise ValueError("Target user is required for delete_user check")
        
        if current_user.role == UserRole.ADMIN and target_user.role not in [UserRole.STUDENT, UserRole.TEACHER]:
            raise PermissionDeniedError()
        
        return True
        
permission_service = PermissionsService()
