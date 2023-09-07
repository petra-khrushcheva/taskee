from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status

from tasks.crud import TaskCRUD
from tasks.dependencies import get_tasks_crud
from tasks.models import Task, TaskCreate

tasks_router = APIRouter()


@tasks_router.post(
      "/tasks",
      response_model=Task,
      status_code=status.HTTP_201_CREATED
    )
async def create_task(
   data: TaskCreate,
   tasks: TaskCRUD = Depends(get_tasks_crud)
):
    task = await tasks.create(data=data)
    return task


@tasks_router.get(
        "/tasks/{task_uuid}",
        response_model=Task,
        status_code=status.HTTP_200_OK
    )
async def get_task(task_uuid: UUID, tasks: TaskCRUD = Depends(get_tasks_crud)):
    task = await tasks.get(task_uuid=task_uuid)
    return task


@tasks_router.get(
        "/tasks",
        response_model=list[Task],
        status_code=status.HTTP_200_OK
    )
async def get_tasks(tasks: TaskCRUD = Depends(get_tasks_crud)):
    tasks = await tasks.get_all()
    return tasks


@tasks_router.patch(
        "/tasks/{task_uuid}",
        response_model=Task,
        status_code=status.HTTP_200_OK
)
async def update_task(
    task_uuid: UUID,
    data: Task,
    tasks: TaskCRUD = Depends(get_tasks_crud)
):
    task = await tasks.patch(task_uuid=task_uuid, data=data)
    return task


@tasks_router.delete(
        "/tasks/{task_uuid}",
        status_code=status.HTTP_200_OK
)
async def delete_task(
       task_uuid: UUID,
       tasks: TaskCRUD = Depends(get_tasks_crud)
):
    status = await tasks.delete(task_uuid=task_uuid)
    return {"status": status, "message": "This task has been deleted!"}
