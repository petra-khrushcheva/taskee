from typing import List

import tasks.schemas as schemas
from database import get_session
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from tasks import services
from tasks.dependencies import get_task_by_id
from tasks.models import Task

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks']
)


@router.get('/', response_model=List[schemas.Task])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    return await services.get_tasks(session=session)


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.Task)
async def create_task(task_data: schemas.TaskCreate,
                      session: AsyncSession = Depends(get_session)):
    return await services.create_task(session=session, task_data=task_data)


@router.get('/{id}', response_model=schemas.Task)
async def get_task(
        task: Task = Depends(get_task_by_id)
):
    return task


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: Task = Depends(get_task_by_id),
    session: AsyncSession = Depends(get_session)
):
    await services.delete_task(session=session, task=task)


@router.put('/{id}',
            status_code=status.HTTP_200_OK,
            response_model=schemas.Task)
async def update_task(task_data: schemas.TaskCreate,
                      task: Task = Depends(get_task_by_id),
                      session: AsyncSession = Depends(get_session)):
    await services.update_task(session=session, task=task, task_data=task_data)
