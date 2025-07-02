"""Data models for the habit tracker."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Habit:
    """Represents a habit to be tracked."""
    
    id: int
    name: str
    created_at: datetime
    completed_today: Optional[bool] = None
    
    def __post_init__(self) -> None:
        """Validate habit data after initialization."""
        if not self.name.strip():
            raise ValueError("Habit name cannot be empty")
        
        if self.id <= 0:
            raise ValueError("Habit ID must be positive")


@dataclass
class Entry:
    """Represents a completion entry for a habit on a specific date."""
    
    id: int
    habit_id: int
    entry_date: date
    created_at: datetime
    
    def __post_init__(self) -> None:
        """Validate entry data after initialization."""
        if self.id <= 0:
            raise ValueError("Entry ID must be positive")
        
        if self.habit_id <= 0:
            raise ValueError("Habit ID must be positive")
        
        if self.entry_date > date.today():
            raise ValueError("Entry date cannot be in the future") 