"""Database operations for the habit tracker."""

from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple

from .models import Habit, Entry


class HabitDatabase:
    """SQLite database wrapper for habit tracking."""
    
    def __init__(self, db_path: Optional[Path] = None) -> None:
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file. Defaults to 'habits.db' in current directory.
        """
        self.db_path = db_path or Path("habits.db")
        self.connection: Optional[sqlite3.Connection] = None
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection, creating it if necessary."""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def init_database(self) -> None:
        """Initialize the database with required tables."""
        conn = self._get_connection()
        
        # Create habits table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create entries table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                entry_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (id),
                UNIQUE(habit_id, entry_date)
            )
        """)
        
        conn.commit()
    
    def add_habit(self, name: str) -> Habit:
        """Add a new habit to the database.
        
        Args:
            name: Name of the habit to add.
            
        Returns:
            The created Habit object.
            
        Raises:
            ValueError: If habit with this name already exists.
        """
        conn = self._get_connection()
        
        try:
            cursor = conn.execute(
                "INSERT INTO habits (name) VALUES (?)",
                (name,)
            )
            habit_id = cursor.lastrowid
            if habit_id is None:
                raise RuntimeError("Failed to get habit ID from database")
            conn.commit()
            
            return Habit(id=habit_id, name=name, created_at=datetime.now())
        except sqlite3.IntegrityError:
            raise ValueError(f"Habit '{name}' already exists")
    
    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        """Get a habit by name.
        
        Args:
            name: Name of the habit to find.
            
        Returns:
            Habit object if found, None otherwise.
        """
        conn = self._get_connection()
        row = conn.execute(
            "SELECT * FROM habits WHERE name = ?",
            (name,)
        ).fetchone()
        
        if row is None:
            return None
        
        return Habit(
            id=row["id"],
            name=row["name"],
            created_at=datetime.fromisoformat(row["created_at"])
        )
    
    def mark_habit_done(self, name: str) -> Entry:
        """Mark a habit as completed for today.
        
        Args:
            name: Name of the habit to mark as done.
            
        Returns:
            The created Entry object.
            
        Raises:
            ValueError: If habit doesn't exist.
        """
        habit = self.get_habit_by_name(name)
        if habit is None:
            raise ValueError(f"Habit '{name}' not found")
        
        conn = self._get_connection()
        today = date.today()
        
        try:
            cursor = conn.execute(
                "INSERT INTO entries (habit_id, entry_date) VALUES (?, ?)",
                (habit.id, today)
            )
            entry_id = cursor.lastrowid
            if entry_id is None:
                raise RuntimeError("Failed to get entry ID from database")
            conn.commit()
            
            return Entry(
                id=entry_id,
                habit_id=habit.id,
                entry_date=today,
                created_at=datetime.now()
            )
        except sqlite3.IntegrityError:
            # Entry already exists for today
            row = conn.execute(
                "SELECT * FROM entries WHERE habit_id = ? AND entry_date = ?",
                (habit.id, today)
            ).fetchone()
            
            return Entry(
                id=row["id"],
                habit_id=habit.id,
                entry_date=today,
                created_at=datetime.fromisoformat(row["created_at"])
            )
    
    def list_habits(self, show_all: bool = False) -> List[Habit]:
        """List all habits with their completion status.
        
        Args:
            show_all: If True, show all habits. If False, only show today's status.
            
        Returns:
            List of Habit objects with completion status.
        """
        conn = self._get_connection()
        
        if show_all:
            # Show all habits with completion status for today
            query = """
                SELECT h.*, 
                       CASE WHEN e.id IS NOT NULL THEN 1 ELSE 0 END as completed_today
                FROM habits h
                LEFT JOIN entries e ON h.id = e.habit_id AND e.entry_date = ?
                ORDER BY h.name
            """
            rows = conn.execute(query, (date.today(),)).fetchall()
        else:
            # Show only habits that have been created
            rows = conn.execute(
                "SELECT * FROM habits ORDER BY name"
            ).fetchall()
        
        habits = []
        for row in rows:
            habit = Habit(
                id=row["id"],
                name=row["name"],
                created_at=datetime.fromisoformat(row["created_at"])
            )
            
            if show_all:
                habit.completed_today = bool(row["completed_today"])
            else:
                # Check if completed today
                entry = conn.execute(
                    "SELECT id FROM entries WHERE habit_id = ? AND entry_date = ?",
                    (habit.id, date.today())
                ).fetchone()
                habit.completed_today = entry is not None
            
            habits.append(habit)
        
        return habits
    
    def get_stats(self, days: int) -> List[Tuple[str, float]]:
        """Get completion statistics for habits over a time period.
        
        Args:
            days: Number of days to look back for statistics.
            
        Returns:
            List of tuples containing (habit_name, completion_percentage).
        """
        conn = self._get_connection()
        
        # Calculate the start date
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        
        query = """
            SELECT h.name,
                   COUNT(e.id) as completed_days,
                   ? as total_days
            FROM habits h
            LEFT JOIN entries e ON h.id = e.habit_id 
                AND e.entry_date BETWEEN ? AND ?
            GROUP BY h.id, h.name
            ORDER BY h.name
        """
        
        rows = conn.execute(query, (days, start_date, end_date)).fetchall()
        
        stats = []
        for row in rows:
            completion_rate = (row["completed_days"] / row["total_days"]) * 100
            stats.append((row["name"], completion_rate))
        
        return stats
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def __enter__(self) -> HabitDatabase:
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close() 