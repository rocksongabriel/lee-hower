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
            status_code=status.HTTP_400_BAD_REQUEST, detail="There was an error"
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
def get_task(uuid: UUID4, db: Session = Depends(get_db)):
    """API endpoint to get an individual task by its uuid"""

    task = db.query(models.Task).filter(models.Task.id == uuid).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {uuid} does not exist",
        )

    return task


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(uuid: UUID4, db: Session = Depends(get_db)):
    """API endpoint to delete a task"""

    task = db.query(models.Task).filter(models.Task.id == uuid)

    if task.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {uuid} does not exist",
        )

    task.delete(synchronize_session=False)

    db.commit()


@router.put("/{uuid}", response_model=tasks_schema.TaskRead)
def update_task(
    uuid: UUID4,
    updated_task: tasks_schema.TaskCreate,
    db: Session = Depends(get_db),
):
    """API endpoint to update a task"""

    task_query = db.query(models.Task).filter(models.Task.id == uuid)

    task = task_query.first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {uuid} does not exist",
        )

    task_query.update(updated_task.dict(), synchronize_session=False)

    db.commit()

    return task
