from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.errors import InvalidSQLError, EmptyAudienceError


class StatisticalRecordService:
    """Сервис для работы с данными статистических записей"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_respondents_with_average_weight(
        self, audience: str
    ) -> dict[int, float]:
        """
        Получает респондентов со средним весом каждого для заданной выборки

        :param audience: SQL-условие для фильтрации аудитории
        :return: Словарь {respondent: average_weight}
        :raises InvalidSQLError: Если SQL-запрос некорректен
        """
        statement = text(
            f"SELECT respondent, AVG(weight) as average_weight FROM statistical_records WHERE {audience} GROUP BY respondent"
        )

        try:
            result = await self.session.execute(statement)
        except Exception as e:
            raise InvalidSQLError(original_exception=e)

        return {row.respondent: row.average_weight for row in result.mappings().all()}

    async def get_percent_of_occurrences(self, audience1: str, audience2: str) -> float:
        """
        Вычисляет процент вхождения второй аудитории в первую

        :param audience1: SQL-условие для первой аудитории
        :param audience2: SQL-условие для второй аудитории
        :return: Процент вхождения (от 0.0 до 1.0)
        :raises InvalidSQLError: Если SQL-запрос некорректен
        :raises EmptyAudienceError: Если в первой выборке нет респондентов
        """
        respondents1 = await self.get_respondents_with_average_weight(
            audience=audience1
        )
        respondents2 = await self.get_respondents_with_average_weight(
            audience=audience2
        )

        common_respondents_keys = set(respondents1.keys()) & set(respondents2.keys())

        average_weight_for_common_respondents = sum(
            respondents1[key] for key in common_respondents_keys
        )
        average_weight_for_respondents1 = sum(respondents1.values())

        if average_weight_for_respondents1 == 0:
            raise EmptyAudienceError()

        percent = (
            average_weight_for_common_respondents / average_weight_for_respondents1
        )

        return percent
