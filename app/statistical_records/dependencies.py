from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.exceptions.errors import InvalidSQLError
from app.statistical_records.service import StatisticalRecordService


def validate_audience_string(audience: str) -> str:
    """
    Валидация SQL-условия для защиты от SQL-инъекций

    :param audience: SQL-условие для фильтрации аудитории
    :return: SQL-условие
    :raises InvalidSQLError: Если обнаружены запрещённые символы или команды
    """
    dangerous = [
        ";",
        "--",
        "/*",
        "*/",
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "CREATE",
        "ALTER",
        "EXEC",
        "EXECUTE",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
    ]

    for danger in dangerous:
        if danger in audience.upper():
            raise InvalidSQLError(
                f"Запрещённые символы или команды в запросе: '{danger}'"
            )

    return audience


def validate_audience1(
    audience1: str = Query(
        ...,
        example="age BETWEEN 18 AND 35",
        description="SQL условие для первой аудитории",
    ),
) -> str:
    return validate_audience_string(audience1)


def validate_audience2(
    audience2: str = Query(
        ...,
        example="sex = 2 AND age >= 18",
        description="SQL условие для второй аудитории",
    ),
) -> str:
    return validate_audience_string(audience2)


def get_statistical_record_service(
    session: AsyncSession = Depends(get_async_session),
) -> StatisticalRecordService:
    return StatisticalRecordService(session)
