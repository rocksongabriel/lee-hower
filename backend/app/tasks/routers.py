from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_active_user, get_current_user
from app.db.config import get_db
from app.tasks import crud
from app.tasks.schemas import TaskCreate, TaskRead
from app.users.models import User
from app.tasks.models import Task

from app.exceptions import user_not_authorized_exception


router = APIRouter()


async def task_not_found(task_uuid: UUID4):
    """Raise HTTPException indicating task does not"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_uuid} does not exist.",
    )


user_not_authorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User unauthorized to perform operation.",
)


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    new_task: TaskCreate,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """API endpoint for adding a task"""

    return crud.create_user_task(db, new_task, current_active_user.id)


@router.get("/", response_model=List[TaskRead])
async def get_users_tasks_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """API endpoint for getting all user's tasks"""

    tasks = crud.get_user_tasks(db=db, user_id=current_user.id)

    return tasks


@router.get("/{uuid}", response_model=TaskRead)
async def get_task(
    uuid: UUID4,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """API endpoint to get an individual task by its uuid"""

    task = crud.get_task(db, uuid)

    if not task:
        return task_not_found(uuid)

    if current_active_user.id != task.owner_id:
        raise user_not_authorized_exception

    return task


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
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

    if current_active_user.id != task.owner_id:
        raise user_not_authorized_exception


@router.put("/{uuid}", response_model=TaskRead)
async def update_task(
    uuid: UUID4,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """API endpoint to update a task"""

    task = crud.get_task(db, uuid)

    if not task:
        return task_not_found(uuid)

    if current_active_user.id != task.owner_id:
        raise user_not_authorized_exception

    task_query = crud.get_task_query(db, uuid)
    crud.update_task(db, task_query, updated_task)

    return task
