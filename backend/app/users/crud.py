from fastapi import HTTPException, status
<<<<<<< HEAD
from pydantic.types import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from app.users.models import User
from app.users.schemas import UserProfileUpdate


def create_user(db: Session, user: User):
    """
    Add a new user to the database and return the user
    """

    try:
        db.add(user)
        db.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The action conflicts with another object in database.",
        )
    else:
        db.refresh(user)

    return user


def get_all_users(db: Session):
    """
    Fetch all the users from the database.
    Return the users.
    """

    return db.query(User).all()


def get_user(db: Session, uuid: UUID4):
    """
    Given a user's uuid (id), fetch user from database.
    Return the user object.
    """

    return db.query(User).filter(User.id == uuid).first()


def get_user_query(db: Session, uuid: UUID4):
    """
    Return a user query.
    """

    return db.query(User).filter(User.id == uuid)


def update_user(db: Session, uuid: UUID4, updated_user: UserProfileUpdate):
    """
    Given a user's id, Update the user profile in the database
    """

    get_user_query(db, uuid).update(
        updated_user.dict(), synchronize_session=False
    )
    db.commit()


def delete_user(db: Session, uuid: UUID4):
    """
    Given a user's uuid, Delete the user object from the database.
    """

    get_user_query(db, uuid).delete(synchronize_session=False)
    db.commit()
