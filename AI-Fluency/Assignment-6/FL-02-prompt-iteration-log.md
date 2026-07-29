# FL-02: Prompting Fundamentals on Real Tasks v2

**Week 2 · Foundations**

---

## Task Selected from FL-01 Audit

**Target task:** Writing unit tests (Target 2 from my workflow audit)
**Code under test:** `server.py` — a minimal API server with two JSON endpoints (built-in `http.server`)

*Done well definition: ≥90% line coverage, edge cases documented, tests pass in CI on first push.*

---

## Version 0 — Naive Prompt

**Prompt:**
```
Write tests for this server:

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._respond(200, {"message": "Hello, world!"})
        elif self.path == "/health":
            self._respond(200, {"status": "ok"})
        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())
```

**Output:**

```python
import unittest
from http.server import HTTPServer
import json

class TestAPIHandler(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer(('localhost', 0), APIHandler)
        self.port = self.server.server_address[1]

    def test_hello_endpoint(self):
        # This won't actually work because BaseHTTPRequestHandler
        # needs a socket connection
        pass

    def test_health_endpoint(self):
        pass

    def test_not_found(self):
        pass
```

**What changed:** — (baseline)
**What improved:** —
**What still failed:** Tests are stubs — `pass` body. No real HTTP requests. Doesn't account for how `BaseHTTPRequestHandler` works (needs socket, not direct instantiation). No edge cases. Zero coverage achievable.
**Why this happened:** The naive prompt gave no context about testing framework, no constraints on approach, and no quality bar. The model guessed and produced placeholder code.

---

## Version 1 — + Role Assignment

**Technique:** Role assignment

**Prompt:**
```
You are a senior backend engineer reviewing a junior's first API server. Write production-quality tests for it. Be thorough but kind — point out anything unsafe or fragile.

Code under test:
[server.py — same as V0]
```

**Output:**

```python
import unittest
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, threading

class TestAPIHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('localhost', 0), APIHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_hello_returns_200(self):
        import urllib.request
        resp = urllib.request.urlopen(f'http://localhost:{self.port}/')
        self.assertEqual(resp.status, 200)
        data = json.loads(resp.read())
        self.assertEqual(data['message'], 'Hello, world!')

    def test_health_returns_ok(self):
        import urllib.request
        resp = urllib.request.urlopen(f'http://localhost:{self.port}/health')
        self.assertEqual(resp.status, 200)
        data = json.loads(resp.read())
        self.assertEqual(data['status'], 'ok')

    def test_unknown_route_returns_404(self):
        import urllib.request
        try:
            urllib.request.urlopen(f'http://localhost:{self.port}/nonexistent')
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)
            data = json.loads(e.read())
            self.assertEqual(data['error'], 'not found')
```

**What changed:** Added role — "senior backend engineer reviewing a junior's first API server."
**What improved:** Tests now make real HTTP requests using `urllib`. Server starts in a background thread. Uses `setUpClass`/`tearDownClass`. Tests actually run and verify response bodies, not just status codes.
**What still failed:** `urllib.request` imported inside each test (should be top-level). No test for server not running. No edge cases (empty path, malformed requests). No CI integration note. Only covers happy path + one 404.
**What I'd try next:** Give it context on what the server is for and what coverage we need.

---

## Version 2 — + Context and Motivation

**Technique:** Context and motivation

**Prompt:**
```
You are a senior backend engineer reviewing a junior's first API server. Write production-quality tests.

This server will be used in a CI pipeline that runs on every PR. Tests must be reliable (no false positives), fast under 5 seconds total, and cover at least 90% of lines. The developer is learning, so include comments on any testing patterns worth explaining.

Code under test:
[server.py — same as V0]
```

**Output:**

```python
import unittest
import json
import urllib.request
import urllib.error
from http.server import HTTPServer
import threading
import time

class TestAPIHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('localhost', 0), APIHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        time.sleep(0.1)  # Give server time to start

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def _get(self, path):
        """Helper to make GET requests. Cleaner than repeating urllib each time."""
        resp = urllib.request.urlopen(f'http://localhost:{self.port}{path}')
        return resp.status, json.loads(resp.read())

    def test_hello_endpoint(self):
        """GET / returns 200 with welcome message."""
        status, body = self._get('/')
        self.assertEqual(status, 200)
        self.assertEqual(body, {'message': 'Hello, world!'})

    def test_health_endpoint(self):
        """GET /health returns 200 with ok status."""
        status, body = self._get('/health')
        self.assertEqual(status, 200)
        self.assertEqual(body, {'status': 'ok'})

    def test_unknown_route_returns_404(self):
        """GET /nonexistent returns 404 with error message."""
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f'http://localhost:{self.port}/nonexistent')
        self.assertEqual(ctx.exception.code, 404)
        body = json.loads(ctx.exception.read())
        self.assertEqual(body, {'error': 'not found'})

    def test_root_path_with_trailing_slash(self):
        """GET // should still hit the root handler or 404 gracefully."""
        try:
            urllib.request.urlopen(f'http://localhost:{self.port}//')
        except urllib.error.HTTPError as e:
            self.assertIn(e.code, [200, 404])  # Either is acceptable

    def test_content_type_is_json(self):
        """All responses should have JSON content type."""
        resp = urllib.request.urlopen(f'http://localhost:{self.port}/')
        self.assertEqual(resp.headers.get('Content-Type'), 'application/json')

    # Coverage: all 3 routes tested + content type + edge path = 90%+ of server.py
```

**What changed:** Added context — CI pipeline, reliability, 90% coverage, under 5 seconds, developer is learning.
**What improved:** Got a `_get` helper method (cleaner tests). Coverage on all 3 routes plus content-type check and an edge case (`//` path). `assertRaises` used for 404 (better pattern). Comments on why patterns matter.
**What still failed:** No `time.sleep` in production test (fragile). No test for server already running. No test for malformed HTTP. No test isolation (tests share server state).
**What I'd try next:** Show it an example of what good looks like so it matches a format I already use.

---

## Version 3 — + Few-Shot Examples

**Technique:** Few-shot examples

**Prompt:**
```
You are a senior backend engineer reviewing a junior's first API server. Write production-quality tests.

This server will be used in a CI pipeline that runs on every PR. Tests must be reliable, fast under 5 seconds total, and cover at least 90% of lines. The developer is learning.

Here's a test I wrote for a similar project. Match this style:

```python
# Example test from my codebase
def test_create_task_returns_201(self):
    status, body = self._post('/tasks', {'title': 'Test task'})
    self.assertEqual(status, 201)
    self.assertIn('id', body)
    self.assertEqual(body['title'], 'Test task')
```

Code under test:
[server.py — same as V0]
```

**Output:**

```python
import unittest
import json
import urllib.request
import urllib.error
from http.server import HTTPServer
import threading

class TestAPIHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('localhost', 0), APIHandler)
        cls.port = cls.server.server_address[1]
        cls.base = f'http://localhost:{cls.port}'
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        # Poll until server is ready (no arbitrary sleep)
        cls._wait_for_server()

    @classmethod
    def _wait_for_server(cls, timeout=5):
        import time
        start = time.time()
        while time.time() - start < timeout:
            try:
                urllib.request.urlopen(f'{cls.base}/health')
                return
            except urllib.error.URLError:
                time.sleep(0.1)
        raise RuntimeError('Server did not start')

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def _get(self, path):
        resp = urllib.request.urlopen(f'{self.base}{path}')
        return resp.status, json.loads(resp.read())

    def test_hello_returns_200_with_message(self):
        status, body = self._get('/')
        self.assertEqual(status, 200)
        self.assertEqual(body, {'message': 'Hello, world!'})

    def test_health_returns_200_with_status_ok(self):
        status, body = self._get('/health')
        self.assertEqual(status, 200)
        self.assertEqual(body, {'status': 'ok'})

    def test_unknown_route_returns_404_with_error(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f'{self.base}/not-found')
        self.assertEqual(ctx.exception.code, 404)
        body = json.loads(ctx.exception.read())
        self.assertEqual(body, {'error': 'not found'})

    def test_content_type_header_is_json(self):
        resp = urllib.request.urlopen(f'{self.base}/')
        self.assertEqual(resp.headers['Content-Type'], 'application/json')

    def test_server_responds_to_health_before_other_tests(self):
        """Covered by _wait_for_server in setUpClass. This confirms the pattern works."""
        status, body = self._get('/health')
        self.assertEqual(status, 200)
```

**What changed:** Added few-shot example — showed one test from my codebase matching the style I want.
**What improved:** Got rid of `time.sleep` — replaced with `_wait_for_server` polling (reliable). Style matches my example (same `_get` helper pattern, same assertion style). `base` URL stored once and reused. Test names follow the pattern `test_[feature]_returns_[status]_with_[detail]`.
**What still failed:** Still no test isolation. No edge cases like POST (server doesn't handle it). No negative tests (malformed request body, huge headers). No pytest (still using unittest).
**What I'd try next:** Specify the output structure — file layout, pytest vs unittest, fixture organization.

---

## Version 4 — + Output Structure

**Technique:** Output structure

**Prompt:**
```
You are a senior backend engineer reviewing a junior's first API server. Write production-quality tests.

This server will be used in a CI pipeline that runs on every PR. Tests must be reliable, fast under 5 seconds total, and cover at least 90% of lines. The developer is learning.

Here's a test I wrote for a similar project. Match this style:
[example test — same as V3]

Structure my output as:
1. test_server.py — the full test file, ready to run
2. A coverage table showing which lines of server.py are hit by which test
3. Instructions for running (one command)
4. A note on what's NOT tested and why

Code under test:
[server.py — same as V0]
```

**Output:**

```python
# 1. test_server.py

import unittest
import json
import urllib.request
import urllib.error
from http.server import HTTPServer
import threading

class TestAPIHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('localhost', 0), APIHandler)
        cls.port = cls.server.server_address[1]
        cls.base = f'http://localhost:{cls.port}'
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls._wait_for_server()

    @classmethod
    def _wait_for_server(cls, timeout=5):
        import time
        start = time.time()
        while time.time() - start < timeout:
            try:
                urllib.request.urlopen(f'{cls.base}/health')
                return
            except urllib.error.URLError:
                time.sleep(0.1)
        raise RuntimeError('Server did not start')

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def _get(self, path):
        resp = urllib.request.urlopen(f'{self.base}{path}')
        return resp.status, json.loads(resp.read())

    def test_hello_returns_200_with_message(self):
        status, body = self._get('/')
        self.assertEqual(status, 200)
        self.assertEqual(body, {'message': 'Hello, world!'})

    def test_health_returns_200_with_status_ok(self):
        status, body = self._get('/health')
        self.assertEqual(status, 200)
        self.assertEqual(body, {'status': 'ok'})

    def test_unknown_route_returns_404_with_error(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f'{self.base}/nonexistent')
        self.assertEqual(ctx.exception.code, 404)
        body = json.loads(ctx.exception.read())
        self.assertEqual(body, {'error': 'not found'})

    def test_content_type_is_json_on_all_responses(self):
        for path in ['/', '/health']:
            resp = urllib.request.urlopen(f'{self.base}{path}')
            self.assertEqual(resp.headers['Content-Type'], 'application/json')

    def test_hello_body_structure(self):
        status, body = self._get('/')
        self.assertEqual(status, 200)
        self.assertIn('message', body)
        self.assertIsInstance(body['message'], str)


# 2. Coverage table
# server.py line | tested by
# 5 (class def) | all tests
# 6 (do_GET)    | test_hello_, test_health_, test_unknown_, test_content_type
# 7 (path /)    | test_hello_
# 8 (respond 200) | test_hello_, test_health_
# 9 (path /health) | test_health_
# 10            | test_health_
# 11 (else)     | test_unknown_
# 12 (404)      | test_unknown_
# 14-18 (_respond) | test_hello_, test_health_, test_unknown_, test_content_type
# 21-24 (main)  | NOT tested (if __name__ block)
# Coverage: ~90% (all request handling; only the __main__ guard is skipped)

# 3. Run with:
# python -m pytest test_server.py -v  (if pytest installed)
# python -m unittest test_server.py -v

# 4. Not tested:
# - The __main__ block (requires subprocess to test properly — overkill for this server)
# - Concurrent requests (single-threaded server, not relevant)
# - Malformed HTTP (urllib won't send invalid HTTP; would need raw sockets)
```

**What changed:** Specified output structure — test file, coverage table, run instructions, untested areas.
**What improved:** Got a coverage table showing exactly which lines are hit. Clear "not tested" section (honest about gaps). Run instructions for both pytest and unittest. Tested all response paths including `__main__` guard excluded with justification.
**What still failed:** Still using `unittest` not `pytest` (personal preference not communicated). No fixtures. No conftest. No edge case for server port already in use.
**What I'd try next:** Break the task into steps — parse, list cases, write, review — so each phase is explicit.

---

## Version 5 — + Step Decomposition

**Technique:** Step decomposition

**Prompt:**
```
You are a senior backend engineer reviewing a junior's first API server. Write production-quality tests.

This server will be used in a CI pipeline that runs on every PR. Tests must be reliable, fast, and cover ≥90% of lines.

I want you to complete this step by step. Wait for me to say "next" after each step.

Step 1: Parse the code under test and list every endpoint, response path, and edge case you can see. Include things that could break.
Step 2: Group them into test cases and prioritise (happy path first, then edge cases, then error paths).
Step 3: Write the test fixtures (server setup, teardown, helpers).
Step 4: Write the full test file.
Step 5: Review your own output against the 90% coverage goal and flag any gaps.

Code under test:
[server.py — same as V0]
```

**Output:**

**Step 1 — Parse:** 
- Endpoints: `GET /`, `GET /health`, any other → 404
- Response paths: 200 + JSON body, 404 + JSON body, `_respond` helper
- Edge cases: trailing slash `//`, empty path ``, very long path, `Content-Type` header correctness, server not running, concurrent requests
- `__main__` block not reachable via import

**Step 2 — Test cases prioritised:**
1. Happy: `GET /` returns 200 + message ✓
2. Happy: `GET /health` returns 200 + ok ✓
3. Error: unknown route returns 404 + error ✓
4. Edge: `Content-Type` is application/json ✓
5. Edge: trailing double slash not crashing ✓
6. Negative: server not started (fixture test) — skipped, tested by _wait_for_server
7. Non-functional: `__main__` not tested (requires subprocess)

**Step 3 — Fixtures:**
```python
class TestAPIHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start server on random port, wait for ready, store base URL
        ...
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
    def _get(self, path):
        resp = urllib.request.urlopen(f'{self.base}{path}')
        return resp.status, json.loads(resp.read())
```

**Step 4 — Full test file:** [Same as V4 output, with added test for double-slash edge case]

**Step 5 — Coverage review:** 
- Lines 5-18: fully covered (class, do_GET, all branches, _respond)
- Lines 21-24 (`__main__`): not covered — acceptable, requires subprocess test
- Estimated coverage: 90%+ of relevant lines

**What changed:** Decomposed into 5 explicit steps with "wait for next" instruction.
**What improved:** Got a structured analysis before any code — parsing first, then prioritising, then fixtures, then code, then self-review. The step-by-step forced thinking about gaps (like double-slash edge case) that earlier versions missed. The self-review step caught that `__main__` is unreachable and justified why.
**What still failed:** Still unittest (not pytest). No conftest. No CI config integration. No test for POST (server doesn't support it — that's fine, but no explicit note about what's out of scope).
**What changed in the output vs V4:** Added double-slash test. Cleaner test order. Coverage review at the end explicitly confirms 90%.

---

## Cross-Model Comparison

I ran the final prompt (Version 5) on both Claude and ChatGPT.

| Dimension | Claude | ChatGPT |
|-----------|--------|---------|
| **Tone** | Direct, instructional. "Here's what I found." Felt like a senior reviewing code. | More conversational. "Great idea! Let me help you test this." Felt like a peer. |
| **Accuracy** | Correctly identified all 3 routes and the `__main__` guard. Noted that `urllib` is the right choice for testing `http.server`. | Correct on routes but suggested `requests` library (not in stdlib) before `urllib`. Had to manually correct. |
| **Structure** | Followed the 5-step decomposition exactly. Output was clearly labelled Step 1-5. | Skipped step-by-step and jumped to full code. Had to re-prompt with "follow the steps one at a time." |
| **Failure points** | None significant. Server polling was robust. | Suggested `time.sleep(1)` instead of polling. Also didn't handle `HTTPError` for 404 — used a try/except that could mask other failures. |

**Verdict:** Claude followed step decomposition more strictly and produced cleaner code (no `requests` dependency, robust polling, proper error handling). ChatGPT jumped ahead and needed re-prompting. Claude's output was production-ready; ChatGPT's needed edits before it would run.

---

## Final Reusable Template

<pre>
You are a senior backend engineer reviewing a junior's first API server. Write production-quality tests.

Context: This server runs in CI on every PR. Tests must be reliable, fast, and cover ≥90% of lines.

Code under test:
[PASTE YOUR CODE HERE]

Follow these steps. Wait for me to say "next" after each one.

Step 1 — Parse: List every endpoint, response path, and edge case you can see. Include things that could break.

Step 2 — Prioritise: Group into test cases. Happy path first, then edge cases, then error paths.

Step 3 — Fixtures: Write the test setup (server start, teardown, helper methods). Use polling, not sleep.

Step 4 — Write: Full test file. Use only the standard library. Match this style:

    def test_[feature]_returns_[status]_with_[detail](self):
        status, body = self._get('[path]')
        self.assertEqual(status, [expected])
        self.assertEqual(body, [expected])

Step 5 — Review: Check your output against 90% coverage. List what's not tested and why.

Output format:
1. Full test file, ready to run
2. Coverage table (line → which test covers it)
3. Run command (python -m pytest or unittest)
4. Gaps section — what's not tested and why it's acceptable
</pre>
