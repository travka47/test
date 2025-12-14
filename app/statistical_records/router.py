from fastapi import Depends, status, APIRouter

from app.exceptions.http_exceptions import (
    EmptyAudienceHTTPException,
    InvalidSQLHTTPException,
)
from app.statistical_records.dependencies import (
    get_statistical_record_service,
    validate_audience1,
    validate_audience2,
)
from app.statistical_records.schemas import PercentResponse
from app.statistical_records.service import StatisticalRecordService

router = APIRouter()


@router.get(
    path="/getPercent",
    status_code=status.HTTP_200_OK,
    response_model=PercentResponse,
    description="Расчёт процента вхождения второй аудитории в первую",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "examples": {
                        "empty_audience": {
                            "summary": EmptyAudienceHTTPException.description,
                            "value": {"detail": EmptyAudienceHTTPException.detail},
                        },
                        "invalid_sql": {
                            "summary": InvalidSQLHTTPException.description,
                            "value": {"detail": InvalidSQLHTTPException.detail},
                        },
                    }
                }
            }
        }
    },
)
async def get_percent_of_occurrences(
    audience1: str = Depends(validate_audience1),
    audience2: str = Depends(validate_audience2),
    service: StatisticalRecordService = Depends(get_statistical_record_service),
):
    percent = await service.get_percent_of_occurrences(
        audience1=audience1, audience2=audience2
    )

    return PercentResponse(percent=percent)
