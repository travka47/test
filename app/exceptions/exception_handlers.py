from fastapi import FastAPI

from app.exceptions.errors import EmptyAudienceError, InvalidSQLError
from app.exceptions.http_exceptions import (
    InvalidSQLHTTPException,
    EmptyAudienceHTTPException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EmptyAudienceError)
    async def empty_audience_handler(request, exc: EmptyAudienceError):
        raise EmptyAudienceHTTPException()

    @app.exception_handler(InvalidSQLError)
    async def invalid_sql_syntax_handler(request, exc: InvalidSQLError):
        raise InvalidSQLHTTPException(detail=str(exc))
