from fastapi import FastAPI

from app.database import initiate_database

app = FastAPI(
    title="Test task API",
    lifespan=initiate_database,
)


@app.get("/")
async def read_root():
    return {"message": "Test task API"}
