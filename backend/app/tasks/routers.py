from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import UUID4
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List

from app.tasks.schemas import TaskRead, TaskCreate
from app.tasks.models import Task

from app.tasks import crud


router = APIRouter()


def task_not_found(task_uuid: UUID4):
    """Raise HTTPException indicating task does not"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_uuid} does not exist.",
    )


@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """API endpoint for adding a task"""

    return crud.create_task(db, task)


@router.get("/", response_model=List[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    """API endpoint for getting all tasks"""

    tasks = db.query(Task).all()

    return tasks


@router.get("/{uuid}", response_model=TaskRead)
def get_task(uuid: UUID4, db: Session = Depends(get_db)):
    """API endpoint to get an individual task by its uuid"""

    task = crud.get_task(db, uuid)

    if not task:
        return task_not_found(uuid)

    return task


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(uuid: UUID4, db: Session = Depends(get_db)):
    """API endpoint to delete a task"""

    task = crud.get_task(db, uuid)

    if task:
        task_query = crud.get_task_query(db, uuid)
        crud.delete_task(db, task_query)
    if not task:
        return task_not_found(uuid)


@router.put("/{uuid}", response_model=TaskRead)
def update_task(
    uuid: UUID4,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
):
    """API endpoint to update a task"""

    task = crud.get_task(db, uuid)

    if not task:
        return task_not_found(uuid)

    task_query = crud.get_task_query(db, uuid)
    crud.update_task(db, task_query, updated_task)

    return task
