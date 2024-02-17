from fastapi import FastAPI

from core.config import settings
from router.api_v1 import router

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)

app.include_router(router)
