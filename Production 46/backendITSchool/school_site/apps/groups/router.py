from fastapi import APIRouter, Depends, Path, Query
from uuid import UUID
from school_site.apps.users.depends import access_token_schema
from .use_cases.create_group import CreateGroupUseCaseProtocol
from .use_cases.update_group import UpdateGroupUseCaseProtocol
from .use_cases.get_group import GetGroupUseCaseProtocol
from .use_cases.delete_group import DeleteGroupUseCaseProtocol
from .use_cases.list_groups import GetListGroupsUseCaseProtocol
from .use_cases.add_students import AddStudentsUseCaseProtocol
from .use_cases.delete_student import DeleteStudentUseCaseProtocol
from .use_cases.add_teacher import AddTeacherUseCaseProtocol
from .use_cases.delete_teacher import DeleteTeacherUseCaseProtocol
from .use_cases.get_for_teacher import GetGroupForTeacherUseCaseProtocol
from .use_cases.get_for_student import GetGroupForStudentUseCaseProtocol
from .depends import (
    get_group_create_use_case, get_group_update_use_case, get_group_get_use_case,
    get_group_delete_use_case, get_group_get_list_use_case,
    get_add_students_use_case, get_delete_student_use_case,
    get_add_teacher_use_case, get_delete_teacher_use_case,
    get_group_for_teacher_use_case, get_group_for_student_use_case
)
from .schemas import (
    GroupReadSchema, GroupPaginationResultSchema, GroupCreateSchema, 
    GroupUpdateSchema, GroupAddStudentsSchema, GroupReadStudentsSchema, GroupReadTeacherSchema,
    GroupWithStudentsAndTeacherAndCoursesSchema, GroupsForStudentReadSchema
)

router = APIRouter(prefix='/api/groups', tags=['Groups'])


@router.post("/", response_model=GroupReadSchema, status_code=201)
async def create_group(
    group_data: GroupCreateSchema,
    access_token: str = Depends(access_token_schema),
    create: CreateGroupUseCaseProtocol = Depends(get_group_create_use_case)
):
    created_group = await create(access_token, group_data)
    return created_group

@router.get("/teacher", response_model=list[GroupReadTeacherSchema], status_code=200)
async def get_group_for_teacher(
    access_token: str = Depends(access_token_schema),
    get: GetGroupForTeacherUseCaseProtocol = Depends(get_group_for_teacher_use_case)
):
    group = await get(access_token)
    return group

@router.get("/student", response_model=list[GroupsForStudentReadSchema], status_code=200)
async def get_group_for_student(
    access_token: str = Depends(access_token_schema),
    get: GetGroupForStudentUseCaseProtocol = Depends(get_group_for_student_use_case)
):
    groups = await get(access_token)
    return groups

@router.put("/{group_id}", response_model=GroupReadSchema, status_code=200)
async def update_group(
    group_data: GroupUpdateSchema,
    group_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    update: UpdateGroupUseCaseProtocol = Depends(get_group_update_use_case)
):
    updated_group = await update(access_token, group_id, group_data)
    return updated_group


@router.get("/{group_id}", response_model=GroupWithStudentsAndTeacherAndCoursesSchema, status_code=200)
async def get_group(
    group_id: UUID = Path(...),
    get: GetGroupUseCaseProtocol = Depends(get_group_get_use_case)
):
    group = await get(group_id)
    return group


@router.get("/", response_model=GroupPaginationResultSchema, status_code=200)
async def list_groups(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100),
    list: GetListGroupsUseCaseProtocol = Depends(get_group_get_list_use_case)
):
    groups = await list(limit, offset)
    return groups


@router.delete("/{group_id}", status_code=204)
async def delete_group(
    group_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    delete: DeleteGroupUseCaseProtocol = Depends(get_group_delete_use_case)
):
    await delete(access_token, group_id)
    return None


@router.post("/{group_id}/students/", response_model=GroupReadStudentsSchema, status_code=200)
async def add_students(
    students: GroupAddStudentsSchema,
    group_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    add: AddStudentsUseCaseProtocol = Depends(get_add_students_use_case)
):
    updated_group = await add(access_token, group_id, students)
    return updated_group


@router.delete("/{group_id}/students/{student_id}", status_code=204)
async def delete_student(
    group_id: UUID = Path(...),
    student_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    delete: DeleteStudentUseCaseProtocol = Depends(get_delete_student_use_case)
):
    await delete(access_token, group_id, student_id)
    return None


@router.post("/{group_id}/teacher/{teacher_id}", response_model=GroupReadTeacherSchema, status_code=200)
async def add_teacher(
    group_id: UUID = Path(...),
    teacher_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    add: AddTeacherUseCaseProtocol = Depends(get_add_teacher_use_case)
):
    updated_group = await add(access_token, group_id, teacher_id)
    return updated_group


@router.delete("/{group_id}/teacher/{teacher_id}", status_code=204)
async def delete_teacher(
    group_id: UUID = Path(...),
    teacher_id: UUID = Path(...),
    access_token: str = Depends(access_token_schema),
    delete: DeleteTeacherUseCaseProtocol = Depends(get_delete_teacher_use_case)
):
    await delete(access_token, group_id, teacher_id)
    return None
