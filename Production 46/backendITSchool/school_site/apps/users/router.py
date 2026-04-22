from fastapi import APIRouter, Depends, Response, Query, Form, UploadFile, File
from typing import Optional
from uuid import UUID
from .schemas import (
    LoginRequestSchema, UserWithPhotoReadSchema, PasswordChangeSchema, 
    UserResetSchema, ResetPasswordRequest, PaginationResultSchema, UserIdSchema
)
from .use_cases.login import LoginUseCaseProtocol
from .use_cases.refresh import RefreshUseCaseProtocol
from .use_cases.logout import LogoutUseCaseProtocol
from .use_cases.change_password import ChangePasswordUseCaseProtocol
from .use_cases.create_user import CreateUserUseCaseProtocol
from .use_cases.get_all_users import GetAllUsersUseCaseProtocol
from .use_cases.get_user_by_id import GetUserByIdUseCaseProtocol
from .use_cases.update_user import UpdateUserUseCaseProtocol
from .use_cases.delete_user import DeleteUserUseCaseProtocol
from .use_cases.auth_by_another_user import AuthByAnotherUserUseCaseProtocol
from .depends import (
    get_login_use_case, get_refresh_use_case, get_logout_use_case, get_change_password_use_case, 
    get_create_user_use_case, get_all_users_use_case, get_get_user_by_id_use_case, get_update_user_use_case, 
    get_delete_user_use_case, get_reset_password_use_case, get_confirm_reset_password_use_case, 
    get_me_by_user_id_use_case, get_auth_by_another_user_use_case, access_token_schema, refresh_token_schema
)
from .use_cases.reset_password import ResetPasswordUseCaseProtocol
from .use_cases.confirm_reset_password import ConfirmResetPasswordUseCaseProtocol
from .use_cases.get_me import GetMeByUserIdUseCaseProtocol
from .utils.cookies import set_auth_cookies
from school_site.core.enums import UserRole


router = APIRouter(prefix='/api/users', tags=['Users'])

@router.post("/auth", response_model=UserWithPhotoReadSchema)
async def login(
    response: Response,
    user_data: LoginRequestSchema,
    login_use_case: LoginUseCaseProtocol = Depends(get_login_use_case)
):
    user_tokens_data = await login_use_case(
        user_data.username, user_data.password
    )
    
    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    
    return user_tokens_data.user

@router.post("/refresh", response_model=UserWithPhotoReadSchema)
async def refresh_token(
    response: Response,
    refresh_use_case: RefreshUseCaseProtocol = Depends(get_refresh_use_case),
    refresh_token: str = Depends(refresh_token_schema)
):
    user_tokens_data = await refresh_use_case(refresh_token)
    
    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    
    return user_tokens_data.user

@router.post("/logout", status_code=204)
async def logout(
    response: Response,
    logout: LogoutUseCaseProtocol = Depends(get_logout_use_case),
    refresh_token: str = Depends(refresh_token_schema),
):
    await logout(refresh_token)
    
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    
    return None


@router.post("/change_password", response_model=UserWithPhotoReadSchema, status_code=200)
async def change_password(
    response: Response,
    password_data: PasswordChangeSchema,  
    change_password_use_case: ChangePasswordUseCaseProtocol = Depends(get_change_password_use_case),
    access_token: str = Depends(access_token_schema)
):
    """Смена пароля авторизованным пользователем"""
    user_tokens_data = await change_password_use_case(
        access_token, 
        password_data
    )
    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    return user_tokens_data.user

@router.get("/me", status_code=200)
async def get_me(
    get_me_by_user_id_use_case: GetMeByUserIdUseCaseProtocol = Depends(get_me_by_user_id_use_case),
    access_token: str = Depends(access_token_schema)
):
    return await get_me_by_user_id_use_case(access_token)

@router.post("/impersonate", response_model=UserWithPhotoReadSchema, status_code=200)
async def impersonate_user(
    response: Response,
    user_id: UserIdSchema,
    auth_by_another_user_use_case: AuthByAnotherUserUseCaseProtocol = Depends(get_auth_by_another_user_use_case),
    access_token: str = Depends(access_token_schema)
):
    user_tokens_data = await auth_by_another_user_use_case(access_token, user_id)
    
    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    
    return user_tokens_data.user

@router.post("/", response_model=UserWithPhotoReadSchema, status_code=201)
async def create_user(
    user_data: str = Form(...),
    image: Optional[UploadFile] = File(None),
    access_token: str = Depends(access_token_schema),
    create_user_use_case: CreateUserUseCaseProtocol = Depends(get_create_user_use_case)
):
    return await create_user_use_case(access_token, user_data, image)
    

@router.get("/", response_model=PaginationResultSchema[UserWithPhotoReadSchema], status_code=200)
async def get_all_users(
    access_token: str = Depends(access_token_schema),
    role: Optional[UserRole] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    get_all_users_use_case: GetAllUsersUseCaseProtocol = Depends(get_all_users_use_case)
):
    return await get_all_users_use_case(access_token, role, limit, offset)

@router.get("/{user_id}", response_model=UserWithPhotoReadSchema, status_code=200)
async def get_user_by_id(
    user_id: UUID,
    access_token: str = Depends(access_token_schema),
    get_user_by_id_use_case: GetUserByIdUseCaseProtocol = Depends(get_get_user_by_id_use_case)
):
    return await get_user_by_id_use_case(access_token, user_id)

@router.put("/{user_id}", response_model=UserWithPhotoReadSchema, status_code=200)
async def update_user(
    user_id: UUID, 
    user_data: str = Form(...),
    image: Optional[UploadFile] = File(None),
    access_token: str = Depends(access_token_schema),
    update_user_use_case: UpdateUserUseCaseProtocol = Depends(get_update_user_use_case)
):
    return await update_user_use_case(access_token, user_id, user_data, image)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    access_token: str = Depends(access_token_schema),
    delete_user_use_case: DeleteUserUseCaseProtocol = Depends(get_delete_user_use_case)
):
    await delete_user_use_case(access_token, user_id)
    return None

@router.post("/reset_password", status_code=204)
async def reset_password(
    user: UserResetSchema,
    reset_password_use_case: ResetPasswordUseCaseProtocol = Depends(get_reset_password_use_case)
):
    await reset_password_use_case(user)
    
    return None

@router.post("/confirm_reset_password", status_code=200)
async def confirm_reset_password(
    response: Response,
    passsword_request: ResetPasswordRequest,
    reset_password_use_case: ConfirmResetPasswordUseCaseProtocol = Depends(get_confirm_reset_password_use_case)
):
    user_tokens_data =  await reset_password_use_case(passsword_request)

    set_auth_cookies(
        response, 
        user_tokens_data.access_token.token, 
        user_tokens_data.refresh_token.token
    )
    return user_tokens_data.user


