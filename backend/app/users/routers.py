from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_active_user
from app.db.config import get_db
from app.exceptions import user_not_authorized_exception
from app.users import crud

from .models import User
from .schemas import UserProfileUpdate, UserRead, UserRegister
from .utils import hash_password


router = APIRouter()


def user_does_not_exist_exception(uuid: UUID4):
    """Function to raise user does not exist error"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {uuid} does not exist",
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(data: UserRegister, db: Session = Depends(get_db)):
    """
    Api endpoint to register a user
    Return the data of the user after successfuly sign up.
    """

    hashed_password = hash_password(data.password)

    user = User(**data.dict())
    user.password = hashed_password

    return crud.create_user(db, user)


@router.get("/", response_model=List[UserRead], name="users:get-users")
async def get_users(
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """
    API endpoint to get all users
    Return all the users in the database.
    """

    return crud.get_all_users(db)


@router.get("/{uuid}", response_model=UserRead, name="users:get-user")
async def get_user(
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """
    API Endpoint to get an individual user by id
    Return user info
    """
    return current_active_user


@router.put("/{uuid}", response_model=UserRead, name="users:update-user")
async def update_user(
    uuid: UUID4,
    updated_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """
    API Endpoint to update a user's data when given its id
    Return the updated user info
    """

    user = crud.get_user(db, uuid)

    if user is None:
        return user_does_not_exist_exception(uuid)

    if current_active_user.id != user.id:
        raise user_not_authorized_exception

    crud.update_user(db, uuid, updated_data)

    return user


@router.delete(
    "/{uuid}", status_code=status.HTTP_204_NO_CONTENT, name="users:delete-user"
)
async def delete_user(
    uuid: UUID4,
    db: Session = Depends(get_db),
    current_active_user: User = Depends(get_current_active_user),
):
    """
    API endpoint to delete a specific user from the database.
    Return no response data
    """

    user = crud.get_user(db, uuid)

    if user is None:
        return user_does_not_exist_exception(uuid)

    if current_active_user.id != user.id:
        raise user_not_authorized_exception

    crud.delete_user(db, uuid)
