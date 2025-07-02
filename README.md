# Lightweight Habit-Tracker CLI

## Purpose
A tiny command-line tool that helps a single user record and review daily habits.  
The focus is *simplicity*—one self-contained SQLite file and a handful of clear commands.

## Key Commands (MVP)

| Command | Example | What it does |
|---------|---------|--------------|
| `init`  | `habit init` | Create the database and starter tables. |
| `add`   | `habit add "Drink water"` | Register a new habit. |
| `done`  | `habit done "Drink water"` | Mark today’s completion (creates row if missing). |
| `list`  | `habit list --today` | Show all habits with today’s status. |
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
