from fastapi import APIRouter

from tasks.router import router as tasks_router
from users.router import router as users_router
from workspaces.router import ws_router, membership_router

router = APIRouter()  #где то в этой строке добавить v1
router.include_router(ws_router)
router.include_router(membership_router)
router.include_router(tasks_router)
router.include_router(users_router)
