from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(body: TaskSchema, db: Session):
    data = body.model_dump()
    task = TaskModel(title = data["title"], description = data["description"], is_completed= data["is_completed"])
    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message":"Created task successfully!",
        "payload": body
    }

def get_tasks(db: Session):
    tasks = db.query(TaskModel).all()
    return {
        "message":"Task Fetched successfully!",
        "payload": tasks
    }

def get_task(id: int, db: Session):
    task = db.query(TaskModel).get(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    
    return {
        "message":"Task Fetched successfully!",
        "payload": task
    }

def update_task(body: TaskModel, id: int , db: Session):
    task = db.query(TaskModel).get(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    
    body = body.model_dump()
    for field, value in body.items():
        setattr(task, field, value)
 
    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message":"Task updated successfully!",
        "payload": task
    }

def delete_task(id: int, db: Session):
    task = db.query(TaskModel).get(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    
    db.delete(task)
    db.commit()

    return {
        "message":"Task deleted successfully!"
    }
