from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app
from app.supabase_client import get_supabase


USER = SimpleNamespace(
    id="user-123",
    email="student@example.com",
    created_at="2026-08-03T00:00:00Z",
)


class FakeAuth:
    def sign_up(self, credentials):
        return SimpleNamespace(user=USER)

    def sign_in_with_password(self, credentials):
        if credentials["password"] == "wrong-password":
            raise ValueError("bad credentials")
        return SimpleNamespace(
            session=SimpleNamespace(
                access_token="valid-token",
                refresh_token="refresh-token",
            )
        )

    def get_user(self, token):
        if token != "valid-token":
            raise ValueError("invalid token")
        return SimpleNamespace(user=USER)


class FakeSupabase:
    auth = FakeAuth()


app.dependency_overrides[get_supabase] = lambda: FakeSupabase()
client = TestClient(app)


def test_public_route_needs_no_token():
    response = client.get("/public/info")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome stranger! This info is public."
    }


def test_signup_returns_201():
    response = client.post(
        "/auth/signup",
        json={"email": "student@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    assert response.json()["user"]["email"] == "student@example.com"


def test_missing_login_field_returns_400():
    response = client.post(
        "/auth/login", json={"email": "student@example.com"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Email and password are required"


def test_login_returns_tokens():
    response = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] == "valid-token"
    assert response.json()["refresh_token"] == "refresh-token"


def test_bad_login_returns_401():
    response = client.post(
        "/auth/login",
        json={
            "email": "student@example.com",
            "password": "wrong-password",
        },
    )
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid login credentials"


def test_profile_requires_bearer_token():
    response = client.get("/protected/profile")
    assert response.status_code == 401
    assert response.json()["error"] == "Access token required"


def test_profile_rejects_tampered_token():
    response = client.get(
        "/protected/profile",
        headers={"Authorization": "Bearer tampered-token"},
    )
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid or expired token"


def test_profile_accepts_valid_token():
    response = client.get(
        "/protected/profile",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 200
    assert response.json()["user"]["id"] == "user-123"


def test_dashboard_reuses_auth_dependency():
    response = client.get(
        "/protected/dashboard",
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "student@example.com"
