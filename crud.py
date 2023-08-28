from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select
import tasks.models as models
import schemas


async def get_task(db: Session, task_id: UUID):
    return db.query(models.Task).filter(models.Task.uuid == task_id).first()


async def create_task(db: Session, item: schemas.TaskCreateSchema):
    task = models.Task(**item.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_tasks(db: Session):
    result = await db.execute(select(models.Task))
    tasks = result.scalars().all()
    return tasks


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(
# email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
