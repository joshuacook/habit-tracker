"""Unit tests for the models module."""

import pytest
from datetime import date, datetime

from habit.models import Habit, Entry


class TestHabit:
    """Test cases for Habit model."""
    
    def test_habit_creation(self):
        """Test creating a valid habit."""
        now = datetime.now()
        habit = Habit(id=1, name="Test Habit", created_at=now)
        
        assert habit.id == 1
        assert habit.name == "Test Habit"
        assert habit.created_at == now
        assert habit.completed_today is None
    
    def test_habit_with_completion_status(self):
        """Test creating a habit with completion status."""
        now = datetime.now()
        habit = Habit(id=1, name="Test Habit", created_at=now, completed_today=True)
        
        assert habit.completed_today is True
    
    def test_habit_validation_empty_name(self):
        """Test that empty habit name raises ValueError."""
        now = datetime.now()
        
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            Habit(id=1, name="", created_at=now)
    
    def test_habit_validation_whitespace_name(self):
        """Test that whitespace-only habit name raises ValueError."""
        now = datetime.now()
        
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            Habit(id=1, name="   ", created_at=now)
    
    def test_habit_validation_invalid_id(self):
        """Test that invalid habit ID raises ValueError."""
        now = datetime.now()
        
        with pytest.raises(ValueError, match="Habit ID must be positive"):
            Habit(id=0, name="Test Habit", created_at=now)
        
        with pytest.raises(ValueError, match="Habit ID must be positive"):
            Habit(id=-1, name="Test Habit", created_at=now)


class TestEntry:
    """Test cases for Entry model."""
    
    def test_entry_creation(self):
        """Test creating a valid entry."""
        now = datetime.now()
        today = date.today()
        entry = Entry(id=1, habit_id=1, entry_date=today, created_at=now)
        
        assert entry.id == 1
        assert entry.habit_id == 1
        assert entry.entry_date == today
        assert entry.created_at == now
    
    def test_entry_validation_invalid_id(self):
        """Test that invalid entry ID raises ValueError."""
        now = datetime.now()
        today = date.today()
        
        with pytest.raises(ValueError, match="Entry ID must be positive"):
            Entry(id=0, habit_id=1, entry_date=today, created_at=now)
        
        with pytest.raises(ValueError, match="Entry ID must be positive"):
            Entry(id=-1, habit_id=1, entry_date=today, created_at=now)
    
    def test_entry_validation_invalid_habit_id(self):
        """Test that invalid habit ID raises ValueError."""
        now = datetime.now()
        today = date.today()
        
        with pytest.raises(ValueError, match="Habit ID must be positive"):
            Entry(id=1, habit_id=0, entry_date=today, created_at=now)
        
        with pytest.raises(ValueError, match="Habit ID must be positive"):
            Entry(id=1, habit_id=-1, entry_date=today, created_at=now)
    
    def test_entry_validation_future_date(self):
        """Test that future entry date raises ValueError."""
        now = datetime.now()
        tomorrow = date.today() + date.resolution
        
        with pytest.raises(ValueError, match="Entry date cannot be in the future"):
            Entry(id=1, habit_id=1, entry_date=tomorrow, created_at=now)
    
    def test_entry_validation_today_date(self):
        """Test that today's date is valid."""
        now = datetime.now()
        today = date.today()
        
        # Should not raise any error
        entry = Entry(id=1, habit_id=1, entry_date=today, created_at=now)
        assert entry.entry_date == today
    
    def test_entry_validation_past_date(self):
        """Test that past date is valid."""
        now = datetime.now()
        yesterday = date.today() - date.resolution
        
        # Should not raise any error
        entry = Entry(id=1, habit_id=1, entry_date=yesterday, created_at=now)
        assert entry.entry_date == yesterday 