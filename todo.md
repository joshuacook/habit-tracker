# TODO Backlog

> Cursor: Work through items **one at a time**; ask clarifying questions whenever unsure.

| ID | Task | Notes / Definition of Done |
|----|------|----------------------------|
| ~~T-01~~ | ~~**Scaffold project**~~ | ~~Create repo structure shown in *description.md*.~~ |
| | | **Completed**: Created `habit/` package with `__init__.py`, `cli.py`, `db.py`, `models.py`. Created `tests/` directory with `__init__.py`. Added `requirements.txt` with Click and pytest dependencies. All files include proper type hints, docstrings, and follow the project's coding conventions. |
| ~~T-02~~ | ~~**Write README skeleton**~~ | ~~Overview, install steps (`pipx`, venv), example session.~~ |
| | | **Completed**: Enhanced README with comprehensive installation instructions (pipx and venv options), detailed quick start guide, complete example session showing all commands, commands reference table, development setup instructions, and database schema documentation. Added setup.py for package installation. |
| ~~T-03~~ | ~~**Pin dependencies**~~ | ~~Add `Click`, `pytest`, dev tools to `requirements.txt`; update README.~~ |
| | | **Completed**: Pinned all dependencies to specific versions: Click==8.1.7, pytest==8.0.0, black==24.1.1, ruff==0.2.1, mypy==1.8.0. Updated setup.py to match requirements.txt. Added development tools section to README with usage instructions. All dependencies install successfully. |
| ~~T-04~~ | ~~**Implement `init`**~~ | ~~`habit init` creates `habits.db` with `habits` + `entries` tables.~~ |
| | | **Completed**: Implemented and tested the `init` command. Running `habit init` creates a `habits.db` SQLite file with the correct `habits` and `entries` tables. The command is idempotent and can be run multiple times safely. |
| | | **Completed**: Implemented and tested the `add` command. Adding a new habit works as expected, and trying to add a duplicate habit name results in a clear error message due to the UNIQUE constraint. |
| | | **Completed**: Implemented and tested the `done` command. Marking a habit as done for today works and is idempotent (safe to run multiple times). Error handling is in place for non-existent habits. |
| T-07 | **Implement `list`** | `--today` (default) vs. `--all`; nice emoji ✔️ / ❌. |
| T-08 | **Implement `stats`** | Percentage complete over window; bar chart text (e.g., `#####-----`). |
| T-09 | **Unit tests** | Cover `db.py` helpers + each CLI command. |
| T-10 | **Docstrings & type hints** | Ensure every public function passes `ruff`, `mypy`. |
| T-11 | **Update docs** | Flesh out README usage; add `docs/schema.md` with ER diagram (ASCII). |
| T-12 | **Release v0.1.0** | Tag, create `CHANGELOG.md`, update version badge in README. |

*(Stretch Tasks – tackle after v0.1.0)*

* ST-01 Export CSV report  
* ST-02 Delete habit command (`remove`)  
* ST-03 Simple curses TUI wrapper  
* ST-04 GitHub Actions CI (lint + tests)

---

Cursor, when an item is *done*:

1. Mark it completed (~~strike through~~) in this file.  
2. Summarize what changed in plain English under the task entry.  
3. Then proceed to the next unstarted task.
