from fastapi import APIRouter

from src.tasks.router import router as tasks_router
from src.users.router import router as users_router
from src.workspaces.router import ws_router, membership_router

router = APIRouter(prefix="/v1")
router.include_router(ws_router)
router.include_router(membership_router)
router.include_router(tasks_router)
router.include_router(users_router)
