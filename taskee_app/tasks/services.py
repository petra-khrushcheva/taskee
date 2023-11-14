from sqlalchemy import desc, select
from sqlalchemy.orm import  joinedload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.models import Task
from tasks.schemas import TaskCreate


class TaskCRUD():

    @staticmethod
    async def get_tasks(session: AsyncSession):
        stmt = (select(Task)
                .options(
                    joinedload(Task.creator),
                    joinedload(Task.executor),
                ).order_by(desc(Task.created_at)))
        result: Result = await session.execute(stmt)
        tasks = result.scalars().all()
        return tasks

    @staticmethod
    async def get_task(session: AsyncSession, id: int):
        return await session.get(Task, id)

    @staticmethod
    async def create_task(session: AsyncSession, task_data: TaskCreate):
        task = Task(**task_data.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

# добавлять создателя поста, когда будут готовы users
# new_post = Post(owner_id=current_user.id, **post.model_dump())

    @staticmethod
    async def delete_task(session: AsyncSession, task: Task):
        await session.delete(task)
        await session.commit()

    @staticmethod
    async def update_task(session: AsyncSession,
                          task: Task,
                          task_data: TaskCreate):
        for key, value in task_data.model_dump().items():
            setattr(task, key, value)
        await session.commit()
        return task
