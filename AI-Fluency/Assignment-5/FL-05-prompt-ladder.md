# FL-05: Prompt Ladder

**Prompt Engineering — One Change at a Time**

---

## Domain: Building a task manager REST API (backend engineering)

---

## Baseline — The Weak Prompt

**Prompt:**
```
Build a REST API for a task manager.
```

**Output:**

Sure! Here's a REST API for a task manager using Node.js and Express:

```javascript
const express = require('express');
const app = express();
app.use(express.json());

let tasks = [];
let id = 1;

app.get('/tasks', (req, res) => {
  res.json(tasks);
});

app.post('/tasks', (req, res) => {
  const task = { id: id++, title: req.body.title, done: false };
  tasks.push(task);
  res.json(task);
});

app.put('/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id == req.params.id);
  if (task) Object.assign(task, req.body);
  res.json(task);
});

app.delete('/tasks/:id', (req, res) => {
  tasks = tasks.filter(t => t.id != req.params.id);
  res.sendStatus(204);
});

app.listen(3000);
```

**What changed:** — (baseline)
**What improved:** —
**What still failed:** No tech stack specified (guessed Node.js), no auth, no persistence, no validation, no error handling, inconsistent status codes, no database, single file everything.
**What I'd try next:** Tell it what I actually need and what stack I use.

---

## Version 1 — + Clearer Goal

**Layer added:** Clearer goal

**Prompt:**
```
Build a REST API for a personal task manager. Users should be able to sign up, log in, create tasks with due dates and priority levels, mark tasks complete, and filter by status or priority.
```

**Output:**

```javascript
const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
// ... (85 lines, includes user model, auth middleware, task CRUD with filters)

app.post('/signup', async (req, res) => {
  const hash = await bcrypt.hash(req.body.password, 10);
  users.push({ email: req.body.email, password: hash });
  res.status(201).json({ message: 'User created' });
});

app.post('/login', (req, res) => {
  // ... JWT token generation
});

app.get('/tasks', authenticate, (req, res) => {
  const { status, priority } = req.query;
  let result = tasks.filter(t => t.userId === req.userId);
  if (status) result = result.filter(t => t.status === status);
  if (priority) result = result.filter(t => t.priority === priority);
  res.json(result);
});
```

**What changed:** Prompt now specifies signup, login, due dates, priority, filtering.
**What improved:** Output includes auth, filters, more complete CRUD. Actually covers the feature set I asked for.
**What still failed:** Still guessed Node.js (wrong stack), no database (in-memory), no input validation, no error responses, inconsistent status codes, no tests, no file structure (single file).
**What I'd try next:** Tell it my actual tech stack so it stops guessing.

---

## Version 2 — + Defined Audience

**Layer added:** Audience

**Prompt:**
```
Build a REST API for a personal task manager. Users should be able to sign up, log in, create tasks with due dates and priority levels, mark tasks complete, and filter by status or priority.

This is for a solo developer building their first backend project. They know Python basics but have never built an API before.
```

**Output:**

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                   (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT,
                    due_date TEXT, priority TEXT, status TEXT)''')
    conn.close()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    conn = sqlite3.connect('tasks.db')
    conn.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                 (data['email'], data['password']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User created'}), 201

# ... (similar for login, task CRUD with filtering)
```

**What changed:** Added audience — "solo developer, knows Python basics, first API."
**What improved:** Switched to Python (right language guess), added SQLite for persistence, uses Flask (popular beginner framework). Output matches the audience's skill level.
**What still failed:** Passwords stored in plain text (no hashing), no input validation, no error handling, SQLite connection opened/closed per request (inefficient), status codes inconsistent, no project structure.
**What I'd try next:** Add tech stack constraints so it doesn't pick Flask without asking.

---

## Version 3 — + Constraints

**Layer added:** Constraints

**Prompt:**
```
Build a REST API for a personal task manager. Users should be able to sign up, log in, create tasks with due dates and priority levels, mark tasks complete, and filter by status or priority.

This is for a solo developer building their first backend project. They know Python basics but have never built an API before.

Constraints:
- Use Python 3.14 standard library only — no Flask, no FastAPI, no third-party packages
- Use http.server and sqlite3 (both built-in)
- Single-file is fine for now
- Must handle errors gracefully
```

**Output:**

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, sqlite3, hashlib, os

DB = 'tasks.db'

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                   (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT,
                    due_date TEXT, priority TEXT, status TEXT DEFAULT 'pending',
                    FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

class TaskHandler(BaseHTTPRequestHandler):
    def _send(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        if self.path == '/signup':
            # ... hash password, insert user
        elif self.path == '/login':
            # ... verify password, return token
        elif self.path == '/tasks':
            # ... validate, insert task
        else:
            self._send(404, {'error': 'not found'})
    # ... do_GET, do_PUT, do_DELETE for tasks with filters
```

**What changed:** Added constraints — Python stdlib only, http.server, sqlite3, no third-party packages.
**What improved:** Now uses the right stack. Hashed passwords (used hashlib). Proper HTTP method routing. Consistent JSON responses. File is self-contained and runnable. Matches the audience's setup (no pip install needed).
**What still failed:** No input validation on fields (empty title, invalid dates), no token expiry on auth, passwords hashed but no salt shown, no project structure guidance, no tests, status codes still inconsistent in some paths.
**What I'd try next:** Specify the output format — file structure, what the response schemas look like, error format.

---

## Version 4 — + Output Format

**Layer added:** Output format

**Prompt:**
```
Build a REST API for a personal task manager. Users should be able to sign up, log in, create tasks with due dates and priority levels, mark tasks complete, and filter by status or priority.

This is for a solo developer building their first backend project. They know Python basics but have never built an API before.

Constraints:
- Use Python 3.14 standard library only — no Flask, no FastAPI, no third-party packages
- Use http.server and sqlite3 (both built-in)
- Single-file is fine for now
- Must handle errors gracefully

Output format:
- Provide the full code in one block
- Include a separate response schema table showing what every endpoint returns (success + error)
- Show example curl commands for each endpoint
- Use this consistent JSON error format: {"error": "<message>", "code": <http_status>}
```

**Output:**

```python
# Full code (same as V3 but with validation added — checks for empty title,
# invalid email, missing fields. Every endpoint sends errors in {"error": ..., "code": ...} format)

# --- Response Schemas ---
# POST /signup
#   Success: 201 {"message": "User created"}
#   Error 400: {"error": "Email already registered", "code": 400}
#   Error 400: {"error": "Email and password required", "code": 400}
#
# POST /login
#   Success: 200 {"token": "<jwt>", "user_id": 1}
#   Error 401: {"error": "Invalid email or password", "code": 401}
#
# GET /tasks?status=pending&priority=high
#   Success: 200 [{"id": 1, "title": "...", "due_date": "...", "priority": "high", "status": "pending"}, ...]
#   Error 401: {"error": "Invalid or expired token", "code": 401}
#
# --- curl examples ---
# curl -X POST localhost:8000/signup -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"secret"}'
# curl -X POST localhost:8000/login -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"secret"}'
# curl localhost:8000/tasks -H "Authorization: Bearer <token>"
```

**What changed:** Specified output format — response schema table, curl examples, consistent error format.
**What improved:** Now I can see exactly what each endpoint returns without reading the code. The curl examples mean I can test immediately. Error format is consistent. Validation was added because the format spec forced thinking about error cases.
**What still failed:** No project structure (everything in one file is fine for v1 but no guidance on splitting later), no tests, no setup instructions, no type hints, no rate limiting or security hardening.
**What I'd try next:** Add quality criteria — what "good" means for this prompt so it self-checks.

---

## Version 5 — + Quality Criteria

**Layer added:** Quality criteria / review instructions

**Prompt:**
```
Build a REST API for a personal task manager. Users should be able to sign up, log in, create tasks with due dates and priority levels, mark tasks complete, and filter by status or priority.

This is for a solo developer building their first backend project. They know Python basics but have never built an API before.

Constraints:
- Use Python 3.14 standard library only — no Flask, no FastAPI, no third-party packages
- Use http.server and sqlite3 (both built-in)
- Single-file is fine for now
- Must handle errors gracefully

Output format:
- Provide the full code in one block
- Include a separate response schema table showing what every endpoint returns (success + error)
- Show example curl commands for each endpoint
- Use this consistent JSON error format: {"error": "<message>", "code": <http_status>}

Quality criteria — check your output against these before sending:
1. Every endpoint validates inputs before using them (empty strings, missing fields, wrong types)
2. Passwords are hashed with a salt
3. Auth tokens have an expiry
4. All database queries use parameterised statements (no string formatting)
5. Status codes: 201 for creation, 200 for success, 400 for bad request, 401 for auth failure, 404 for not found, 500 for server error
6. The server starts with `python server.py` — no extra steps
7. Every error returns the consistent {"error": ..., "code": ...} format
```

**Output:**

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, sqlite3, hashlib, os, time, secrets

DB = 'tasks.db'
TOKEN_EXPIRY = 86400  # 24 hours

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, salt TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                   (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT,
                    due_date TEXT, priority TEXT, status TEXT DEFAULT 'pending',
                    FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest(), salt

def verify_token(token):
    # Parse token, check expiry against stored timestamp
    ...

class TaskHandler(BaseHTTPRequestHandler):
    def _send(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _get_user_id(self):
        auth = self.headers.get('Authorization', '')
        user = verify_token(auth.replace('Bearer ', ''))
        if not user:
            self._send(401, {'error': 'Invalid or expired token', 'code': 401})
            return None
        return user

    def do_POST(self):
        body = self._read_body()
        if self.path == '/signup':
            if not body.get('email') or not body.get('password'):
                return self._send(400, {'error': 'Email and password required', 'code': 400})
            pw_hash, salt = hash_password(body['password'])
            try:
                conn = sqlite3.connect(DB)
                conn.execute('INSERT INTO users (email, password, salt) VALUES (?, ?, ?)',
                             (body['email'], pw_hash, salt))
                conn.commit()
                conn.close()
                self._send(201, {'message': 'User created'})
            except sqlite3.IntegrityError:
                self._send(400, {'error': 'Email already registered', 'code': 400})

        elif self.path == '/login':
            conn = sqlite3.connect(DB)
            row = conn.execute('SELECT * FROM users WHERE email = ?',
                               (body.get('email'),)).fetchone()
            conn.close()
            if not row:
                return self._send(401, {'error': 'Invalid email or password', 'code': 401})
            pw_hash, _ = hash_password(body.get('password', ''), row[3])
            if pw_hash != row[2]:
                return self._send(401, {'error': 'Invalid email or password', 'code': 401})
            token = secrets.token_hex(32)
            # Store token with timestamp
            self._send(200, {'token': token, 'user_id': row[0]})

        elif self.path == '/tasks':
            user_id = self._get_user_id()
            if user_id is None: return
            if not body.get('title'):
                return self._send(400, {'error': 'Title is required', 'code': 400})
            conn = sqlite3.connect(DB)
            conn.execute('''INSERT INTO tasks (user_id, title, due_date, priority)
                           VALUES (?, ?, ?, ?)''',
                         (user_id, body['title'], body.get('due_date', ''),
                          body.get('priority', 'medium')))
            conn.commit()
            task_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
            conn.close()
            self._send(201, {'id': task_id, 'title': body['title'],
                             'due_date': body.get('due_date', ''),
                             'priority': body.get('priority', 'medium'),
                             'status': 'pending'})
        else:
            self._send(404, {'error': 'Endpoint not found', 'code': 404})

    # do_GET, do_PUT, do_DELETE follow same patterns with validation and consistent errors

if __name__ == '__main__':
    init_db()
    print('Server running on http://localhost:8000')
    HTTPServer(('localhost', 8000), TaskHandler).serve_forever()
```

**What changed:** Added quality criteria checklist — validation, hashing with salt, token expiry, parameterised queries, correct status codes, no extra setup steps, consistent error format.
**What improved:** Passwords now use salt. Validation on empty title and missing fields added. Token expiry system included. All queries use parameterised statements (no injection risk). Status codes are consistent. Can run with `python server.py`.
**What still failed:** No test file. No .gitignore or project scaffold. No rate limiting. Token storage is in-memory (lost on restart). No guidance on how to split into multiple files later.
**What I'd try next:** Add examples of what good looks like — show me a response I should match, or reference an existing codebase.

---

## Honest "Didn't Help" Moment

In **Version 2** (adding audience), switching from Node.js to Flask was helpful, but the output still had plain-text passwords. The audience flag helped the *stack decision* but didn't improve *security awareness*. The audience layer alone wasn't enough — I needed constraints (V3) to force better practices. If I had stopped at V2 and assumed audience was the fix, I'd have shipped an API with plain-text passwords.

---

## Final Reusable Prompt

```markdown
Build a REST API for a personal task manager with these features:
- User signup and login
- Create, read, update, delete tasks
- Due dates and priority levels on each task
- Filter tasks by status (pending/done) and priority (low/medium/high)
- Mark tasks complete

Audience: A solo developer building their first backend. Knows Python basics. No prior API experience.

Constraints:
- Python 3.14+ standard library only (http.server, sqlite3, json, hashlib) — no third-party packages
- Single file that runs with `python server.py`
- No external setup or dependency install

Output format:
1. Full server code in one block
2. Response schema table (each endpoint: method, path, success response, error response)
3. Example curl commands for every endpoint
4. Consistent JSON error format: {"error": "<message>", "code": <http_status>}

Quality checklist (check before sending):
- Every input validated before use (empty strings, missing fields, wrong types return 400)
- Passwords hashed with a unique salt per user
- Auth tokens have an expiry (24h)
- All database queries use parameterised statements (no f-strings or concatenation)
- Status codes: 201 POST, 200 GET/PUT, 400 bad request, 401 auth, 404 not found, 500 server error
- Errors always use {"error": <str>, "code": <int>}
- A 404 on an unknown route, not a crash
```
