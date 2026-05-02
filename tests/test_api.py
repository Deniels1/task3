"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_register_parent(self):
        """Test parent registration."""
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "Parent"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"

    def test_login(self):
        """Test login endpoint."""
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_get_me(self):
        """Test get current user."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data


class TestChildrenEndpoints:
    """Test children endpoints."""

    def test_get_children(self):
        """Test get children list with pagination."""
        response = client.get("/api/v1/children?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

    def test_create_child(self):
        """Test create child profile."""
        response = client.post("/api/v1/children", json={
            "name": "Test Child",
            "age": 6
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Child"
        assert data["age"] == 6
        assert data["xp_total"] == 0

    def test_get_child(self):
        """Test get child by ID."""
        response = client.get("/api/v1/children/child-1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "child-1"
        assert "name" in data

    def test_get_child_progress(self):
        """Test get child progress."""
        response = client.get("/api/v1/children/child-1/progress")
        assert response.status_code == 200
        data = response.json()
        assert data["child_id"] == "child-1"
        assert "xp_total" in data


class TestCurriculumEndpoints:
    """Test curriculum endpoints."""

    def test_get_units(self):
        """Test get units list."""
        response = client.get("/api/v1/units")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_unit_lessons(self):
        """Test get lessons for a unit."""
        response = client.get("/api/v1/units/unit-1/lessons")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_lesson(self):
        """Test get lesson by ID."""
        response = client.get("/api/v1/lessons/lesson-1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "lesson-1"

    def test_get_lesson_exercises(self):
        """Test get exercises for a lesson."""
        response = client.get("/api/v1/lessons/lesson-1/exercises")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestGamificationEndpoints:
    """Test gamification endpoints."""

    def test_complete_lesson(self):
        """Test lesson completion."""
        response = client.post("/api/v1/lessons/lesson-1/complete", json={
            "child_id": "child-1",
            "lesson_id": "lesson-1",
            "correct_answers": 5,
            "total_attempts": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert "xp_earned" in data
        assert "total_xp" in data
        assert "new_level" in data
        assert "new_streak" in data

    def test_get_leaderboard(self):
        """Test leaderboard endpoint."""
        response = client.get("/api/v1/leaderboard")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "rank" in data[0]

    def test_get_badges(self):
        """Test get child badges."""
        response = client.get("/api/v1/badges/children/child-1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_badge_templates(self):
        """Test get badge templates."""
        response = client.get("/api/v1/badges/templates")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestExerciseEndpoints:
    """Test exercise endpoints."""

    def test_get_exercise(self):
        """Test get exercise by ID."""
        response = client.get("/api/v1/exercises/ex-1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "ex-1"

    def test_submit_exercise(self):
        """Test submit exercise answer."""
        response = client.post("/api/v1/exercises/ex-1/submit", json={
            "answer": "A"
        })
        assert response.status_code == 200
        data = response.json()
        assert "correct" in data
        assert "xp_earned" in data


class TestNotificationEndpoints:
    """Test notification endpoints."""

    def test_get_notifications(self):
        """Test get notifications."""
        response = client.get("/api/v1/notifications")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_mark_notification_read(self):
        """Test mark notification as read."""
        response = client.patch("/api/v1/notifications/notif-1", json={
            "is_read": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["is_read"] is True


class TestAdminEndpoints:
    """Test admin endpoints."""

    def test_get_activity_logs(self):
        """Test get activity logs."""
        response = client.get("/api/v1/admin/logs")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_stats(self):
        """Test get platform stats."""
        response = client.get("/api/v1/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_parents" in data
        assert "total_children" in data


class TestHealthEndpoint:
    """Test health check."""

    def test_health(self):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
