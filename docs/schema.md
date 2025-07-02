# Database Schema

## Overview

The habit tracker uses a simple SQLite database with two main tables: `habits` and `entries`.

## Entity Relationship Diagram

```
┌─────────────────┐         ┌─────────────────┐
│     habits      │         │     entries     │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │◄────────┤ id (PK)         │
│ name (UNIQUE)   │         │ habit_id (FK)   │
│ created_at      │         │ entry_date      │
└─────────────────┘         │ created_at      │
                            └─────────────────┘
```

## Table Definitions

### habits

Stores habit definitions.

| Column     | Type      | Constraints           | Description                    |
|------------|-----------|----------------------|--------------------------------|
| id         | INTEGER   | PRIMARY KEY AUTOINCR  | Unique habit identifier        |
| name       | TEXT      | UNIQUE NOT NULL       | Habit name (must be unique)    |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIME  | When the habit was created     |

### entries

Stores daily completion records.

| Column     | Type      | Constraints                    | Description                    |
|------------|-----------|-------------------------------|--------------------------------|
| id         | INTEGER   | PRIMARY KEY AUTOINCR          | Unique entry identifier        |
| habit_id   | INTEGER   | NOT NULL, FOREIGN KEY         | References habits.id           |
| entry_date | DATE      | NOT NULL                      | Date of completion             |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIME          | When the entry was created     |

## Constraints

- **UNIQUE(habit_id, entry_date)**: Prevents duplicate entries for the same habit on the same date
- **FOREIGN KEY(habit_id)**: Ensures referential integrity with habits table
- **UNIQUE(name)**: Ensures habit names are unique

## Sample Data

### habits table
```
id | name           | created_at
---+----------------+-------------------
1  | Drink water    | 2024-01-01 10:00
2  | Exercise       | 2024-01-01 10:05
3  | Read 30 min    | 2024-01-01 10:10
```

### entries table
```
id | habit_id | entry_date | created_at
---+----------+------------+-------------------
1  | 1        | 2024-01-01 | 2024-01-01 20:00
2  | 2        | 2024-01-01 | 2024-01-01 18:30
3  | 1        | 2024-01-02 | 2024-01-02 19:45
```

## Relationships

- **One-to-Many**: One habit can have many entries (one per day)
- **Many-to-One**: Many entries can belong to one habit

## Indexes

The database automatically creates indexes on:
- Primary keys (id columns)
- Foreign keys (habit_id)
- Unique constraints (name, habit_id + entry_date)

## Data Integrity

The schema ensures:
- No duplicate habits with the same name
- No duplicate entries for the same habit on the same date
- All entries reference valid habits
- Proper date handling for completion tracking 