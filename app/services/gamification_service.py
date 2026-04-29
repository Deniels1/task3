"""
Gamification service.

Simple XP, streak, and level calculation.
"""

from datetime import datetime, timedelta, date
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Child


class GamificationService:
    """Service for XP, streaks, and level calculation."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def calculate_xp(self, lesson_difficulty: int) -> int:
        """
        Calculate XP for lesson completion.
        
        Formula: 100 + (difficulty - 1) * 20
        """
        BASE_XP = 100
        DIFFICULTY_BONUS = 20
        return BASE_XP + (lesson_difficulty - 1) * DIFFICULTY_BONUS
    
    def get_level_threshold(self, level: int) -> int:
        """
        Get XP needed for next level.
        
        Formula: level * level * 100
        Level 1->2: 100 XP
        Level 2->3: 400 XP
        """
        return level * level * 100
    
    def check_level_up(self, current_level: int, current_xp: int, xp_to_add: int) -> Tuple[int, bool]:
        """Check if child levels up after earning XP."""
        total_xp = current_xp + xp_to_add
        threshold = self.get_level_threshold(current_level)
        
        if total_xp >= threshold:
            return current_level + 1, True  # Level up!
        return current_level, False  # No change
    
    def update_streak(self, child: Child) -> Tuple[int, bool]:
        """
        Update child's streak based on activity.
        
        Returns: (new_streak, updated)
        """
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        
        # Already active today
        if child.streak_last_activity_date == today:
            return child.streak_current, False
        
        # Active yesterday - continue streak
        if child.streak_last_activity_date == yesterday:
            new_streak = child.streak_current + 1
            return new_streak, True
        
        # First time or streak broken
        return 1, True
    
    async def process_lesson_complete(
        self,
        child: Child,
        lesson_difficulty: int,
        correct: int,
        total: int
    ) -> dict:
        """
        Process lesson completion.
        
        Updates: XP, level, streak, stats.
        """
        # Calculate XP
        xp = self.calculate_xp(lesson_difficulty)
        
        # Update child stats
        child.xp_total += xp
        child.lessons_completed += 1
        child.last_activity_at = datetime.utcnow()
        
        # Check level up
        new_level, leveled_up = self.check_level_up(
            child.level_number,
            child.xp_total - xp,  # XP before this lesson
            xp
        )
        child.level_number = new_level
        
        # Update streak
        new_streak, streak_updated = self.update_streak(child)
        child.streak_current = new_streak
        
        if new_streak > child.streak_best:
            child.streak_best = new_streak
        
        # Accuracy
        if total > 0:
            child.accuracy_rate = int((correct / total) * 100)
        
        # Save to DB
        await self.db.flush()
        await self.db.refresh(child)
        
        return {
            "xp_earned": xp,
            "total_xp": child.xp_total,
            "new_level": new_level,
            "level_up": leveled_up,
            "new_streak": new_streak,
            "streak_updated": streak_updated
        }
