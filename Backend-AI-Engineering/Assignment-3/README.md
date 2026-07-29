# BE-02: Connecting CRUD to SQLite Database

**Week 3 · Foundations**

Replaced the in-memory task list from Assignment 1 with a persistent SQLite database. The API endpoints remain identical — only the storage layer changed.

## Quick Start

```bash
python server.py
```

Server runs on `http://localhost:8000`. The database file `tasks.db` is created automatically on first run.

## API Endpoints

All endpoints return JSON.

| Method | Path | Description | Status |
|--------|------|-------------|--------|
| GET | /tasks | List all tasks | 200 |
| GET | /tasks/{id} | Get one task | 200 / 404 |
| POST | /tasks | Create a task | 201 / 400 |
| PUT | /tasks/{id} | Update a task | 200 / 404 |
| DELETE | /tasks/{id} | Delete a task | 200 / 404 |

### Example requests

```bash
curl http://localhost:8000/tasks
curl http://localhost:8000/tasks/1
curl -X POST localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
curl -X PUT localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"done":true}'
curl -X DELETE localhost:8000/tasks/1
```

## Database

### Why SQLite

- Zero setup — no server to install, no config, no credentials
- Built into Python's standard library (`sqlite3`)
- Single file (`tasks.db`) — easy to inspect, backup, or delete
- Perfect for development and learning; easy to swap for PostgreSQL later

### Database file

Stored as `tasks.db` in the project root. Created automatically if missing.

### Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    done INTEGER DEFAULT 0
);
```

### Example SQL queries (Stage 4)

```sql
-- List every task
SELECT * FROM tasks;

-- Show only completed tasks
SELECT * FROM tasks WHERE done = 1;

-- Count all tasks
SELECT COUNT(*) FROM tasks;

-- Mark every task as completed
UPDATE tasks SET done = 1;

-- Delete all completed tasks
DELETE FROM tasks WHERE done = 1;
```

Open `tasks.db` with [DB Browser for SQLite](https://sqlitebrowser.org/) to explore manually.

## Persistence

Restart the server — your data survives.
