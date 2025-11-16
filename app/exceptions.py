class BookHubException(Exception):
    detail = "Неожиданная ошибка"


class ObjectNotFoundException(BookHubException):
    detail = "Объект не найден"
