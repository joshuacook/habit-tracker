"""Unit tests for the database module."""

import pytest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from habit.db import HabitDatabase
from habit.models import Habit, Entry


class TestHabitDatabase:
    """Test cases for HabitDatabase class."""
    
    @pytest.fixture
    def temp_db_path(self, tmp_path):
        """Create a temporary database path."""
        return tmp_path / "test_habits.db"
    
    @pytest.fixture
    def db(self, temp_db_path):
        """Create a HabitDatabase instance with temporary path."""
        return HabitDatabase(temp_db_path)
    
    def test_init_database_creates_tables(self, db):
        """Test that init_database creates the required tables."""
        db.init_database()
        
        # Check that tables exist
        conn = db._get_connection()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        
        assert "habits" in tables
        assert "entries" in tables
    
    def test_init_database_is_idempotent(self, db):
        """Test that init_database can be called multiple times safely."""
        db.init_database()
        db.init_database()  # Should not raise any errors
        
        # Verify tables still exist
        conn = db._get_connection()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        
        assert "habits" in tables
        assert "entries" in tables
    
    def test_add_habit_success(self, db):
        """Test adding a habit successfully."""
        db.init_database()
        habit = db.add_habit("Test Habit")
        
        assert habit.name == "Test Habit"
        assert habit.id > 0
        assert isinstance(habit.created_at, datetime)
    
    def test_add_habit_duplicate_raises_error(self, db):
        """Test that adding a duplicate habit raises ValueError."""
        db.init_database()
        db.add_habit("Test Habit")
        
        with pytest.raises(ValueError, match="Habit 'Test Habit' already exists"):
            db.add_habit("Test Habit")
    
    def test_get_habit_by_name_found(self, db):
        """Test getting a habit by name when it exists."""
        db.init_database()
        original_habit = db.add_habit("Test Habit")
        found_habit = db.get_habit_by_name("Test Habit")
        
        assert found_habit is not None
        assert found_habit.id == original_habit.id
        assert found_habit.name == original_habit.name
    
    def test_get_habit_by_name_not_found(self, db):
        """Test getting a habit by name when it doesn't exist."""
        db.init_database()
        found_habit = db.get_habit_by_name("Nonexistent")
        
        assert found_habit is None
    
    def test_mark_habit_done_success(self, db):
        """Test marking a habit as done successfully."""
        db.init_database()
        habit = db.add_habit("Test Habit")
        entry = db.mark_habit_done("Test Habit")
        
        assert entry.habit_id == habit.id
        assert entry.entry_date == date.today()
        assert entry.id > 0
    
    def test_mark_habit_done_idempotent(self, db):
        """Test that marking a habit done is idempotent."""
        db.init_database()
        db.add_habit("Test Habit")
        
        entry1 = db.mark_habit_done("Test Habit")
        entry2 = db.mark_habit_done("Test Habit")
        
        # Should return the same entry
        assert entry1.id == entry2.id
        assert entry1.habit_id == entry2.habit_id
        assert entry1.entry_date == entry2.entry_date
    
    def test_mark_habit_done_nonexistent_raises_error(self, db):
        """Test that marking a nonexistent habit done raises ValueError."""
        db.init_database()
        
        with pytest.raises(ValueError, match="Habit 'Nonexistent' not found"):
            db.mark_habit_done("Nonexistent")
    
    def test_list_habits_empty(self, db):
        """Test listing habits when none exist."""
        db.init_database()
        habits = db.list_habits()
        
        assert habits == []
    
    def test_list_habits_with_completion_status(self, db):
        """Test listing habits with completion status."""
        db.init_database()
        habit1 = db.add_habit("Habit 1")
        habit2 = db.add_habit("Habit 2")
        
        # Mark one habit as done
        db.mark_habit_done("Habit 1")
        
        habits = db.list_habits()
        
        assert len(habits) == 2
        assert habits[0].name == "Habit 1"
        assert habits[0].completed_today is True
        assert habits[1].name == "Habit 2"
        assert habits[1].completed_today is False
    
    def test_list_habits_show_all(self, db):
        """Test listing habits with show_all=True."""
        db.init_database()
        habit1 = db.add_habit("Habit 1")
        habit2 = db.add_habit("Habit 2")
        
        # Mark one habit as done
        db.mark_habit_done("Habit 1")
        
        habits = db.list_habits(show_all=True)
        
        assert len(habits) == 2
        assert habits[0].name == "Habit 1"
        assert habits[0].completed_today is True
        assert habits[1].name == "Habit 2"
        assert habits[1].completed_today is False
    
    def test_get_stats_empty(self, db):
        """Test getting stats when no habits exist."""
        db.init_database()
        stats = db.get_stats(7)
        
        assert stats == []
    
    def test_get_stats_with_data(self, db):
        """Test getting stats with habit data."""
        db.init_database()
        db.add_habit("Test Habit")
        
        # Mark habit as done for today
        db.mark_habit_done("Test Habit")
        
        stats = db.get_stats(1)
        
        assert len(stats) == 1
        assert stats[0][0] == "Test Habit"
        assert stats[0][1] == 100.0  # 100% completion for 1 day
    
    def test_get_stats_multiple_days(self, db):
        """Test getting stats over multiple days."""
        db.init_database()
        db.add_habit("Test Habit")
        
        # Mark habit as done for today
        db.mark_habit_done("Test Habit")
        
        stats = db.get_stats(7)
        
        assert len(stats) == 1
        assert stats[0][0] == "Test Habit"
        # Should be 1/7 = 14.29% completion
        assert abs(stats[0][1] - 14.29) < 0.1
    
    def test_context_manager(self, db):
        """Test that HabitDatabase works as a context manager."""
        db.init_database()
        
        with db as db_instance:
            assert db_instance is db
            assert db_instance.connection is not None
        
        # Connection should be closed after context exit
        assert db.connection is None
    
    def test_close_connection(self, db):
        """Test that close() properly closes the connection."""
        db.init_database()
        db._get_connection()  # Create connection
        
        assert db.connection is not None
        db.close()
        assert db.connection is None 