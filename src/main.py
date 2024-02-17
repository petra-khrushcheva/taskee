from fastapi import FastAPI

from core.config import settings
# from роутер как правильно v1
from router import router

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)

app.include_router(router)
