# FL-04: Framed Case Studies

**Week 2 · Frame Your Work**

---

## Voice Card

> Direct, plain, no buzzwords, warm.

I added this to my Claude Project as a standing instruction so every draft stays in my voice.

---

## Case 1: Minimal API Server — Two Endpoints, Zero Dependencies

### The problem

I needed to build a working API server for my first backend assignment. The catch: no external packages allowed — standard library only. Beginners overthink this, spend hours on Flask setup and config. I wanted to prove I could ship something functional in minutes.

### What I did

I wrote a single-file Python server using only `http.server` and `json` from the standard library. Two endpoints:

- `GET /` returns a welcome message
- `GET /health` returns `{"status": "ok"}`
- Everything else returns a 404 with an error message

I decided against using a framework because the assignment didn't need one. A framework adds dependencies, startup time, and learning curve. For a two-endpoint server, built-in tools were faster and cleaner.

### What came of it

The server ran on `localhost:8000`, responded to curl and browser requests, and passed every check. Total code: 25 lines. Total time from start to first working response: under 10 minutes.

Next time I'd add request logging and a configurable port. But for the brief — smallest possible backend — it did exactly what it needed to.

---

## Case 2: Production-Ready API Patterns — Security-First Design

### The problem

Our internship moved from "make it work" to "make it right." The next assignment asked for a well-structured backend with input validation, proper status codes, and security considerations. I wanted a repeatable pattern I could use for every endpoint going forward.

### What I did

I designed a request handler that validates inputs before processing, returns consistent JSON error responses, and separates routing logic from response formatting. Security decisions built in from the start:

- All inputs sanitised before reaching business logic
- Status codes follow HTTP conventions (200 for success, 400 for bad request, 401 for auth, 500 for server error)
- CORS headers set explicitly, not left as defaults
- No secrets in code — configuration separated from logic

I chose Python's built-in `http.server` because it forced me to understand how HTTP works at the protocol level instead of hiding it behind a framework's abstraction. That decision cost a bit more handwritten code but built a stronger mental model.

### What came of it

I now have a template I can reuse for any new endpoint. The security patterns — validate, respond consistently, handle errors — are baked in at the handler level instead of bolted on later. The total project lives on GitHub with a README, .gitignore, and clean commit history.

Next thing: add automated tests that verify the security behaviours, not just the happy path.

---

## Bio & Contact

### Bio

I build secure, production-ready APIs with Python. I'm a backend engineering intern focused on making sure the things I ship are safe by default, not as an afterthought.

### Contact / CTA

See something that looks like your stack? [Download my CV](mailto:your-email@example.com) or send a message. Happy to talk APIs, security, or what I'm building next.

---

## Before / After: Generic AI vs Edited

### Before (generic AI line)

> "I'm a passionate and results-driven backend developer dedicated to leveraging cutting-edge technologies to deliver innovative solutions that drive measurable impact and exceed stakeholder expectations."

### After (my version, post-edit)

> I build secure, production-ready APIs with Python. I'm a backend engineering intern focused on making sure the things I ship are safe by default, not as an afterthought.

**What I cut:** "passionate," "results-driven," "cutting-edge," "leveraging," "innovative solutions," "measurable impact," "stakeholder expectations" — seven buzzwords that say nothing specific.

**What stayed:** a concrete claim (I build APIs), an audience signal (backend intern), and a specific stance (safe by default). A real person could say this out loud.
