import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks/", response_model=list[schemas.TaskSchema])
def read_items(db: Session = Depends(get_db)):
    items = crud.get_tasks(db)
    return items


@app.post("/tasks/", response_model=schemas.TaskSchema)
def create_item(
    item: schemas.TaskCreateSchema, db: Session = Depends(get_db)
):
    return crud.create_task(db=db, item=item)


@app.get("/tasks/{task_id}", response_model=schemas.TaskSchema)
def read_item(task_id: UUID, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# @app.get("/")
# async def get_all_tasks():
#     tasks = db.session.query(TaskModel).all()
#     return tasks


# @app.get("/tasks/{task_id}")
# async def get_task(task_id: int):
#     return {"task_id": task_id}


# @app.post("/tasks", response_model=TaskSchema)
# async def create_task(task: TaskSchema):
#     db_task = TaskModel(
#         title=task.title,
#         description=task.description,
#         status=task.status,
#         deadline=task.deadline)
#     db.session.add(db_task)
#     db.session.commit()
#     return db_task


# @app.put("/tasks/{task_id}")
# async def update_task(task_id: int, task: TaskSchema):
#     return {"task_id": task_id, **task.model_dump()}


# @app.delete("/tasks/{task_id}")
# async def delete_task(task_id: int):
#     return {"task_id": "task deleted"}

# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
