# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.1.0] - 2024-07-02

### Added
- Initial release of the habit tracker CLI
- Core commands: `init`, `add`, `done`, `list`, `stats`
- SQLite database backend with habits and entries tables
- Comprehensive test suite with 99% coverage
- Type hints and Google-style docstrings throughout
- Development tools: black, ruff, mypy, pytest
- Complete documentation including README and schema docs

### Features
- **init**: Initialize database with required tables
- **add**: Add new habits with unique name constraint
- **done**: Mark habits as completed for today (idempotent)
- **list**: Show habits with completion status using emojis
- **stats**: Display completion statistics with visual progress bars

### Technical Details
- Python 3.12+ with type annotations
- Click framework for CLI interface
- SQLite database with proper constraints
- Comprehensive error handling
- Context manager support for database connections

### Documentation
- Complete README with installation and usage instructions
- Database schema documentation with ER diagram
- API documentation with docstrings
- Development setup instructions 