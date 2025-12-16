from decimal import Decimal

from pydantic import BaseModel, field_serializer


class PercentResponse(BaseModel):
    percent: Decimal

    @field_serializer('percent')
    def normalize_percent(self, percent: Decimal):
        return percent.normalize()
