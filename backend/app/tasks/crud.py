from pydantic.types import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from app.tasks.models import Task

from app.tasks.schemas import TaskCreate


def create_task(db: Session, new_task: TaskCreate):
    """
    Create new task in the database.
    Return the new task.
    """

    print(new_task)
    print(db)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_task(db: Session, uuid: UUID4):
    """
    Get a task by uuid (id) from the database.
    Return this item.
    """

    return db.query(Task).filter(Task.id == uuid).first()


def get_all_tasks(db: Session):
    """
    Get all tasks from the database.
    Return all tasks
    """

    return db.query(Task).all()


def get_user_tasks(db: Session, user_id: UUID4):
    """
    Given a user's id, get and return all their
    tasks from the database
    """

    return db.query(Task).filter(Task.owner_id == user_id).all()


def get_task_query(db: Session, uuid: UUID4):
    """
    Return a task query on the database that fetches a
    task based on uuid (id)
    """

    return db.query(Task).filter(Task.id == uuid)


def delete_task(db: Session, query: Query):
    """
    Take a query object and delete the correspoding item from the
    database.
    """

    query.delete(synchronize_session=False)
    db.commit()


def update_task(db: Session, query: Query, updated_task: TaskCreate):
    """
    Update a task in the database.
    """

    query.update(updated_task.dict(), synchronize_session=False)
    db.commit()
