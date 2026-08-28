import os
from datetime import timedelta

os.environ["DATABASE_URL"] = "sqlite:///./careerlens_auth_test.db"
os.environ["JWT_SECRET"] = "test-only-secret-that-is-long-enough-to-pass-validation"
os.environ["CORS_ORIGINS"] = "http://testserver"

import pytest
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import User


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def valid_signup() -> dict[str, str]:
    return {"full_name": "Aditi Sharma", "email": "aditi@example.com", "password": "CareerLens2026"}


def test_successful_signup_returns_token_pair(client):
    response = client.post("/api/v1/auth/signup", json=valid_signup())
    assert response.status_code == 201
    payload = response.json()
    assert payload["access_token"]
    assert payload["refresh_token"]
    assert payload["user"]["email"] == "aditi@example.com"
    assert "password" not in str(payload).lower()


def test_duplicate_email_is_rejected(client):
    assert client.post("/api/v1/auth/signup", json=valid_signup()).status_code == 201
    assert client.post("/api/v1/auth/signup", json=valid_signup()).status_code == 409


@pytest.mark.parametrize("field,value", [("email", "not-an-email"), ("password", "weak")])
def test_invalid_signup_payload_is_rejected(client, field, value):
    payload = valid_signup()
    payload[field] = value
    assert client.post("/api/v1/auth/signup", json=payload).status_code == 422


def test_successful_login_and_wrong_password(client):
    assert client.post("/api/v1/auth/signup", json=valid_signup()).status_code == 201
    assert client.post("/api/v1/auth/login", json={"email": "aditi@example.com", "password": "CareerLens2026"}).status_code == 200
    assert client.post("/api/v1/auth/login", json={"email": "aditi@example.com", "password": "incorrect-password"}).status_code == 401


def test_protected_me_rejects_invalid_and_expired_tokens(client):
    assert client.get("/api/v1/auth/me").status_code == 401
    assert client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"}).status_code == 401
    with SessionLocal() as db:
        user = User(full_name="Aditi", email="aditi@example.com", password_hash="not-used")
        db.add(user)
        db.commit()
        db.refresh(user)
        expired, _, _ = create_access_token(user.id, expires_delta=timedelta(seconds=-1))
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_refresh_rotates_and_logout_revokes(client):
    first_refresh = client.post("/api/v1/auth/signup", json=valid_signup()).json()["refresh_token"]
    refreshed = client.post("/api/v1/auth/refresh", json={"refresh_token": first_refresh})
    assert refreshed.status_code == 200
    second_refresh = refreshed.json()["refresh_token"]
    assert second_refresh != first_refresh
    assert client.post("/api/v1/auth/refresh", json={"refresh_token": first_refresh}).status_code == 401
    assert client.post("/api/v1/auth/logout", json={"refresh_token": second_refresh}).status_code == 200
    assert client.post("/api/v1/auth/refresh", json={"refresh_token": second_refresh}).status_code == 401
