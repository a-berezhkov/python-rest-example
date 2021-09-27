# Демо REST flask
## Запуск

1. Установить python с оф. сайта
2. Перейти в каталог с проектом
3. Развернуть базу, запустив ```python create_db.py```
4. Установить зависимости ```pip install -r requirements.txt```
5. Запустить flask ```flask run```

## Доступные действия

- /api/tasks/<task_id> - получение информации о задаче

- /api/add_task [POST] - добавление задачи 

- /api/task-by-user/<user_id> = получение задач пользователя

- /api/task-update [PUT] - обновление задачи

- /api/task-delete/<task_id> [DELETE] - удаление задачи