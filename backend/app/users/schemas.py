from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import UUID4, SecretStr
from typing import Optional


class UserBase(BaseModel):
    """Base pydantic model representing the user data"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    created: datetime


class UserRegister(BaseModel):
    """Pydantic model for registering a user account"""

    email: EmailStr
    password: SecretStr


class UserProfileUpdate(UserBase):
    """Model to update the user profile with data"""

    email: EmailStr


class UserRead(UserBase):
    """Response model for User"""

    id: UUID4
    email: EmailStr
