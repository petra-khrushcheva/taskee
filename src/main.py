from fastapi import FastAPI

from src.core import settings
from src.router import router

app = FastAPI(title=settings.project_name, version=settings.project_version)

app.include_router(router)
