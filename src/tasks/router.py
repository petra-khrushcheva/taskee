from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from tasks.dependencies import get_ws_task_by_id, is_ws_admin_or_task_creator
from tasks.schemas import TaskRead, TaskCreate
from tasks.services import TaskCRUD
from workspaces.dependencies import is_ws_user, is_ws_admin
from users.schemas import UserRead

router = APIRouter(prefix="/workspaces/{ws_id}/tasks", tags=["Tasks"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskRead)
async def create_task(
    ws_id: UUID,
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: UserRead = Depends(is_ws_user),
):
    return await TaskCRUD.create_task(
        session=session,
        task_data=task_data,
        current_user=current_user,
        ws_id=ws_id
    )


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task: TaskRead = Depends(get_ws_task_by_id)):
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(is_ws_admin_or_task_creator)],
)
async def delete_task(
    task: TaskRead = Depends(get_ws_task_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await TaskCRUD.delete_task(session=session, task=task)


@router.put(
        "/{task_id}",
        status_code=status.HTTP_200_OK,
        response_model=TaskRead,
        dependencies=[Depends(is_ws_admin)],
    )
async def update_task(
    task_data: TaskCreate,
    task: TaskRead = Depends(get_ws_task_by_id),
    session: AsyncSession = Depends(get_session),
):
    return await TaskCRUD.update_task(
        session=session, task=task, task_data=task_data
    )
