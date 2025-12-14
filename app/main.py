from fastapi import FastAPI

from app.database import initiate_database
from app.exceptions.exception_handlers import register_exception_handlers
from app.statistical_records.router import router as statistical_records_router

app = FastAPI(
    title="Test task API",
    lifespan=initiate_database,
)

app.include_router(statistical_records_router)
register_exception_handlers(app)


@app.get("/")
async def read_root():
    return {"message": "Test task API"}
