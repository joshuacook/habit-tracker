"""Command-line interface for the habit tracker."""

from __future__ import annotations

import click
from pathlib import Path

from .db import HabitDatabase
from .models import Habit, Entry


@click.group()
@click.version_option()
def main() -> None:
    """Lightweight Habit-Tracker CLI.
    
    A simple command-line tool to track daily habits using SQLite.
    """
    pass


@main.command()
def init() -> None:
    """Initialize the habit tracker database."""
    db = HabitDatabase()
    db.init_database()
    click.echo("✅ Database initialized successfully!")


@main.command()
@click.argument("name")
def add(name: str) -> None:
    """Add a new habit to track."""
    db = HabitDatabase()
    try:
        habit = db.add_habit(name)
        click.echo(f"✅ Added habit: {habit.name}")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")


@main.command()
@click.argument("name")
def done(name: str) -> None:
    """Mark a habit as completed for today."""
    db = HabitDatabase()
    try:
        entry = db.mark_habit_done(name)
        click.echo(f"✅ Marked '{name}' as done for today!")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")


@main.command()
@click.option("--all", "show_all", is_flag=True, help="Show all habits, not just today's status")
def list(show_all: bool) -> None:
    """List habits and their status."""
    db = HabitDatabase()
    habits = db.list_habits(show_all=show_all)
    
    if not habits:
        click.echo("No habits found. Use 'habit add <name>' to create your first habit.")
        return
    
    for habit in habits:
        status = "✔️" if habit.completed_today else "❌"
        click.echo(f"{status} {habit.name}")


@main.command()
@click.option("--days", default=7, help="Number of days to show stats for")
def stats(days: int) -> None:
    """Show completion statistics for habits."""
    db = HabitDatabase()
    stats_data = db.get_stats(days)
    
    if not stats_data:
        click.echo("No habits found. Use 'habit add <name>' to create your first habit.")
        return
    
    click.echo(f"📊 Stats for the last {days} days:")
    for habit_name, completion_rate in stats_data:
        bar_length = 20
        filled = int(bar_length * completion_rate / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        click.echo(f"{habit_name}: {bar} {completion_rate:.1f}%")


if __name__ == "__main__":
    main() 