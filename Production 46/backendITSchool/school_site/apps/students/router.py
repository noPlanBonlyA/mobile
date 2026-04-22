from fastapi import APIRouter, Depends, Path, Query
from uuid import UUID
from .schemas import (
    StudentReadSchema, StudentCreateSchema, StudentUpdateSchema,
    StudentReadWithUserAndUsePhotoSchema,
    StudentPaginationWithUserAndUserPhotoResultSchema
)
from .use_cases.create_student import CreateStudentUseCaseProtocol
from .use_cases.update_student import UpdateStudentUseCaseProtocol
from .use_cases.delete_student import DeleteStudentUseCaseProtocol
from .use_cases.get_student import GetStudentUseCaseProtocol
from .use_cases.list_student import GetListStudentUseCaseProtocol
from .use_cases.get_me_student import GetMeStudentUseCaseProtocol
from .depends import (
    get_student_create_use_case, get_student_update_use_case, get_student_delete_use_case,
    get_student_get_use_case, get_student_list_use_case, get_student_get_me_use_case
)
from school_site.apps.users.depends import access_token_schema

router = APIRouter(prefix='/api/students', tags=['Students'])

@router.post("/", response_model=StudentReadSchema)
async def create_student(
    student: StudentCreateSchema,
    access_token: str = Depends(access_token_schema),
    create: CreateStudentUseCaseProtocol = Depends(get_student_create_use_case)
):
    return await create(access_token, student)

@router.put("/{student_id}", response_model=StudentReadSchema)
async def update_student(
    student: StudentUpdateSchema,
    student_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    update: UpdateStudentUseCaseProtocol = Depends(get_student_update_use_case)
):
    return await update(access_token, student_id, student)


@router.delete("/{student_id}", status_code=204)
async def delete_student(
    student_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    delete: DeleteStudentUseCaseProtocol = Depends(get_student_delete_use_case)
):
    await delete(access_token, student_id)

    return None

@router.get("/me", response_model=StudentReadWithUserAndUsePhotoSchema)
async def get_me(
    access_token: str = Depends(access_token_schema),
    get_me: GetMeStudentUseCaseProtocol = Depends(get_student_get_me_use_case)
):
    return await get_me(access_token)

@router.get("/{student_id}", response_model=StudentReadWithUserAndUsePhotoSchema)
async def get_student(
    student_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    get: GetStudentUseCaseProtocol = Depends(get_student_get_use_case)
):
    return await get(access_token, student_id)


@router.get("/", response_model=StudentPaginationWithUserAndUserPhotoResultSchema)
async def list_students(
    access_token: str = Depends(access_token_schema),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    sorting_by: str = Query("created_at", description="Field to sort by, default is 'created_at'"),
    list: GetListStudentUseCaseProtocol = Depends(get_student_list_use_case)
):
    return await list(access_token, limit, offset, sorting_by)


