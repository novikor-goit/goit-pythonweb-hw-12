from unittest.mock import patch

from fastapi.testclient import TestClient

from src.database.models import User


class TestUsers:
    def test_get_me(self, authenticated_client: TestClient):
        response = authenticated_client.get("/api/users/me")
        assert response.status_code == 200, response.json()
        assert response.json()["username"] == "testuser"

    def test_update_avatar_not_admin(self, authenticated_client: TestClient):
        with patch("src.services.media.MediaStorage.upload_file") as mock_upload:
            mock_upload.return_value = "http://example.com/avatar.png"
            response = authenticated_client.patch(
                "/api/users/avatar", files={"file": ("test.png", b"", "image/png")}
            )
            assert response.status_code == 403, response.json()

    def test_update_avatar_admin(self, client: TestClient, admin: User):
        response = client.post(
            "/api/auth/login",
            data={"username": admin.username, "password": "password"},
        )
        token = response.json()["access_token"]
        client.headers["Authorization"] = f"Bearer {token}"

        with patch("src.services.media.MediaStorage.upload_file") as mock_upload:
            mock_upload.return_value = "http://example.com/avatar.png"
            response = client.patch(
                "/api/users/avatar", files={"file": ("test.png", b"", "image/png")}
            )
            assert response.status_code == 200, response.json()
            assert response.json()["avatar"] == "http://example.com/avatar.png"
