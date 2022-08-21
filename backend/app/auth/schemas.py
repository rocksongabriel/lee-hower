from pydantic import BaseModel
from pydantic.types import UUID4


class Token(BaseModel):
    token: str
    token_type: str


class AccessRefreshToken(BaseModel):
    access_token: Token
    refresh_token: Token


class TokenData(BaseModel):
    id: UUID4
