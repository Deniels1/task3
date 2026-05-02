"""Tests for gamification logic."""

import pytest
from datetime import date, timedelta

from app.services.gamification_service import GamificationService


class MockChild:
    """Mock child for testing."""
    def __init__(self):
        self.xp_total = 0
        self.level_number = 1
        self.streak_current = 0
        self.streak_best = 0
        self.streak_last_activity_date = None
        self.lessons_completed = 0
        self.accuracy_rate = 0


class TestXPCalculation:
    """Test XP calculation."""

    def test_xp_difficulty_1(self):
        """XP for difficulty 1 should be 100."""
        service = GamificationService(None)
        assert service.calculate_xp(1) == 100

    def test_xp_difficulty_2(self):
        """XP for difficulty 2 should be 120."""
        service = GamificationService(None)
        assert service.calculate_xp(2) == 120

    def test_xp_difficulty_3(self):
        """XP for difficulty 3 should be 140."""
        service = GamificationService(None)
        assert service.calculate_xp(3) == 140


class TestLevelThreshold:
    """Test level threshold calculation."""

    def test_level_1_to_2(self):
        """Level 1 to 2 needs 100 XP."""
        service = GamificationService(None)
        assert service.get_level_threshold(2) == 400

    def test_level_2_to_3(self):
        """Level 2 to 3 needs 400 XP."""
        service = GamificationService(None)
        assert service.get_level_threshold(3) == 900


class TestLevelUp:
    """Test level up logic."""

    def test_no_level_up(self):
        """Should not level up if not enough XP."""
        service = GamificationService(None)
        new_level, leveled_up = service.check_level_up(1, 0, 50)
        assert new_level == 1
        assert leveled_up is False

    def test_level_up(self):
        """Should level up if enough XP."""
        service = GamificationService(None)
        new_level, leveled_up = service.check_level_up(1, 50, 100)
        assert new_level == 2
        assert leveled_up is True


class TestStreak:
    """Test streak logic."""

    def test_first_activity(self):
        """First activity should set streak to 1."""
        service = GamificationService(None)
        child = MockChild()
        child.streak_last_activity_date = None
        new_streak, updated = service.update_streak(child)
        assert new_streak == 1
        assert updated is True

    def test_continue_streak(self):
        """Activity yesterday should continue streak."""
        service = GamificationService(None)
        child = MockChild()
        child.streak_current = 3
        child.streak_last_activity_date = (date.today() - timedelta(days=1)).isoformat()
        new_streak, updated = service.update_streak(child)
        assert new_streak == 4
        assert updated is True

    def test_same_day(self):
        """Activity today should not change streak."""
        service = GamificationService(None)
        child = MockChild()
        child.streak_current = 3
        child.streak_last_activity_date = date.today().isoformat()
        new_streak, updated = service.update_streak(child)
        assert new_streak == 3
        assert updated is False
