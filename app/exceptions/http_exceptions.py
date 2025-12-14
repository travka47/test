from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Bad request"
    description: str | None = None

    def __init__(self, detail: str | None = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class EmptyAudienceHTTPException(CustomHTTPException):
    detail = "В первой выборке нет респондентов"
    description = "В первой выборке нет респондентов (деление на 0)"


class InvalidSQLHTTPException(CustomHTTPException):
    detail = "Некорректный SQL-запрос"
    description = "Некорректное условие в SQL-запросе"
