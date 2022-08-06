from fastapi import HTTPException, APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db

from .schemas import UserRegister, UserRead
from .models import User

from app.utils.security import hash_password

router = APIRouter()


@router.post(
    "/register", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    """
    Api endpoint to register a user
    Return the data of the user after successfuly sign up.
    """

    # hash the password and set the user password field to the hashed
    # password
    hashed_password = hash_password(data.password)

    user = User(**data.dict())
    user.password = hashed_password

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


@router.get("/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    """
    API endpoint to get all users
    Return all the users in the database.
    """

    users = db.query(User).all()

    return users
