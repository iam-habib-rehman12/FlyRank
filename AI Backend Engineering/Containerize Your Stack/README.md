# A3 - Containerize Your Stack

A Dockerized FastAPI task service backed by PostgreSQL. The API and database start together with one command, and a named Docker volume keeps task data across container restarts.

## Architecture

```text
HTTP request
    |
FastAPI routes (app/main.py)
    |
TaskService (app/service.py)
    |
TaskRepository protocol (app/repository.py)
    |
PostgresTaskRepository (app/postgres_repository.py)
    |
PostgreSQL container + taskdata volume
```

The routes and business service depend on the `TaskRepository` contract, not on PostgreSQL. Database SQL is isolated in `PostgresTaskRepository`; the storage swap is made where the application constructs that repository. The route contracts and service behavior therefore do not change when storage changes.

All user-provided SQL values use psycopg `%s` placeholders and are passed separately. No route builds SQL strings.

## Requirements implemented

- PostgreSQL 17 runs in Docker.
- FastAPI and PostgreSQL start with `docker compose up`.
- The API reaches PostgreSQL through the Compose service hostname `db`.
- Credentials come from a git-ignored `.env`.
- A safe `.env.example` is committed.
- `database/init.sql` creates the table and seeds three tasks only when it is empty.
- A named `taskdata` volume preserves rows.
- All five CRUD endpoints use PostgreSQL.
- The repository uses parameterized queries.
- A database-aware `GET /health` endpoint runs `SELECT 1`.
- Compose waits for the database health check before starting the API.
- Service tests demonstrate that route/business contracts are independent of storage.

## Project structure

```text
Containerize Your Stack/
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- models.py
|   |-- postgres_repository.py
|   |-- repository.py
|   `-- service.py
|-- database/
|   `-- init.sql
|-- tests/
|   `-- test_service.py
|-- .dockerignore
|-- .env.example
|-- .gitignore
|-- compose.yaml
|-- Dockerfile
|-- requirements.txt
`-- README.md
```

## Prerequisites

Install either:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/), or
- Docker Engine with the Compose plugin.

Confirm it is available:

```bash
docker --version
docker compose version
```

## Run the complete stack

Clone the repository and enter this assignment:

```bash
git clone https://github.com/iam-habib-rehman12/FlyRank.git
cd "FlyRank/AI Backend Engineering/Containerize Your Stack"
```

Create the local environment file:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Choose a local database password in `.env`, then start everything:

```bash
docker compose up --build
```

The API becomes available at:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- PostgreSQL: localhost:5432

Stop the stack without deleting stored data:

```bash
docker compose down
```

> Do not run `docker compose down -v` during the persistence test. The `-v` option deliberately deletes the named volume and its data.

## Environment variables

| Variable | Purpose | Example |
|---|---|---|
| `POSTGRES_USER` | Local database user | `postgres` |
| `POSTGRES_PASSWORD` | Local database password | choose locally |
| `POSTGRES_DB` | Database name | `tasks` |
| `POSTGRES_PORT` | Host Postgres port | `5432` |
| `API_PORT` | Host API port | `8000` |

Compose constructs `DATABASE_URL` inside the API container and uses `db` as the host. Real values remain in `.env`, which Git ignores.

## API reference

| Method | Endpoint | Purpose | Success |
|---|---|---|---:|
| `GET` | `/health` | Check API and database | `200` |
| `GET` | `/tasks` | List all tasks | `200` |
| `GET` | `/tasks/{id}` | Read one task | `200` |
| `POST` | `/tasks` | Create a task | `201` |
| `PUT` | `/tasks/{id}` | Replace a task | `200` |
| `DELETE` | `/tasks/{id}` | Delete a task | `204` |

Invalid request bodies return `400` with a JSON error. Unknown task IDs return `404` with:

```json
{"error": "Task not found"}
```

## CRUD verification

### List the seed data

```bash
curl -i http://localhost:8000/tasks
```

Expected response shape:

```http
HTTP/1.1 200 OK
content-type: application/json

[
  {"id":1,"title":"Learn Docker fundamentals","done":false},
  {"id":2,"title":"Connect FastAPI to Postgres","done":false},
  {"id":3,"title":"Prove volume persistence","done":false}
]
```

### Create

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Persistent task","done":false}'
```

Expected: `201 Created`.

### Read

```bash
curl -i http://localhost:8000/tasks/4
```

Expected: `200 OK`.

### Update

```bash
curl -i -X PUT http://localhost:8000/tasks/4 \
  -H "Content-Type: application/json" \
  -d '{"title":"Persistent task","done":true}'
```

Expected: `200 OK` with `"done": true`.

### Delete

```bash
curl -i -X DELETE http://localhost:8000/tasks/4
```

Expected: `204 No Content`.

### Unknown task

```bash
curl -i http://localhost:8000/tasks/999999
```

Expected: `404 Not Found` and `{"error":"Task not found"}`.

## Inspect PostgreSQL directly

List tables:

```bash
docker compose exec db psql -U postgres -d tasks -c "\dt"
```

Read task rows:

```bash
docker compose exec db psql -U postgres -d tasks \
  -c "SELECT id, title, done FROM tasks ORDER BY id;"
```

If you changed `POSTGRES_USER` or `POSTGRES_DB`, use those values in the command.

## Persistence proof procedure

1. Start the stack with `docker compose up --build`.
2. Create a task titled `Survives restart`.
3. Confirm it appears in `GET /tasks` and the direct SQL query.
4. Run `docker compose down`.
5. Run `docker compose up`.
6. Call `GET /tasks` again.
7. Confirm the same task ID and title are still present.

The task survives because Compose mounts the named `taskdata` volume at PostgreSQL's data directory:

```yaml
volumes:
  - taskdata:/var/lib/postgresql/data
```

Containers are replaceable processes. The volume owns the durable database files and outlives those containers.

Useful inspection command:

```bash
docker volume ls
```

## Database initialization

`database/init.sql` runs when PostgreSQL initializes a new empty volume. It:

1. creates `tasks` if missing;
2. inserts three example tasks only when no rows exist.

Starting the app repeatedly cannot duplicate seed data. Restarting Compose against the existing volume also does not rerun first-volume initialization.

## Tests

The service tests use an in-memory implementation of the same repository protocol:

```bash
python -m pytest -q
```

This proves the business behavior does not depend on psycopg or PostgreSQL. The production dependency assembly selects `PostgresTaskRepository` without changing the service methods or HTTP routes.

## Security and reliability

- `.env` is excluded by both Git and the Docker build context.
- The repository contains no real database credentials.
- SQL values are always parameterized.
- The app image runs as a non-root user.
- PostgreSQL has a health check.
- The API waits for a healthy database.
- Connection pooling avoids opening a new database connection for every query.
- `GET /health` verifies the database with `SELECT 1`.

## Assignment checklist

- [x] PostgreSQL service in Docker
- [x] Named volume for persistence
- [x] API and database start with one Compose command
- [x] Environment-based connection settings
- [x] `.env` ignored
- [x] `.env.example` committed
- [x] Automatic table creation
- [x] Seed-only-when-empty SQL
- [x] PostgreSQL repository implementation
- [x] Parameterized CRUD queries
- [x] Storage-independent service and routes
- [x] Required status codes and JSON errors
- [x] Health endpoint with database check
- [x] Persistence verification procedure documented
- [x] Public repository with incremental commits

## Assignment

FlyRank Backend AI Engineering - BE-04 - A3 Containerize Your Stack.
