from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.core.services.files import FileServiceProtocol
from school_site.core.depends import get_image_service
from school_site.apps.students.depends import get_student_by_group_service, get_students_services
from school_site.apps.students.services.students import StudentsByGroupServiceProtocol, StudentServiceProtocol
from school_site.apps.teachers.depends import get_teachers_services
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol 
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from school_site.apps.points_history.services.points_history import PointsHistoryServiceProtocol
from school_site.apps.points_history.depends import get_points_history_service
from .repositories.photo_courses import PhotoRepositoryProtocol, PhotoRepository
from .repositories.courses import CourseRepositoryProtocol, CourseRepository
from .repositories.lessons import LessonRepositoryProtocol, LessonRepository
from .repositories.lesson_html_files import LessonHTMLRepositoryProtocol, LessonHTMLRepository
from .repositories.lesson_group import LessonGroupRepositoryProtocol, LessonGroupRepository
from .repositories.lesson_student import LessonStudentRepositoryProtocol, LessonStudentRepository
from .repositories.homework_files import FileHomeworkRepositoryProtocol, FileHomeworkRepository
from .repositories.homeworks import HomeworkRepositoryProtocol, HomeworkRepository
from .repositories.lesson_student_homework import LessonStudentHomeworkRepositoryProtocol, LessonStudentHomeworkRepository
from .repositories.comments import CommentRepositoryProtocol, CommentRepository
from .repositories.course_student import CourseStudentRepositoryProtocol, CourseStudentRepository
from .repositories.comments_students import CommentStudentRepositoryProtocol, CommentStudentRepository
from .services.comments_students import CommentStudentServiceProtocol, CommentStudentService
from .services.lesson_group_student import CombinedLessonGroupStudentServiceProtocol, CombinedLessonGroupStudentService
from .services.photo_courses import PhotoServiceProtocol, PhotoService
from .services.courses import CourseServiceProtocol, CourseService
from .services.lessons import LessonServiceProtocol, LessonService, GetLessonWithMaterialsServiceProtocol, GetLessonWithMaterialsService
from .services.lesson_group import LessonGroupServiceProtocol, LessonGroupService, DeleteLessonGroupServiceProtocol, DeleteLessonGroupService
from .services.lesson_student import LessonStudentServiceProtocol, LessonStudentService, \
    GetLessonStudentByStudentAndLessonServiceProtocol, GetLessonStudentByStudentAndLessonService, GetLessonStudentsByStudentServiceProtocol, GetLessonStudentsByStudentService
from .services.lesson_html_files import LessonHTMLServiceProtocol, LessonHTMLService
from .services.homeworks_files import FileHomeworkServiceProtocol, FileHomeworkService
from .services.homeworks import HomeworkServiceProtocol, HomeworkService
from .services.lesson_student_homework import LessonStudentHomeworkServiceProtocol, LessonStudentHomeworkService
from .services.lesson_student import GetAllLessonStudentsByLessonGroupServiceProtocol, \
    GetAllLessonStudentsByLessonGroupService
from .services.lesson_student import GetDetailedLessonStudentByIdServiceProtocol, GetDetailedLessonStudentByIdService
from .services.lesson_student import LessonStudentWithStudentServiceProtocol, LessonStudentWithStudentService
from .services.comments import CommentServiceProtocol, CommentService
from .services.auth import AuthService, AuthAdminServiceProtocol
from .services.course_student import CourseStudentServiceProtocol, CourseStudentService, GetCoursesByStudentServiceProtocol, GetCoursesByStudentService
from .use_cases.courses.create_course import CreateCourseUseCaseProtocol, CreateCourseUseCase
from .use_cases.courses.update_course import UpdateCourseUseCaseProtocol, UpdateCourseUseCase
from .use_cases.courses.get_course import GetCourseUseCaseProtocol, GetCourseUseCase
from .use_cases.courses.delete_course import DeleteCourseUseCaseProtocol, DeleteCourseUseCase
from .use_cases.courses.list_courses import GetListCoursesUseCaseProtocol, GetListCoursesUseCase
from .use_cases.lessons.create_lesson import CreateLessonUseCaseProtocol, CreateLessonUseCase
from .use_cases.lessons.update_lesson import UpdateLessonUseCaseProtocol, UpdateLessonUseCase
from .use_cases.lessons.get_lesson import GetLessonUseCaseProtocol, GetLessonUseCase
from .use_cases.lessons.delete_lesson import DeleteLessonUseCaseProtocol, DeleteLessonUseCase
from .use_cases.lessons.list_lessons import GetListLessonsUseCaseProtocol, GetListLessonsUseCase
from .use_cases.materials.create_material import CreateLessonHTMLFileUseCaseProtocol, CreateLessonHTMLFileUseCase
from .use_cases.materials.update_material import UpdateLessonHTMLFileUseCaseProtocol, UpdateLessonHTMLFileUseCase
from .use_cases.materials.get_material import GetLessonHTMLFileUseCaseProtocol, GetLessonHTMLFileUseCase
from .use_cases.materials.delete_material import DeleteLessonHTMLFileUseCaseProtocol, DeleteLessonHTMLFileUseCase
from .use_cases.materials.create_material_by_text import CreateLessonHTMLFileByTextUseCaseProtocol, CreateLessonHTMLFileByTextUseCase
from .use_cases.materials.update_material_by_text import UpdateLessonHTMLFileByTextUseCaseProtocol, UpdateLessonHTMLFileByTextUseCase
from .use_cases.lesson_group_student.create_lesson_group_student import CreateLessonGroupStudentUseCaseProtocol, CreateLessonGroupStudentUseCase
from .use_cases.lesson_group_student.bulk_create_lesson_group_student import BulkCreateLessonGroupStudentUseCaseProtocol, BulkCreateLessonGroupStudentUseCase
from .use_cases.file_homeworks.create_file_homework import CreateHomeworkFileUseCaseProtocol, CreateHomeworkFileUseCase
from .use_cases.homeworks.create_homework import CreateHomeworkUseCaseProtocol, CreateHomeworkUseCase
from .use_cases.add_homework import AddHomeworkUseCaseProtocol, AddHomeworkUseCase
from .use_cases.homeworks.add_homework_to_lesson_by_text import AddHomeworkToLessonByTextUseCaseProtocol, AddHomeworkToLessonByTextUseCase
from .use_cases.comments.create_comment import CreateCommentUseCaseProtocol, CreateCommentUseCase
from .use_cases.comments.update_comment import UpdateCommentUseCaseProtocol, UpdateCommentUseCase
from .use_cases.comments.delete_comment import DeleteCommentUseCaseProtocol, DeleteCommentUseCase
from .use_cases.lesson_group.update_lesson_group import UpdateLessonGroupUseCaseProtocol, UpdateLessonGroupUseCase
from .use_cases.lesson_group.detach_group_from_lesson import DeleteLessonGroupByLessonAndGroupUseCaseProtocol, DeleteLessonGroupByLessonAndGroupUseCase
from .use_cases.lesson_group.detach_group_from_course import DeleteLessonGroupByLessonAndCourseUseCaseProtocol, DeleteLessonGroupByLessonAndCourseUseCase
from .use_cases.lessons.get_student_lesson_with_material import GetStudentMaterialUseCase, GetStudentMaterialUseCaseProtocol
from .use_cases.lessons.get_teacher_lesson_with_materials import GetTeacherMaterialUseCaseProtocol, GetTeacherMaterialUseCase
from .use_cases.lessons.get_lesson_info_teacher import GetTeacherLessonInfoUseCaseProtocol, GetTeacherLessonInfoUseCase
from .use_cases.courses_students.get_courses_for_student import GetCoursesForStudentUseCaseProtocol, GetCoursesForStudentUseCase
from .use_cases.lessons.get_all_lesson_students import GetAllLessonStudentsByLessonGroupUseCaseProtocol, GetAllLessonStudentsByLessonGroupUseCase
from .use_cases.lessons.get_teacher_lessons import GetTeacherLessonsUseCaseProtocol, GetTeacherLessonsUseCase
from .use_cases.courses_teachers.get_courses_for_teacher import GetCoursesForTeacherUseCaseProtocol, GetCoursesForTeacherUseCase
from .use_cases.lesson_group.get_by_group_id import GetByGroupIdLessonGroupUseCaseProtocol, GetByGroupIdLessonGroupUseCase
from .use_cases.lesson_students.get_detailed_student import GetDetailedLessonStudentUseCaseProtocol, GetDetailedLessonStudentUseCase
from .use_cases.lesson_students.create_ls_and_update_student import CreateLessonStudentsAndUpdateStudentsUseCaseProtocol, CreateLessonStudentsAndUpdateStudentsUseCase
from .use_cases.lesson_students.update_ls_and_update_student import UpdateLessonStudentsAndUpdateStudentsUseCaseProtocol, UpdateLessonStudentsAndUpdateStudentsUseCase
from .use_cases.lesson_students.delete_ls_and_update_student import DeleteLessonStudentsAndUpdateStudentsUseCaseProtocol, DeleteLessonStudentsAndUpdateStudentsUseCase
from .use_cases.lesson_students.get_all_by_student import GetAllLessonStudentByStudentUseCaseProtocol, GetAllLessonStudentByStudentUseCase
from .use_cases.homeworks.add_homework_to_lesson import AddHomeworkToLessonUseCaseProtocol, AddHomeworkToLessonUseCase
from .use_cases.lessons.get_lesson_info_by_teacher_id import GetTeacherLessonInfoByTeacherIdUseCaseProtocol, GetTeacherLessonInfoByTeacherIdUseCase

def get_course_file_service() -> FileServiceProtocol:
    """Зависимость для работы с изображениями продуктов."""
    return get_image_service("course-files")

def __get_photo_repository(
        session: AsyncSession = Depends(get_async_session)
) -> PhotoRepositoryProtocol:
    return PhotoRepository(session)


def __get_course_repository(
        session: AsyncSession = Depends(get_async_session)
) -> CourseRepositoryProtocol:
    return CourseRepository(session)


def __get_lesson_repository(
        session: AsyncSession = Depends(get_async_session)
) -> LessonRepositoryProtocol:
    return LessonRepository(session)

def __get_lesson_html_file_repository(
        session: AsyncSession = Depends(get_async_session)
) -> LessonHTMLRepositoryProtocol:
    return LessonHTMLRepository(session)


def __get_lesson_group_repository(
        session: AsyncSession = Depends(get_async_session)
) -> LessonGroupRepositoryProtocol:
    return LessonGroupRepository(session)

def __get_lesson_student_repository(
    session: AsyncSession = Depends(get_async_session)
) -> LessonStudentRepositoryProtocol:
    return LessonStudentRepository(session)

def __get_homework_files_repository(
    session: AsyncSession = Depends(get_async_session)
) -> FileHomeworkRepositoryProtocol:
    return FileHomeworkRepository(session)

def __get_homework_repository(
    session: AsyncSession = Depends(get_async_session)
) -> HomeworkRepositoryProtocol:
    return HomeworkRepository(session)

def __get_lesson_student_homework_repository(
    session: AsyncSession = Depends(get_async_session)
) -> LessonStudentHomeworkRepositoryProtocol:
    return LessonStudentHomeworkRepository(session)

def __get_comment_repository(
    session: AsyncSession = Depends(get_async_session)
) -> CommentRepositoryProtocol:
    return CommentRepository(session)

def __get_comment_student_repository(
    session: AsyncSession = Depends(get_async_session)
) -> CommentStudentRepositoryProtocol:
    return CommentStudentRepository(session)

def __get_course_student_repository(
    session: AsyncSession = Depends(get_async_session)
) -> CourseStudentRepositoryProtocol:   
    return CourseStudentRepository(session)

def get_course_student_service(
    course_student_repository: CourseStudentRepositoryProtocol = Depends(__get_course_student_repository),
) -> CourseStudentServiceProtocol:
    return CourseStudentService(course_student_repository)

def get_courses_by_student_service(
    course_student_repository: CourseStudentRepositoryProtocol = Depends(__get_course_student_repository),
    file_service: FileServiceProtocol = Depends(get_course_file_service)
) -> GetCoursesByStudentServiceProtocol:
    return GetCoursesByStudentService(course_student_repository, file_service)

def get_photo_service(
        photo_repository: PhotoRepositoryProtocol = Depends(__get_photo_repository),
        image_service: FileServiceProtocol = Depends(get_course_file_service)
) -> PhotoServiceProtocol:
    return PhotoService(photo_repository, image_service)

def get_course_service(
        course_repository: CourseRepositoryProtocol = Depends(__get_course_repository),
        photo_service: PhotoServiceProtocol = Depends(get_photo_service)
) -> CourseServiceProtocol:
    return CourseService(course_repository, photo_service)

def get_lesson_service(
        lesson_repository: LessonRepositoryProtocol = Depends(__get_lesson_repository)
) -> LessonServiceProtocol:
    return LessonService(lesson_repository)

def get_comment_student_service(
    comment_student_repository: CommentStudentRepositoryProtocol = Depends(__get_comment_student_repository)
) -> CommentStudentServiceProtocol:
    return CommentStudentService(comment_student_repository)

def get_detailed_lesson_student_service(
        repository: LessonStudentRepositoryProtocol = Depends(__get_lesson_student_repository),
        file_service: FileServiceProtocol = Depends(get_course_file_service)
) -> GetDetailedLessonStudentByIdServiceProtocol:
    return GetDetailedLessonStudentByIdService(repository, file_service)

def get_lesson_student_by_student_and_lesson_service(
        repository: LessonStudentRepositoryProtocol = Depends(__get_lesson_student_repository)
)-> GetLessonStudentByStudentAndLessonServiceProtocol:
    return GetLessonStudentByStudentAndLessonService(repository)

def get_auth_service(
    token_service: TokenServiceProtocol = Depends(get_token_service)
) -> AuthAdminServiceProtocol:
    return AuthService(token_service)

def get_course_create_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> CreateCourseUseCaseProtocol:
    return CreateCourseUseCase(course_service, auth_service)

def get_course_update_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateCourseUseCaseProtocol:
    return UpdateCourseUseCase(course_service, auth_service)

def get_course_get_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> GetCourseUseCaseProtocol:
    return GetCourseUseCase(course_service)

def get_course_delete_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteCourseUseCaseProtocol:
    return DeleteCourseUseCase(course_service, auth_service)

def get_course_get_list_use_case(
        course_service: CourseServiceProtocol = Depends(get_course_service)
) -> GetListCoursesUseCaseProtocol:
    return GetListCoursesUseCase(course_service)

def get_lesson_create_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> CreateLessonUseCaseProtocol:
    return CreateLessonUseCase(lesson_service, auth_service)

def get_lesson_update_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateLessonUseCaseProtocol:
    return UpdateLessonUseCase(lesson_service, auth_service)

def get_lesson_get_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service)
) -> GetLessonUseCaseProtocol:
    return GetLessonUseCase(lesson_service)

def get_lesson_delete_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteLessonUseCaseProtocol:
    return DeleteLessonUseCase(lesson_service, auth_service)

def get_lesson_get_list_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service)
) -> GetListLessonsUseCaseProtocol:
    return GetListLessonsUseCase(lesson_service)

def get_lesson_html_service(
        lesson_html_repository = Depends(__get_lesson_html_file_repository),
        file_service: FileServiceProtocol = Depends(get_course_file_service)
                            ) -> LessonHTMLServiceProtocol:
    return LessonHTMLService(lesson_html_repository, file_service)

def get_homework_files_service(
        file_service: FileServiceProtocol = Depends(get_course_file_service),
        homework_files_repository: FileHomeworkRepositoryProtocol = Depends(__get_homework_files_repository)
) -> FileHomeworkServiceProtocol:
    return FileHomeworkService(homework_files_repository, file_service)

def get_homework_service(
        homework_repository: HomeworkRepositoryProtocol = Depends(__get_homework_repository)
) -> HomeworkServiceProtocol:
    return HomeworkService(homework_repository)

def get_lesson_student_homework_service(
        repository: LessonStudentHomeworkRepositoryProtocol = Depends(__get_lesson_student_homework_repository)
) -> LessonStudentHomeworkServiceProtocol:
    return LessonStudentHomeworkService(repository)

def get_all_lesson_students_by_lesson_group_service(
    repository: LessonStudentRepositoryProtocol = Depends(__get_lesson_student_repository)
) -> GetAllLessonStudentsByLessonGroupServiceProtocol:
    return GetAllLessonStudentsByLessonGroupService(repository)

def get_all_lesson_students_by_student_service(
    repository: LessonStudentRepositoryProtocol = Depends(__get_lesson_student_repository)
) -> GetLessonStudentsByStudentServiceProtocol:
    return GetLessonStudentsByStudentService(repository)

def get_all_lesson_students_by_student_use_case(
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
    student_service: StudentServiceProtocol = Depends(get_students_services),
    lesson_student_service: GetLessonStudentsByStudentServiceProtocol = Depends(get_all_lesson_students_by_student_service),
) -> GetAllLessonStudentByStudentUseCaseProtocol:
    return GetAllLessonStudentByStudentUseCase(auth_service, student_service, lesson_student_service)

def get_lesson_student_with_student_service(
    lesson_student_repository: LessonStudentRepositoryProtocol = Depends(__get_lesson_student_repository),
    student_service: StudentServiceProtocol = Depends(get_students_services),
    history_service: PointsHistoryServiceProtocol = Depends(get_points_history_service)
) -> LessonStudentWithStudentServiceProtocol:
    return LessonStudentWithStudentService(lesson_student_repository, student_service, history_service)

def get_comment_service(
    comment_repository: CommentRepositoryProtocol = Depends(__get_comment_repository)
) -> CommentServiceProtocol:
    return CommentService(comment_repository)


def get_lesson_with_materials_service(
    lesson_repository: LessonRepositoryProtocol = Depends(__get_lesson_repository),
    file_service: FileServiceProtocol = Depends(get_course_file_service)
) -> GetLessonWithMaterialsServiceProtocol:
    return GetLessonWithMaterialsService(lesson_repository, file_service)

def get_create_comment_use_case(
    comment_service: CommentServiceProtocol = Depends(get_comment_service),
    teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> CreateCommentUseCaseProtocol:
    return CreateCommentUseCase(comment_service, teacher_service, auth_service)  

def get_update_comment_use_case(
    comment_service: CommentServiceProtocol = Depends(get_comment_service),
    teacher_service: TeacherServiceProtocol = Depends(get_teachers_services),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateCommentUseCaseProtocol:
    return UpdateCommentUseCase(comment_service, teacher_service, auth_service)  

def get_delete_comment_use_case(
    comment_service: CommentServiceProtocol = Depends(get_comment_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteCommentUseCaseProtocol:
    return DeleteCommentUseCase(comment_service, auth_service)

def get_material_create_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                 auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> CreateLessonHTMLFileUseCaseProtocol:
    return CreateLessonHTMLFileUseCase(lesson_service, auth_service)

def get_material_create_by_text_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                        ) -> CreateLessonHTMLFileByTextUseCaseProtocol:
    return CreateLessonHTMLFileByTextUseCase(lesson_service, auth_service)

def get_material_update_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                 auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> UpdateLessonHTMLFileUseCaseProtocol:
    return UpdateLessonHTMLFileUseCase(lesson_service, auth_service)

def get_material_update_by_text_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                        ) -> UpdateLessonHTMLFileByTextUseCaseProtocol:
    return UpdateLessonHTMLFileByTextUseCase(lesson_service, auth_service)

def get_material_get_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> GetLessonHTMLFileUseCaseProtocol:
    return GetLessonHTMLFileUseCase(lesson_service, auth_service)

def get_material_delete_use_case(lesson_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
                                auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                 ) -> DeleteLessonHTMLFileUseCaseProtocol:
    return DeleteLessonHTMLFileUseCase(lesson_service, auth_service)
    

def get_lesson_group_service(repository: LessonGroupRepositoryProtocol = Depends(__get_lesson_group_repository)
                              ) -> LessonGroupServiceProtocol:
    return LessonGroupService(repository)

def get_lesson_group_update_use_case(
    lesson_group_service: LessonGroupServiceProtocol = Depends(get_lesson_group_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateLessonGroupUseCaseProtocol:
    return UpdateLessonGroupUseCase(lesson_group_service, auth_service)

def get_delete_lesson_group_service(
       repository: LessonGroupRepositoryProtocol = Depends(__get_lesson_group_repository) 
) -> DeleteLessonGroupServiceProtocol:
    return DeleteLessonGroupService(repository)

def get_delete_lesson_group_by_lesson_and_group_use_case(service: DeleteLessonGroupServiceProtocol = Depends(get_delete_lesson_group_service),
                                                        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                                         ) -> DeleteLessonGroupByLessonAndGroupUseCaseProtocol:
    return DeleteLessonGroupByLessonAndGroupUseCase(service, auth_service)

def get_delete_lesson_group_by_course_and_group_use_case(service: DeleteLessonGroupServiceProtocol = Depends(get_delete_lesson_group_service),
                                                        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                                         ) -> DeleteLessonGroupByLessonAndCourseUseCaseProtocol:
    return DeleteLessonGroupByLessonAndCourseUseCase(service, auth_service)

def get_lesson_student_service(repository: LessonStudentRepositoryProtocol = Depends(__get_lesson_student_repository)
                               ) -> LessonStudentServiceProtocol:
    return LessonStudentService(repository)

def get_combined_lesson_student_group_service(lesson_group_service: LessonGroupServiceProtocol = Depends(get_lesson_group_service),
                                              lesson_student_service: LessonStudentServiceProtocol = Depends(get_lesson_student_service),
                                              course_student_service: CourseStudentServiceProtocol = Depends(get_course_student_service),
                                              lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
                                              student_service: StudentsByGroupServiceProtocol = Depends(get_student_by_group_service)
                                              ) -> CombinedLessonGroupStudentServiceProtocol:
    return CombinedLessonGroupStudentService(lesson_group_service, lesson_student_service, course_student_service, lesson_service, student_service)

def get_create_lesson_group_student_use_case(lesson_student_group_service: CombinedLessonGroupStudentService = Depends(get_combined_lesson_student_group_service),
                                             auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                             ) -> CreateLessonGroupStudentUseCaseProtocol:
    return CreateLessonGroupStudentUseCase(lesson_student_group_service, auth_service) 

def get_bulk_create_lesson_group_student_use_case(lesson_student_group_service: CombinedLessonGroupStudentService = Depends(get_combined_lesson_student_group_service),
                                             auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
                                             ) -> BulkCreateLessonGroupStudentUseCaseProtocol:
    return BulkCreateLessonGroupStudentUseCase(lesson_student_group_service, auth_service)

def get_create_homework_file_use_case(
        homework_files_service: FileHomeworkServiceProtocol = Depends(get_homework_files_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
        
) -> CreateHomeworkFileUseCaseProtocol:
    return CreateHomeworkFileUseCase(homework_files_service, auth_service)

def get_create_homework_use_case(
    homework_service: HomeworkServiceProtocol = Depends(get_homework_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)

) -> CreateHomeworkUseCaseProtocol:
    return CreateHomeworkUseCase(homework_service, auth_service)

def get_add_homework_use_case(
    file_homework_service: FileHomeworkServiceProtocol = Depends(get_homework_files_service),
    homework_service: HomeworkServiceProtocol = Depends(get_homework_service),
    lesson_student_service_by_student_and_lesson: GetLessonStudentByStudentAndLessonServiceProtocol = Depends(get_lesson_student_by_student_and_lesson_service),
    lesson_student_service: LessonStudentServiceProtocol = Depends(get_lesson_student_service),
    lesson_student_homework_service: LessonStudentHomeworkServiceProtocol = Depends(get_lesson_student_homework_service),
    student_service: StudentServiceProtocol = Depends(get_students_services),
    comment_student_service: CommentStudentServiceProtocol = Depends(get_comment_student_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> AddHomeworkUseCaseProtocol:
    return AddHomeworkUseCase(file_homework_service, homework_service, lesson_student_service_by_student_and_lesson,
                              lesson_student_service, lesson_student_homework_service, student_service, comment_student_service, auth_service)

def get_lesson_for_teacher_use_case(
    lesson_with_materials_service: GetLessonWithMaterialsServiceProtocol = Depends(get_lesson_with_materials_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
    teacher_service: TeacherServiceProtocol = Depends(get_teachers_services)
) -> GetTeacherMaterialUseCaseProtocol:
    return GetTeacherMaterialUseCase(lesson_with_materials_service, auth_service, teacher_service)

def get_lesson_for_student_use_case(
    lesson_with_materials_service: GetLessonWithMaterialsServiceProtocol = Depends(get_lesson_with_materials_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
    student_service: StudentServiceProtocol = Depends(get_students_services)
) -> GetStudentMaterialUseCaseProtocol:
    return GetStudentMaterialUseCase(lesson_with_materials_service, auth_service, student_service)

def get_teacher_lesson_info_use_case(
    lesson_with_materials_service: GetLessonWithMaterialsServiceProtocol = Depends(get_lesson_with_materials_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
    teacher_service: TeacherServiceProtocol = Depends(get_teachers_services)
) -> GetTeacherLessonInfoUseCaseProtocol:
    return GetTeacherLessonInfoUseCase(lesson_with_materials_service, auth_service, teacher_service)

def get_teacher_lesson_info_by_teacher_id_use_case(
    lesson_with_materials_service: GetLessonWithMaterialsServiceProtocol = Depends(get_lesson_with_materials_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
) -> GetTeacherLessonInfoByTeacherIdUseCaseProtocol:
    return GetTeacherLessonInfoByTeacherIdUseCase(lesson_with_materials_service, auth_service)


def get_courses_for_student_use_case(
    course_student_service: GetCoursesByStudentServiceProtocol = Depends(get_courses_by_student_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
    student_service: StudentServiceProtocol = Depends(get_students_services)
) -> GetCoursesForStudentUseCaseProtocol:
    return GetCoursesForStudentUseCase(course_student_service, auth_service, student_service)

def get_add_homework_to_lesson_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        material_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> AddHomeworkToLessonUseCaseProtocol:
    return AddHomeworkToLessonUseCase(lesson_service, material_service, auth_service)

def get_add_homework_to_lesson_by_text_use_case(
        lesson_service: LessonServiceProtocol = Depends(get_lesson_service),
        material_service: LessonHTMLServiceProtocol = Depends(get_lesson_html_service),
        auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> AddHomeworkToLessonByTextUseCaseProtocol:
    return AddHomeworkToLessonByTextUseCase(lesson_service, material_service, auth_service)

def get_teacher_lessons_use_case(
    lesson_service: GetLessonWithMaterialsServiceProtocol = Depends(get_lesson_with_materials_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> GetTeacherLessonsUseCaseProtocol:
    return GetTeacherLessonsUseCase(lesson_service, auth_service)

def get_courses_for_teacher_use_case(
    course_service: CourseServiceProtocol = Depends(get_course_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
    teacher_service: TeacherServiceProtocol = Depends(get_teachers_services)
) -> GetCoursesForTeacherUseCaseProtocol:
    return GetCoursesForTeacherUseCase(course_service, auth_service, teacher_service)

def get_by_group_id_lesson_group_use_case(
    lesson_group_service: LessonGroupServiceProtocol = Depends(get_lesson_group_service)
) -> GetByGroupIdLessonGroupUseCaseProtocol:
    return GetByGroupIdLessonGroupUseCase(lesson_group_service)

def get_all_lesson_students_by_lesson_group_use_case(
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service),
    lesson_student_service: LessonStudentServiceProtocol = Depends(get_lesson_student_service)
) -> GetAllLessonStudentsByLessonGroupUseCaseProtocol:
    return GetAllLessonStudentsByLessonGroupUseCase(lesson_student_service, auth_service)

def get_detailed_lesson_student_use_case(
    lesson_student_service: GetDetailedLessonStudentByIdServiceProtocol = Depends(get_detailed_lesson_student_service)
) -> GetDetailedLessonStudentUseCaseProtocol:
    return GetDetailedLessonStudentUseCase(lesson_student_service)

def get_create_lesson_students_and_update_students_use_case(
    lesson_student_service: LessonStudentWithStudentServiceProtocol = Depends(get_lesson_student_with_student_service)
) -> CreateLessonStudentsAndUpdateStudentsUseCaseProtocol:
    return CreateLessonStudentsAndUpdateStudentsUseCase(lesson_student_service)

def get_update_lesson_students_and_update_students_use_case(
    lesson_student_service: LessonStudentWithStudentServiceProtocol = Depends(get_lesson_student_with_student_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateLessonStudentsAndUpdateStudentsUseCaseProtocol:
    return UpdateLessonStudentsAndUpdateStudentsUseCase(lesson_student_service, auth_service)

def get_delete_lesson_students_and_update_students_use_case(
    lesson_student_service: LessonStudentWithStudentServiceProtocol = Depends(get_lesson_student_with_student_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteLessonStudentsAndUpdateStudentsUseCaseProtocol:
    return DeleteLessonStudentsAndUpdateStudentsUseCase(lesson_student_service, auth_service)

