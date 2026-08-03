from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from .models import Task


class PostgresTaskRepository:
    def __init__(self, database_url: str) -> None:
        self._pool = ConnectionPool(
            conninfo=database_url,
            min_size=1,
            max_size=10,
            kwargs={"row_factory": dict_row},
            open=True,
        )
        self._pool.wait(timeout=30)

    def list(self) -> list[Task]:
        with self._pool.connection() as connection:
            rows = connection.execute(
                "SELECT id, title, done FROM tasks ORDER BY id"
            ).fetchall()
        return [Task(**row) for row in rows]

    def get(self, task_id: int) -> Task | None:
        with self._pool.connection() as connection:
            row = connection.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,),
            ).fetchone()
        return Task(**row) if row else None

    def create(self, title: str, done: bool = False) -> Task:
        with self._pool.connection() as connection:
            row = connection.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done
                """,
                (title, done),
            ).fetchone()
        return Task(**row)

    def update(
        self, task_id: int, title: str, done: bool
    ) -> Task | None:
        with self._pool.connection() as connection:
            row = connection.execute(
                """
                UPDATE tasks
                SET title = %s, done = %s
                WHERE id = %s
                RETURNING id, title, done
                """,
                (title, done, task_id),
            ).fetchone()
        return Task(**row) if row else None

    def delete(self, task_id: int) -> bool:
        with self._pool.connection() as connection:
            row = connection.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,),
            ).fetchone()
        return row is not None

    def ping(self) -> bool:
        with self._pool.connection() as connection:
            return connection.execute("SELECT 1").fetchone() is not None

    def close(self) -> None:
        self._pool.close()
