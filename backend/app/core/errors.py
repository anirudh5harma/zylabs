from fastapi import HTTPException, status


class AppError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    pass


class InvalidStateError(AppError):
    pass


def to_http_error(error: AppError) -> HTTPException:
    if isinstance(error, NotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": error.code, "message": error.message},
        )
    if isinstance(error, InvalidStateError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": error.code, "message": error.message},
        )
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"code": error.code, "message": error.message},
    )

