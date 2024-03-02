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
- Cоздайте .env файл по образцу:
```
DB_HOSTNAME=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=
DB_NAME=
DB_ECHO=False
SECRET_KEY=

PROJECT_NAME='Taskee - таск трекер'
PROJECT_VERSION="0.2.0"
JWT_LIFETIME_SECONDS=2592000 #1 month

PGADMIN_EMAIL=
PGADMIN_PASSWORD=

``` 
- Запустите Docker-compose:
```
docker compose -f docker-compose-dev.yml up
``` 