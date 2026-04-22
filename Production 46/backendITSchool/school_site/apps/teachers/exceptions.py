from typing import Any
from school_site.core.utils.exceptions import ModelFieldNotFoundException
from .models import Teacher


class TeacherNotExistsExceptions(ModelFieldNotFoundException):
    """
    Исключение, возникающее при поиске несуществующего username.
    """
    def __init__(
            self,
            value: Any,
            headers: dict[str, Any] | None = None
    ) -> None:
       super().__init__(
            model=Teacher,
            field="username",
            value=value,
            headers=headers,
        ) 