from fastapi import FastAPI

from tasks.router import router as tasks_router
from users.router import router as users_router
from workspaces.router import router as workspace_router
from core.config import settings

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)

app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(workspace_router)
