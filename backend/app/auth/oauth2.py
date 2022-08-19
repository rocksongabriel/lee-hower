from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.auth.schemas import TokenData
from app.database import get_db
from app.users import crud
from app.users.models import User
from app.users.utils import verify_password


# CONSTANTS
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
# TODO put this in .env
SECRET_KEY = "90565699a84ecb855fc42f1a71a931f7e7ee730cb0d9866e8a8d0d936c333077"

# Oauth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Take a token and verify the token.
    Return a user object if token is valid.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    else:
        user = crud.get_user(db, token_data.id)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    """
    Given the current user, return the user if the user's
    account is active.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user."
        )

    return current_user
