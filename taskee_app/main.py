from fastapi import FastAPI
from tasks.router import router as tasks_router
from users.router import router as users_router

app = FastAPI(
    title='Taskee - таск трекер'
)

app.include_router(tasks_router)
app.include_router(users_router)