from fastapi import status
from school_site.core.utils.exceptions import CoreException
from typing import Any
class ImageUploadError(CoreException):
    """
    Исключение, возникающее при ошибке загрузки изображения.
    """
    def __init__(
        self,
        detail: str = "Failed to upload image",
        headers: dict[str, Any] | None = None
    ) -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, headers=headers)
