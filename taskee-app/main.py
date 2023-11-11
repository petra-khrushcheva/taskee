from fastapi import FastAPI

from tasks.router import router as tasks_router

app = FastAPI(
    title='Taskee - таск трекер'
)

app.include_router(tasks_router)
