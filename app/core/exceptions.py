from fastapi import HTTPException


class BookHubException(Exception):
    detail = "Неожиданная ошибка"


class ObjectNotFoundException(BookHubException):
    detail = "Объект не найден"


class BookHubHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundHTTPException(BookHubHTTPException):
    status_code = 404
    detail = "Объект не найден"
