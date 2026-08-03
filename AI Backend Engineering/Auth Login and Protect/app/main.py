from typing import Any

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from supabase import Client

from .config import get_settings
from .schemas import Credentials, TokenResponse
from .security import get_current_user
from .supabase_client import get_supabase

app = FastAPI(
    title="Auth - Login & Protect",
    version="1.0.0",
    description="Secure FastAPI service using Supabase Auth and bearer-token protection.",
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _request: Request, _exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})


def validate_credentials(credentials: Credentials) -> tuple[str, str]:
    email = (credentials.email or "").strip()
    password = credentials.password or ""
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    return email, password


def public_user(user: Any) -> dict[str, Any]:
    if hasattr(user, "model_dump"):
        data = user.model_dump()
    elif isinstance(user, dict):
        data = user
    else:
        data = {
            "id": getattr(user, "id", None),
            "email": getattr(user, "email", None),
            "created_at": getattr(user, "created_at", None),
        }
    return {key: data.get(key) for key in ("id", "email", "created_at")}


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/signup", status_code=201, tags=["Authentication"])
async def signup(
    credentials: Credentials, supabase: Client = Depends(get_supabase)
) -> dict[str, Any]:
    email, password = validate_credentials(credentials)
    try:
        result = supabase.auth.sign_up({"email": email, "password": password})
        return {"user": public_user(result.user)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post(
    "/auth/login",
    response_model=TokenResponse,
    tags=["Authentication"],
)
async def login(
    credentials: Credentials, supabase: Client = Depends(get_supabase)
) -> TokenResponse:
    email, password = validate_credentials(credentials)
    try:
        result = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        session = getattr(result, "session", None)
        if session is None:
            raise ValueError("No session returned")
        return TokenResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid login credentials") from exc


@app.post(
    "/auth/logout",
    status_code=204,
    tags=["Authentication"],
    dependencies=[Depends(get_current_user)],
)
async def logout(request: Request) -> Response:
    settings = get_settings()
    settings.validate()
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{settings.supabase_url}/auth/v1/logout",
            headers={
                "apikey": settings.supabase_key,
                "Authorization": f"Bearer {request.state.access_token}",
            },
        )
    if response.status_code not in (200, 204):
        raise HTTPException(status_code=400, detail="Unable to log out")
    return Response(status_code=204)


@app.get("/public/info", tags=["Public"])
async def public_info() -> dict[str, str]:
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile", tags=["Protected"])
async def protected_profile(
    user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    return {"user": public_user(user)}


@app.get("/protected/dashboard", tags=["Protected"])
async def protected_dashboard(
    user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    return {
        "message": "Welcome to your protected dashboard.",
        "user": public_user(user),
    }
