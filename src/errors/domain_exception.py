from src.errors.codes import ErrorCode


class DomainException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str = "Request Failed",
        error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
    ):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
