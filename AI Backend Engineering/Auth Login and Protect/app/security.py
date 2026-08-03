from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client

from .supabase_client import get_supabase

bearer_scheme = HTTPBearer(auto_error=False)


def access_token_required() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access token required",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    supabase: Client = Depends(get_supabase),
) -> Any:
    authorization = request.headers.get("Authorization", "")
    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or not credentials.credentials.strip()
        or not authorization.startswith("Bearer ")
    ):
        raise access_token_required()

    try:
        response = supabase.auth.get_user(credentials.credentials)
        user = getattr(response, "user", None)
        if user is None:
            raise ValueError("Supabase returned no user")
        request.state.access_token = credentials.credentials
        request.state.user = user
        return user
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
