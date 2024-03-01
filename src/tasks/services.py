from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.tasks.models import Task
from src.tasks.schemas import TaskCreate
from src.users.models import User


class TaskCRUD():

    @staticmethod
    async def create_task(
        session: AsyncSession,
        task_data: TaskCreate,
        current_user: User,
        ws_id: UUID
    ):
        task = Task(
            creator_id=current_user.id,
            workspace_id=ws_id,
            **task_data.model_dump()
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        stmt = (
            select(Task)
            .options(joinedload(Task.executor))
            .filter_by(id=task.id)
        )
        new_task = await session.execute(stmt)
        return new_task.scalar_one()

    @staticmethod
    async def get_ws_task(session: AsyncSession, ws_id: UUID, task_id: UUID):
        stmt = (
            select(Task)
            .options(
                joinedload(Task.executor),
            ).where(
                Task.id == task_id,
                Task.workspace_id == ws_id
            )
        )
        task: Result = await session.execute(stmt)
        return task.scalar_one_or_none()

    @staticmethod
    async def delete_task(session: AsyncSession, task: Task):
        # task.is_active = False
        await session.delete(task)
        await session.commit()

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task: Task,
        task_data: TaskCreate
    ):
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        await session.commit()
        await session.refresh(task)
        return task
