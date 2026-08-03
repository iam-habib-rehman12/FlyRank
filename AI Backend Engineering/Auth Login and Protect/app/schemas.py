from pydantic import BaseModel


class Credentials(BaseModel):
    email: str | None = None
    password: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ErrorResponse(BaseModel):
    error: str
