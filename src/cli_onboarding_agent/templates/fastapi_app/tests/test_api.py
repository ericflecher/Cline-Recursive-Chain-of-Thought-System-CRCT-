"""
Tests for the API endpoints of {{project_name}}.

This module contains tests for the API endpoints.
"""

import pytest
from fastapi import status

from app.schemas.user import UserCreate
from app.schemas.item import ItemCreate


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert "docs" in response.json()


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


class TestUserEndpoints:
    """Tests for user endpoints."""

    def test_create_user(self, client):
        """Test creating a user."""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert "password" not in data

    def test_get_users(self, client):
        """Test getting all users."""
        # Create a user first
        user_data = {
            "email": "test2@example.com",
            "password": "password123",
            "full_name": "Test User 2"
        }
        client.post("/api/v1/users/", json=user_data)

        # Get all users
        response = client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_user(self, client):
        """Test getting a specific user."""
        # Create a user first
        user_data = {
            "email": "test3@example.com",
            "password": "password123",
            "full_name": "Test User 3"
        }
        create_response = client.post("/api/v1/users/", json=user_data)
        user_id = create_response.json()["id"]

        # Get the user
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]

    def test_update_user(self, client):
        """Test updating a user."""
        # Create a user first
        user_data = {
            "email": "test4@example.com",
            "password": "password123",
            "full_name": "Test User 4"
        }
        create_response = client.post("/api/v1/users/", json=user_data)
        user_id = create_response.json()["id"]

        # Update the user
        update_data = {
            "full_name": "Updated User 4"
        }
        response = client.put(f"/api/v1/users/{user_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]
        assert data["full_name"] == update_data["full_name"]

    def test_delete_user(self, client):
        """Test deleting a user."""
        # Create a user first
        user_data = {
            "email": "test5@example.com",
            "password": "password123",
            "full_name": "Test User 5"
        }
        create_response = client.post("/api/v1/users/", json=user_data)
        user_id = create_response.json()["id"]

        # Delete the user
        response = client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify the user is deleted
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestItemEndpoints:
    """Tests for item endpoints."""

    def test_create_item(self, client):
        """Test creating an item."""
        # Create a user first
        user_data = {
            "email": "itemuser@example.com",
            "password": "password123",
            "full_name": "Item User"
        }
        user_response = client.post("/api/v1/users/", json=user_data)
        user_id = user_response.json()["id"]

        # Create an item
        item_data = {
            "title": "Test Item",
            "description": "This is a test item",
            "owner_id": user_id
        }
        response = client.post("/api/v1/items/", json=item_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == item_data["title"]
        assert data["description"] == item_data["description"]
        assert data["owner_id"] == user_id
        assert "id" in data

    def test_get_items(self, client):
        """Test getting all items."""
        # Create a user first
        user_data = {
            "email": "itemuser2@example.com",
            "password": "password123",
            "full_name": "Item User 2"
        }
        user_response = client.post("/api/v1/users/", json=user_data)
        user_id = user_response.json()["id"]

        # Create an item
        item_data = {
            "title": "Test Item 2",
            "description": "This is another test item",
            "owner_id": user_id
        }
        client.post("/api/v1/items/", json=item_data)

        # Get all items
        response = client.get("/api/v1/items/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
