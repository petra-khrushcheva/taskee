from tasks import schemas
from tasks.models import Task
from sqlalchemy import select, desc
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tasks(session: AsyncSession):
    stmt = select(Task).order_by(desc(Task.created_at))
    result: Result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def get_task(session: AsyncSession, id: int):
    return await session.get(Task, id)


async def create_task(session: AsyncSession, post_data: schemas.TaskCreate):
    task = Task(**post_data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

# добавлять создателя поста, когда будут готовы users
# new_post = Post(owner_id=current_user.id, **post.model_dump())


async def delete_task(session: AsyncSession, task: Task):
    await session.delete(task)
    await session.commit()


async def update_task(session: AsyncSession,
                      task: Task,
                      task_data: schemas.TaskCreate):
    for key, value in task_data.model_dump().items():
        setattr(task, key, value)
    await session.commit()
    return task
