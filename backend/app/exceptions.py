from fastapi import HTTPException, status

user_not_authorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User unauthorized to perform operation",
)
