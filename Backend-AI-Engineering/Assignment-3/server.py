from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os

DB_FILE = "tasks.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tasks "
        "(id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER DEFAULT 0)"
    )
    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    if count == 0:
        examples = [
            ("Buy groceries", 0),
            ("Finish homework", 0),
            ("Go for a walk", 0),
        ]
        conn.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", examples)
        conn.commit()
    conn.close()


def dict_from_row(row):
    return {"id": row[0], "title": row[1], "done": bool(row[2])}


class TaskHandler(BaseHTTPRequestHandler):
    def _send(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _get_path_parts(self):
        parts = self.path.strip("/").split("/")
        return parts

    def do_GET(self):
        parts = self._get_path_parts()
        conn = sqlite3.connect(DB_FILE)

        if parts == ["tasks"]:
            rows = conn.execute("SELECT id, title, done FROM tasks").fetchall()
            tasks = [dict_from_row(r) for r in rows]
            conn.close()
            self._send(200, tasks)

        elif len(parts) == 2 and parts[0] == "tasks":
            try:
                task_id = int(parts[1])
            except ValueError:
                conn.close()
                self._send(400, {"error": "Invalid task ID"})
                return
            row = conn.execute(
                "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
            conn.close()
            if row:
                self._send(200, dict_from_row(row))
            else:
                self._send(404, {"error": "Task not found"})

        else:
            conn.close()
            self._send(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/tasks":
            self._send(404, {"error": "Not found"})
            return
        body = self._read_body()
        title = body.get("title")
        if not title or not title.strip():
            self._send(400, {"error": "Title is required"})
            return
        conn = sqlite3.connect(DB_FILE)
        cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title.strip(),))
        conn.commit()
        task_id = cur.lastrowid
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        conn.close()
        self._send(201, dict_from_row(row))

    def do_PUT(self):
        parts = self._get_path_parts()
        if len(parts) != 2 or parts[0] != "tasks":
            self._send(404, {"error": "Not found"})
            return
        try:
            task_id = int(parts[1])
        except ValueError:
            self._send(400, {"error": "Invalid task ID"})
            return
        body = self._read_body()
        conn = sqlite3.connect(DB_FILE)
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if not row:
            conn.close()
            self._send(404, {"error": "Task not found"})
            return
        title = body.get("title", row[1])
        done = body.get("done", bool(row[2]))
        conn.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (title, int(done), task_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        conn.close()
        self._send(200, dict_from_row(row))

    def do_DELETE(self):
        parts = self._get_path_parts()
        if len(parts) != 2 or parts[0] != "tasks":
            self._send(404, {"error": "Not found"})
            return
        try:
            task_id = int(parts[1])
        except ValueError:
            self._send(400, {"error": "Invalid task ID"})
            return
        conn = sqlite3.connect(DB_FILE)
        row = conn.execute(
            "SELECT id FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if not row:
            conn.close()
            self._send(404, {"error": "Task not found"})
            return
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        self._send(200, {"message": "Task deleted"})


if __name__ == "__main__":
    init_db()
    server = HTTPServer(("localhost", 8000), TaskHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
