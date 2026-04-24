from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskSchema, TaskResponseSchema
from src.utils.db import get_db
from src.utils.helpers import is_authenticated
from src.user.models import UserModel

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create", status_code=status.HTTP_201_CREATED)
def create_task(body: TaskSchema, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.create_task(body, db)

@task_routes.get("/", status_code=status.HTTP_200_OK)
def get_tasks(db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_tasks(db)

@task_routes.get("/{id}", status_code=status.HTTP_200_OK)
def get_task(id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_task(id, db)

@task_routes.put("/{id}", status_code=status.HTTP_201_CREATED)
def update_task(body: TaskSchema, id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.update_task(body, id, db)

@task_routes.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_task(id: int, db = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.delete_task(id, db)