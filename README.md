# Lightweight Habit-Tracker CLI

A tiny command-line tool that helps a single user record and review daily habits.  
The focus is *simplicity*—one self-contained SQLite file and a handful of clear commands.

## Installation

### Option 1: Using pipx (Recommended)
```bash
# Install directly from this repository
pipx install git+https://github.com/yourusername/habit-tracker.git

# Or install in editable mode for development
pipx install --editable .
```

### Option 2: Using virtual environment
```bash
# Clone the repository
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

1. **Initialize the database:**
   ```bash
   habit init
   ```

2. **Add your first habit:**
   ```bash
   habit add "Drink water"
   habit add "Exercise"
   habit add "Read 30 minutes"
   ```

3. **Mark habits as done:**
   ```bash
   habit done "Drink water"
   habit done "Exercise"
   ```

4. **Check your progress:**
   ```bash
   habit list
   habit stats --days 7
   ```

## Example Session

```bash
$ habit init
✅ Database initialized successfully!

$ habit add "Morning meditation"
✅ Added habit: Morning meditation

$ habit add "Drink 8 glasses of water"
✅ Added habit: Drink 8 glasses of water

$ habit add "Read before bed"
✅ Added habit: Read before bed

$ habit done "Morning meditation"
✅ Marked 'Morning meditation' as done for today!

$ habit done "Drink 8 glasses of water"
✅ Marked 'Drink 8 glasses of water' as done for today!

$ habit list
✔️ Morning meditation
✔️ Drink 8 glasses of water
❌ Read before bed

$ habit stats --days 7
📊 Stats for the last 7 days:
Morning meditation: ████████████████████ 100.0%
Drink 8 glasses of water: ████████████████████ 100.0%
Read before bed: ░░░░░░░░░░░░░░░░░░░░ 0.0%

$ habit list --all
✔️ Morning meditation
✔️ Drink 8 glasses of water
❌ Read before bed
```

## Commands Reference

| Command | Example | Description |
|---------|---------|-------------|
| `init`  | `habit init` | Create the database and starter tables. |
| `add`   | `habit add "Drink water"` | Register a new habit. |
| `done`  | `habit done "Drink water"` | Mark today's completion (idempotent). |
| `list`  | `habit list --all` | Show all habits with today's status. |
| `stats` | `habit stats --days 7` | Show completion % per habit over a window. |

### Command Options

- `habit list --all`: Show all habits (default shows only today's status)
- `habit stats --days N`: Show stats for the last N days (default: 7)

## Key Commands (MVP)

| Command | Example | What it does |
|---------|---------|--------------|
| `init`  | `habit init` | Create the database and starter tables. |
| `add`   | `habit add "Drink water"` | Register a new habit. |
| `done`  | `habit done "Drink water"` | Mark today's completion (creates row if missing). |
| `list`  | `habit list --today` | Show all habits with today's status. |
| `stats` | `habit stats --days 7` | Show completion % per habit over a window. |

*(Stretch)*: export CSV, delete habits, emoji progress bar, simple TUI later.

## Tech/Architecture
| Layer | Choice | Notes |
|-------|--------|-------|
| Language | **Python 3.12** | Type-annotated, PEP 8. |
| DB      | **sqlite3** (std-lib) | Single file in project root (`habits.db`). |
| CLI     | **Click ≥ 8** | Nice help text & colors. |
| Tests   | **pytest ≥ 8** | Aim for ~80 % coverage. |

Folder layout:
```
habit_tracker/
│─ habit/              # package
│   ├─ __init__.py
│   ├─ cli.py          # Click entry
│   ├─ db.py
│   └─ models.py
├─ tests/
├─ README.md
├─ description.md
├─ todo.md
└─ requirements.txt
```

## Development

### Setup Development Environment
```bash
# Clone and setup
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting and formatting
ruff check .
black .
mypy habit/
```

### Development Tools

The project uses several development tools to maintain code quality:

- **pytest**: Testing framework
- **black**: Code formatter
- **ruff**: Fast Python linter
- **mypy**: Static type checker

All tools are pinned to specific versions in `requirements.txt` for reproducible builds.

### Database Schema

The tool uses a simple SQLite database with two tables:

- **habits**: Stores habit definitions (id, name, created_at)
- **entries**: Stores daily completions (id, habit_id, entry_date, created_at)

The database file (`habits.db`) is created in the project root when you run `habit init`.

## Documentation Rules (teach Cursor these!)

1. **Markdown only**, UTF-8, LF line endings.  
2. Heading levels: `#`, `##`, `###`; never skip.  
3. Sentences ≤ 25 words when possible; use active voice.  
4. Every public function *must* have a Google-style docstring.  
5. Changelogs belong in `CHANGELOG.md`, semver headings (`## [vX.Y.Z] – YYYY-MM-DD`).  
6. Code blocks: triple-back-tick + language, no tabs.  
7. When Cursor edits docs, it should preserve comments denoted by `<!-- doc-guard -->`.

## Coding Conventions

* 4-space indent, `black` + `ruff`.
* Type hints everywhere (`from __future__ import annotations`).
* Prefer `Pathlib` over `os.path`.
* No network calls, no external DBs.

## License
MIT (include full text in `LICENSE`).

---

Ask Cursor to **confirm understanding** of this description and the doc rules before starting on the todos.
