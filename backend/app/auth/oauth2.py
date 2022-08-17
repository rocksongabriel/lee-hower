from datetime import datetime, timedelta

from jose import jwt


# CONSTANTS
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
SECRET_KEY = "90565699a84ecb855fc42f1a71a931f7e7ee730cb0d9866e8a8d0d936c333077"  # TODO put this in .env


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


def refresh_access_token(data: dict[str, int | str | datetime]) -> str:
    """
    Encode data and return encoded jwt string object.
    """

    return create_access_token(
        data,
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
