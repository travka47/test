from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import InvalidSQLError, EmptyAudienceError, EmptyListError


class StatisticalRecordService:
    """Сервис для работы с данными статистических записей"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_sum_of_respondents_average_weights(
        self, audiences: list[str]
    ) -> Decimal:
        """
        Получает сумму средних весов респондентов для заданной выборки

        :param audiences: список SQL-условий для фильтрации аудитории (применяются все условия)
        :return: Сумма средних весов респондентов
        :raises EmptyListError: Если список audiences пустой
        :raises InvalidSQLError: Если SQL-запрос некорректен
        """
        if not audiences:
            raise EmptyListError()
        if len(audiences) == 1:
            condition = audiences[0]
        else:
            condition = " AND ".join([f"({audience})" for audience in audiences])

        statement = text(
            f"""
            WITH respondents_average_weights AS (
                SELECT AVG(weight) as average_weight
                FROM statistical_records
                WHERE {condition}
                GROUP BY respondent
            )
            SELECT SUM(average_weight)
            FROM respondents_average_weights
            """
        )

        try:
            result = await self.session.execute(statement)
            total = result.scalar_one_or_none()
        except Exception as e:
            raise InvalidSQLError(original_exception=e)

        return total if total else Decimal(0)

    async def get_percent_of_occurrences(self, audience1: str, audience2: str) -> Decimal:
        """
        Вычисляет процент вхождения второй аудитории в первую

        :param audience1: SQL-условие для первой аудитории
        :param audience2: SQL-условие для второй аудитории
        :return: Процент вхождения (от 0.0 до 1.0)
        :raises InvalidSQLError: Если SQL-запрос некорректен
        :raises EmptyAudienceError: Если в первой выборке нет респондентов
        """
        sum_respondents1 = await self.get_sum_of_respondents_average_weights(
            audiences=[audience1]
        )

        sum_common = await self.get_sum_of_respondents_average_weights(
            audiences=[audience1, audience2]
        )

        if sum_respondents1 == 0:
            raise EmptyAudienceError()

        percent = sum_common / sum_respondents1

        return percent
