from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.oauth2 import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
)
from app.auth.schemas import AccessRefreshToken, Token
from app.db.config import get_db


router = APIRouter()


@router.post("/login", response_model=AccessRefreshToken, name="users:login-email-and-password")
async def get_access_and_refresh_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    API endpoint to get access token and refresh tokens
    """

    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {"sub": str(user.id)}
    token_type = "bearer"

    access_token = {
        "token": create_access_token(data),
        "token_type": token_type,
    }
    refresh_token = {
        "token": create_refresh_token(data),
        "token_type": token_type,
    }

    return {"access_token": access_token, "refresh_token": refresh_token}
