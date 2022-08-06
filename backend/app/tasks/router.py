from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import UUID4
from app.tasks import schema as tasks_schema
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List


router = APIRouter()


@router.post("/", response_model=tasks_schema.TaskRead)
def create_task(task: tasks_schema.TaskCreate, db: Session = Depends(get_db)):
    """API endpoint for adding a task"""

    new_task = models.Task(**task.dict())

    try:
        db.add(new_task)
        db.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There was an error"
        )
    else:
        db.refresh(new_task)

    return new_task


@router.get("/", response_model=List[tasks_schema.TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    """API endpoint for getting all tasks"""

    tasks = db.query(models.Task).all()

    return tasks


@router.get("/{uuid}", response_model=tasks_schema.TaskRead)
def get_post(uuid: UUID4, db: Session = Depends(get_db)):
    """API endpoint to get an individual task by it's uuid"""

    task = db.query(models.Task).filter(models.Task.id == uuid).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {uuid} does not exist"
        )

    return task
