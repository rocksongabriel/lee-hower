from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy.orm import Session
from app.users.utils import verify_password

from app.users.models import User


# CONSTANTS
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
# TODO put this in .env
SECRET_KEY = "90565699a84ecb855fc42f1a71a931f7e7ee730cb0d9866e8a8d0d936c333077"


def authenticate_user(
    db: Session, username: str, password: str
) -> User | bool:
    """
    Take username and password and authenticate the user'
    username against their password.
    Return user from db if credentials are authentic
    """
    user = db.query(User).filter(User.email == username).first()

    if user is None:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(
    data: dict[str, int | str | datetime],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Encode data and return encoded jwt string object.
    """

    data_to_encode = data.copy()

    if expires_delta is None:
        expiration_time = datetime.now() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    else:
        expiration_time = datetime.now() + expires_delta
    data_to_encode.update({"exp": expiration_time})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict[str, int | str | datetime]) -> str:
    """
    Encode data and return encoded jwt string object.
    """

    return create_access_token(
        data, expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
