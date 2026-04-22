"""
Основной модуль для роутов приложения.
"""

from fastapi import FastAPI

from school_site.apps.users.router import router as users_router
from school_site.apps.products.router import router as product_router
from school_site.apps.students.router import router as student_router
from school_site.apps.teachers.router import router as teacher_router
from school_site.apps.courses.router import router as courses_router
from school_site.apps.news.router import router as news_router
from school_site.apps.notification.router import router as notification_router
from school_site.apps.groups.router import router as groups_router
from school_site.apps.schedule.router import router as schedule_router
from school_site.apps.events.router import router as events_router
from school_site.apps.points_history.router import router as points_history_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Применяем роуты приложения.
    """

    app.include_router(users_router)
    app.include_router(product_router)
    app.include_router(student_router)
    app.include_router(courses_router)
    app.include_router(news_router)
    app.include_router(notification_router)
    app.include_router(groups_router)
    app.include_router(teacher_router)
    app.include_router(events_router)
    app.include_router(schedule_router)
    app.include_router(points_history_router)

    return app