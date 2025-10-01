from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.restaurant import router as restaurant_router


app = FastAPI(title=settings.project_name, version=settings.version)


app.include_router(health_router, prefix="/api/v1")
app.include_router(restaurant_router, prefix="/api/v1/restaurant")


@app.get("/")
def root():
    return {"message": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)


