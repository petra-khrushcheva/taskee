from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.tasks.dependencies import (get_ws_task_by_id,
                                    is_ws_admin_or_task_creator)
from src.tasks.schemas import (TaskCreate, TaskRead, TaskUpdate,
                               TaskWithExecutor)
from src.tasks.services import TaskCRUD
from src.users.schemas import UserRead
from src.workspaces.dependencies import (is_user_in_workspace, is_ws_admin,
                                         is_ws_user)

"""Router for task's CRUD"""
router = APIRouter(prefix="/workspaces/{ws_id}/tasks", tags=["Tasks"])


@router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=TaskWithExecutor
    )
async def create_task(
    ws_id: UUID,
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: UserRead = Depends(is_ws_user),
):
    """
    Route for creating a task inside a workspace.
    Avaliable for workspace members with statuses "admin" and "user".
    """
    if task_data.executor_id is not None:
        await is_user_in_workspace(
            user_id=task_data.executor_id, ws_id=ws_id, session=session
        )
    return await TaskCRUD.create_task(
        session=session,
        task_data=task_data,
        current_user=current_user,
        ws_id=ws_id
    )


@router.get(
        "/{task_id}",
        response_model=TaskWithExecutor,
        dependencies=[Depends(is_ws_user)]
    )
async def get_task(task: TaskRead = Depends(get_ws_task_by_id)):
    """
    Route for retrieving a single task.
    Avaliable for any member of its workspace.
    """
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
    """
    Route for deleting a task.
    Avaliable for workspace admin or task creator.
    """
    return await TaskCRUD.delete_task(session=session, task=task)


@router.put(
        "/{task_id}",
        status_code=status.HTTP_200_OK,
        response_model=TaskWithExecutor,
        dependencies=[Depends(is_ws_admin)],
    )
async def update_task(
    ws_id: UUID,
    task_data: TaskUpdate,
    task: TaskRead = Depends(get_ws_task_by_id),
    session: AsyncSession = Depends(get_session),
):
    """
    Route for updating task information, including status and executor_id.
    Avaliable for workspace admin.
    """
    if task_data.executor_id is not None:
        await is_user_in_workspace(
            user_id=task_data.executor_id, ws_id=ws_id, session=session
        )
    return await TaskCRUD.update_task(
        session=session, task=task, task_data=task_data
    )
