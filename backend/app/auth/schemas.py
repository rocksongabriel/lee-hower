from pydantic import BaseModel


class Token(BaseModel):
    token: str
    token_type: str


class AccessRefreshToken(BaseModel):
    access_token: Token
    refresh_token: Token
