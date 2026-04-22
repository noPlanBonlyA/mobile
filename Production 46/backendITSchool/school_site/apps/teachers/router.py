from fastapi import APIRouter, Depends, Path, Query
from uuid import UUID
from school_site.apps.users.depends import access_token_schema
from .schemas import (
    TeacherReadSchema, TeacherCreateSchema, TeacherUpdateSchema,
    TeacherReadWithUserSchema, TeacherPaginationWithUserAndUserPhotoResultSchema
)
from .use_cases.create_teacher import CreateTeacherUseCaseProtocol
from .use_cases.update_teacher import UpdateTeacherUseCaseProtocol
from .use_cases.delete_teacher import DeleteTeacherUseCaseProtocol
from .use_cases.get_teacher import GetTeacherUseCaseProtocol
from .use_cases.list_teacher import GetListTeacherUseCaseProtocol
from .use_cases.get_me_teacher import GetMeTeacherUseCaseProtocol
from .depends import (
    get_teacher_create_use_case, get_teacher_update_use_case, get_teacher_delete_use_case,
    get_teacher_get_use_case, get_teacher_list_use_case, get_teacher_get_me_use_case
)

router = APIRouter(prefix='/api/teachers', tags=['Teachers'])

@router.post("/", response_model=TeacherReadSchema)
async def create_teacher(
    teacher: TeacherCreateSchema,
    access_token: str = Depends(access_token_schema),
    create: CreateTeacherUseCaseProtocol = Depends(get_teacher_create_use_case)
):
    return await create(access_token, teacher)

@router.put("/{teacher_id}", response_model=TeacherReadSchema)
async def update_teacher(
    teacher: TeacherUpdateSchema,
    teacher_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    update: UpdateTeacherUseCaseProtocol = Depends(get_teacher_update_use_case)
):
    return await update(access_token, teacher_id, teacher)


@router.delete("/{teacher_id}", status_code=204)
async def delete_teacher(
    teacher_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    delete: DeleteTeacherUseCaseProtocol = Depends(get_teacher_delete_use_case)
):
    await delete(access_token, teacher_id)

    return None


@router.get("/me", response_model=TeacherReadWithUserSchema)
async def get_me(
    access_token: str = Depends(access_token_schema),
    get_me: GetMeTeacherUseCaseProtocol = Depends(get_teacher_get_me_use_case)
):
    return await get_me(access_token)

@router.get("/{teacher_id}", response_model=TeacherReadWithUserSchema)
async def get_teacher(
    teacher_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    get: GetTeacherUseCaseProtocol = Depends(get_teacher_get_use_case)
):
    return await get(access_token, teacher_id)


@router.get("/", response_model=TeacherPaginationWithUserAndUserPhotoResultSchema)
async def list_teachers(
    access_token: str = Depends(access_token_schema),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    list: GetListTeacherUseCaseProtocol = Depends(get_teacher_list_use_case)
):
    return await list(access_token, limit, offset) 