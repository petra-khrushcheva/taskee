from fastapi import FastAPI

from src.core.config import settings
from src.router.api_v1 import router

app = FastAPI(title=settings.project_name, version=settings.project_version)

app.include_router(router)
