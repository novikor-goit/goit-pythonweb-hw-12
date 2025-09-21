from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User


class TestAuth:
    @patch("src.api.routes.auth.send_email_in_background")
    def test_register_user(self, mock_send_email, client: TestClient):
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser_integr",
                "email": "test_integr@example.com",
                "password": "password",
            },
        )
        assert response.status_code == 201, response.json()
        mock_send_email.assert_called_once()

    def test_register_duplicate_username(self, client: TestClient, user: User):
        response = client.post(
            "/api/auth/register",
            json={
                "username": user.username,
                "email": "new@example.com",
                "password": "password",
            },
        )
        assert response.status_code == 409, response.json()

    @pytest.mark.asyncio
    async def test_login_unconfirmed_email(
        self, client: TestClient, user: User, db_session: AsyncSession
    ):
        user.is_confirmed = False
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        response = client.post(
            "/api/auth/login",
            data={"username": user.username, "password": "password"},
        )
        assert response.status_code == 401, response.json()

    def test_login_incorrect_password(self, client: TestClient, user: User):
        response = client.post(
            "/api/auth/login",
            data={"username": user.username, "password": "wrongpassword"},
        )
        assert response.status_code == 401, response.json()

    def test_login(self, client: TestClient, user: User):
        response = client.post(
            "/api/auth/login",
            data={"username": user.username, "password": "password"},
        )
        assert response.status_code == 200, response.json()
        assert "access_token" in response.json()

    @patch("src.api.routes.auth.send_email_in_background")
    def test_password_reset(self, mock_send_email, client: TestClient, user: User):
        response = client.post(
            "/api/auth/request-password-reset",
            json={"email": user.email},
        )
        assert response.status_code == 200, response.json()
        mock_send_email.assert_called_once()

    def test_refresh_token_invalid(self, client: TestClient):
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": "Bearer invalid_token"},
        )
        assert response.status_code == 401, response.json()
