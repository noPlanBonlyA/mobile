from school_site.core.utils.exceptions import ModelAlreadyExistsError, ModelNotFoundException
from typing import Any 
from .models import News
from typing import Self


class NewsAlreadyExistsError(ModelAlreadyExistsError):
    def __init__(self: Self, headers: dict[str, Any] | None = None) -> None:
        super.__init__(
        model = News,
        field = 'name',
        message = 'try another name for create',
        headers = headers
        )

class NewsNotFoundException(ModelNotFoundException):
    def __init__(sefl: Self, headers: dict[str, Any] | None = None) -> None:
        super.__init__(
        model = News, 
        headers = headers
        )