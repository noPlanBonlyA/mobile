from typing import Any, Self
from school_site.core.utils.exceptions import ModelNotFoundException, ModelAlreadyExistsError
from school_site.apps.notification.models import Notification, NotificationRecipients, ReadStatus


class NotificationNotFoundException(ModelNotFoundException):
    """Исключение, возникающее при попытке найти несуществующее уведомление."""
    def __init__(self: Self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            model=Notification,
            headers=headers
        )


class NotificationRecipientAlreadyExistsError(ModelAlreadyExistsError):
    """Исключение, возникающее при попытке добавить существующего получателя."""
    def __init__(self: Self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            model=NotificationRecipients,
            field="recipient_id",
            message="Recipient already exists for this notification",
            headers=headers
        )


class ReadStatusAlreadyExistsError(ModelAlreadyExistsError):
    """Исключение, возникающее при попытке создать существующий статус прочтения."""
    def __init__(self: Self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(
            model=ReadStatus,
            field="student_id",
            message="Read status already exists for this notification",
            headers=headers
        )