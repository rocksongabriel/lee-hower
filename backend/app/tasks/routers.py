from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_active_user, get_current_user
from app.database import get_db
from app.tasks import crud
from app.tasks.schemas import TaskCreate, TaskRead
from app.users.models import User


router = APIRouter()


def task_not_found(task_uuid: UUID4):
    """Raise HTTPException indicating task does not"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_uuid} does not exist.",
    )


@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """API endpoint for adding a task"""

    return crud.create_task(db, task)


@router.get("/", response_model=List[TaskRead])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """API endpoint for getting all tasks"""

    tasks = crud.get_all_tasks(db)

    return tasks


@router.get("/{uuid}", response_model=TaskRead)
def get_task(
    uuid: UUID4,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """API endpoint to get an individual task by its uuid"""

    task = crud.get_task(db, uuid)

    if not task:
        return task_not_found(uuid)

    return task


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    uuid: UUID4,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
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
    current_active_user: User = Depends(get_current_active_user),
):
    """API endpoint to update a task"""

    task = crud.get_task(db, uuid)

    if not task:
        return task_not_found(uuid)

    task_query = crud.get_task_query(db, uuid)
    crud.update_task(db, task_query, updated_task)

    return task
