from school_site.core.utils.exceptions import CoreException

class FileInUseException(CoreException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Cannot delete a file because it is used in lessons"
        )