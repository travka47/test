from pydantic import BaseModel


class PercentResponse(BaseModel):
    percent: float = 0.0
