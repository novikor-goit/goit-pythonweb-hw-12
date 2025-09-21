from fastapi.testclient import TestClient

from src.database.models import Contact


class TestContacts:
    def test_create_contact(self, authenticated_client: TestClient):
        response = authenticated_client.post(
            "/api/contacts",
            json={
                "first_name": "Test",
                "last_name": "Contact",
                "email": "test.contact2@example.com",
                "phone": "1234567890",
            },
        )
        assert response.status_code == 201, response.json()

    def test_get_contacts(self, authenticated_client: TestClient, contact: Contact):
        response = authenticated_client.get("/api/contacts")
        assert response.status_code == 200, response.json()
        assert len(response.json()) == 1

    def test_get_contact(self, authenticated_client: TestClient, contact: Contact):
        response = authenticated_client.get(f"/api/contacts/{contact.id}")
        assert response.status_code == 200, response.json()
        assert response.json()["first_name"] == contact.first_name

    def test_update_contact(self, authenticated_client: TestClient, contact: Contact):
        response = authenticated_client.put(
            f"/api/contacts/{contact.id}",
            json={
                "first_name": "Updated",
                "last_name": "Contact",
                "email": "updated.contact@example.com",
                "phone": "1112223333",
            },
        )
        assert response.status_code == 200, response.json()
        assert response.json()["first_name"] == "Updated"

    def test_delete_contact(self, authenticated_client: TestClient, contact: Contact):
        response = authenticated_client.delete(f"/api/contacts/{contact.id}")
        assert response.status_code == 204, response.json()

    def test_get_contact_not_found(self, authenticated_client: TestClient):
        response = authenticated_client.get("/api/contacts/999")
        assert response.status_code == 404, response.json()

    def test_update_contact_not_found(self, authenticated_client: TestClient):
        response = authenticated_client.put(
            "/api/contacts/999",
            json={
                "first_name": "Updated",
                "last_name": "Contact",
                "email": "updated.contact@example.com",
                "phone": "1112223333",
            },
        )
        assert response.status_code == 404, response.json()

    def test_delete_contact_not_found(self, authenticated_client: TestClient):
        response = authenticated_client.delete("/api/contacts/999")
        assert response.status_code == 404, response.json()
