from fastapi import FastAPI

from tasks.urls import tasks_router

app = FastAPI(title="Taskee")

app.include_router(tasks_router)
