from typing import Union
from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from tasks.models import Task, TaskCreate


class TaskCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TaskCreate) -> Task:
        values = data.dict()
        task = Task(**values)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_uuid: Union[str, UUID]) -> Task:
        statement = select(Task).where(Task.uuid == task_uuid)
        results = await self.session.execute(statement=statement)
        task = results.scalar_one_or_none()
        if task is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="This task doesn't exist"
            )
        return task

    async def get_all(self) -> list[Task]:
        result = await self.session.execute(select(Task))
        return result.scalars().all()

    async def patch(self, task_uuid: Union[str, UUID], data: Task) -> Task:
        task = await self.get(task_uuid=task_uuid)
        values = data.dict(exclude_unset=True)
        for key, value in values.items():
            setattr(task, key, value)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_uuid: Union[str, UUID]) -> None:
        statement = delete(Task).where(Task.uuid == task_uuid)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return True
