from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from .services.auth import AuthService, AuthAdminServiceProtocol
from .repositories.groups import GroupRepositoryProtocol, GroupRepository
from .repositories.group_students import GroupStudentsRepositoryProtocol, GroupStudentsRepository
from .services.groups import GroupServiceProtocol, GroupService
from .services.group_students import GroupStudentServiceProtocol, GroupStudentService
from .use_cases.create_group import CreateGroupUseCaseProtocol, CreateGroupUseCase
from .use_cases.update_group import UpdateGroupUseCaseProtocol, UpdateGroupUseCase
from .use_cases.get_group import GetGroupUseCaseProtocol, GetGroupUseCase
from .use_cases.delete_group import DeleteGroupUseCaseProtocol, DeleteGroupUseCase
from .use_cases.list_groups import GetListGroupsUseCaseProtocol, GetListGroupsUseCase
from .use_cases.add_students import AddStudentsUseCaseProtocol, AddStudentsUseCase
from .use_cases.delete_student import DeleteStudentUseCaseProtocol, DeleteStudentUseCase
from .use_cases.get_for_teacher import GetGroupForTeacherUseCaseProtocol, GetGroupForTeacherUseCase
from .use_cases.get_for_student import GetGroupForStudentUseCaseProtocol, GetGroupForStudentUseCase
from school_site.apps.students.services.students import StudentServiceProtocol
from school_site.apps.students.depends import get_students_services
from .repositories.group_teachers import GroupTeachersRepositoryProtocol, GroupTeachersRepository
from .services.group_teachers import GroupTeacherServiceProtocol, GroupTeacherService
from .use_cases.add_teacher import AddTeacherUseCaseProtocol, AddTeacherUseCase
from .use_cases.delete_teacher import DeleteTeacherUseCaseProtocol, DeleteTeacherUseCase
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from school_site.apps.teachers.depends import get_teachers_services
from school_site.apps.courses.services.lesson_group import LessonGroupServiceProtocol
from school_site.apps.courses.services.lesson_student import LessonStudentServiceProtocol
from school_site.apps.courses.services.course_student import CourseStudentServiceProtocol
from school_site.apps.courses.depends import get_lesson_group_service, get_lesson_student_service, get_course_student_service
from school_site.apps.courses.services.lessons import LessonServiceProtocol
from school_site.apps.courses.depends import get_lesson_service

def get_auth_service(
    token_service: TokenServiceProtocol = Depends(get_token_service)
) -> AuthAdminServiceProtocol:
    return AuthService(token_service)

def __get_group_repository(
        session: AsyncSession = Depends(get_async_session)
) -> GroupRepositoryProtocol:
    return GroupRepository(session)

def __get_group_students_repository(
        session: AsyncSession = Depends(get_async_session)
) -> GroupStudentsRepositoryProtocol:
    return GroupStudentsRepository(session)

def __get_group_teachers_repository(
        session: AsyncSession = Depends(get_async_session)
) -> GroupTeachersRepositoryProtocol:
    return GroupTeachersRepository(session)

def get_group_service(
        group_repository: GroupRepositoryProtocol = Depends(__get_group_repository)
) -> GroupServiceProtocol:
    return GroupService(group_repository)

def get_group_student_service(
    group_students_repository: GroupStudentsRepositoryProtocol = Depends(__get_group_students_repository),
    student_service: StudentServiceProtocol = Depends(get_students_services),
    group_service: GroupServiceProtocol = Depends(get_group_service),
    lesson_group_service: LessonGroupServiceProtocol = Depends(get_lesson_group_service),
    lesson_student_service: LessonStudentServiceProtocol = Depends(get_lesson_student_service),
    course_student_service: CourseStudentServiceProtocol = Depends(get_course_student_service),
    lesson_service: LessonServiceProtocol = Depends(get_lesson_service)
) -> GroupStudentServiceProtocol:
    return GroupStudentService(
        group_students_repository,
        group_service,
        student_service,
        lesson_group_service,
        lesson_student_service,
        course_student_service,
        lesson_service
    )

def get_group_teacher_service(
    group_teachers_repository: GroupTeachersRepositoryProtocol = Depends(__get_group_teachers_repository),
    teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
    group_service: GroupServiceProtocol = Depends(get_group_service)
) -> GroupTeacherServiceProtocol:
    return GroupTeacherService(group_teachers_repository, group_service, teacher_service)

def get_group_create_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> CreateGroupUseCaseProtocol:
    return CreateGroupUseCase(auth_service, group_service)

def get_group_update_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> UpdateGroupUseCaseProtocol:
    return UpdateGroupUseCase(auth_service, group_service)

def get_group_get_use_case(
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> GetGroupUseCaseProtocol:
    return GetGroupUseCase(group_service)

def get_group_delete_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> DeleteGroupUseCaseProtocol:
    return DeleteGroupUseCase(auth_service, group_service)

def get_group_get_list_use_case(
        group_service: GroupServiceProtocol = Depends(get_group_service)
) -> GetListGroupsUseCaseProtocol:
    return GetListGroupsUseCase(group_service)

def get_add_students_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        student_service: GroupStudentServiceProtocol = Depends(get_group_student_service)
) -> AddStudentsUseCaseProtocol:
    return AddStudentsUseCase(auth_service, student_service)

def get_delete_student_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        student_service: GroupStudentServiceProtocol = Depends(get_group_student_service)
) -> DeleteStudentUseCaseProtocol:
    return DeleteStudentUseCase(auth_service, student_service)

def get_add_teacher_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        teacher_service: GroupTeacherServiceProtocol = Depends(get_group_teacher_service)
) -> AddTeacherUseCaseProtocol:
    return AddTeacherUseCase(auth_service, teacher_service)

def get_delete_teacher_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        teacher_service: GroupTeacherServiceProtocol = Depends(get_group_teacher_service)
) -> DeleteTeacherUseCaseProtocol:
    return DeleteTeacherUseCase(auth_service, teacher_service)

def get_group_for_teacher_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        group_service: GroupTeacherServiceProtocol = Depends(get_group_teacher_service),
        teacher_service: TeacherServiceProtocol = Depends(get_teachers_services)
) -> GetGroupForTeacherUseCaseProtocol:
    return GetGroupForTeacherUseCase(group_service, teacher_service, auth_service)

def get_group_for_student_use_case(
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
        group_service: GroupStudentServiceProtocol = Depends(get_group_student_service),
        student_service: StudentServiceProtocol = Depends(get_students_services)
) -> GetGroupForStudentUseCaseProtocol:
    return GetGroupForStudentUseCase(group_service, student_service, auth_service)