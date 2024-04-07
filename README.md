![Workflow badge](https://github.com/petra-khrushcheva/taskee_2_0/actions/workflows/main.yml/badge.svg)

# Taskee - таск трекер для групповой работы

Таск трекер для групповой работы с различным уровнем доступа для членов группы.  
Доступны эндпойнты для работы с рабочими пространствами (workspaces) и задачами внутри рабочих пространств (tasks). Эндпойнты закрыты авторизацией.  
Информация сохраняется в базу данных PostgresQL.
***
### Технологии
Python 3.11  
FastAPI 0.104  
SQLAlchemy 2.0  
Pydantic 2.5  
Alembic 1.13  
PostgreSQL  
***
### Установка
- Клонируйте проект:
```
git clone git@github.com:petra-khrushcheva/taskee_2_0.git
``` 
- Перейдите в директорию taskee_2_0:
```
cd taskee_2_0
``` 
- Cоздайте переменные окружения по [образцу](https://github.com/petra-khrushcheva/taskee_2_0/blob/main/.env.example).
- Запустите Docker-compose:
```
docker compose -f docker-compose-dev.yml up
``` 