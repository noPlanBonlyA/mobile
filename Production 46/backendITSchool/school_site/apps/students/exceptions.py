from typing import Any
from school_site.core.utils.exceptions import ModelFieldNotFoundException
from .models import Student


class StudentNotExistsExceptions(ModelFieldNotFoundException):
    """
    Исключение, возникающее при поиске несуществующего username.
    """
    def __init__(
            self,
            value: Any,
            headers: dict[str, Any] | None = None
    ) -> None:
       super().__init__(
            model=Student,
            field="username",
            value=value,
            headers=headers,
        )