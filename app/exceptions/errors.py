class InvalidSQLError(Exception):
    def __init__(self, original_exception):
        message = f"Некорректный SQL-запрос: {str(original_exception)}"
        super().__init__(message)


class EmptyAudienceError(Exception):
    pass
