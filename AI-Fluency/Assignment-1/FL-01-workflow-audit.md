# Workflow Audit — Habib Rehman

Backend AI Engineering Intern · July 2026

## Accounts & Tools

| Tool         | Account Status       |
|-------------|----------------------|
| Claude       | ✅ Account created (anthropic.com) |
| ChatGPT      | ✅ Account created (chat.openai.com) |
| Anthropic Academy | ✅ Enrolled — *AI Fluency: Framework & Foundations* (Module 1 completed) |

## Workflow Audit: Recurring Tasks

| # | Task | Classification | Rationale |
|---|------|---------------|-----------|
| 1 | Debugging API route errors | **Collaborate with AI** | AI spots edge cases I miss (e.g., type mismatches, status codes); I verify the fix in Postman. |
| 2 | Writing unit tests | **Delegate to AI with review** | AI generates test scaffolds from function signatures; I adjust edge coverage. |
| 3 | Code review (team PRs) | **Just me** | Requires understanding team context, business logic, and unwritten conventions — AI can't read between the lines. |
| 4 | Database schema design | **Collaborate with AI** | I define entities and relationships; AI suggests indexing, cascade rules, and migration patterns for review. |
| 5 | Writing documentation (READMEs, API docs) | **Delegate to AI with review** | AI drafts structure and wording from code; I correct tone and technical accuracy. |
| 6 | Refactoring legacy code | **Collaborate with AI** | AI identifies duplication and suggests extraction; I decide whether the refactor aligns with roadmap. |
| 7 | Learning a new library/framework | **Just me** | Reading docs and building mental models is personal — AI summaries skip nuance I need. |
| 8 | Setting up CI/CD config | **Delegate to AI with review** | AI writes YAML from requirements; I test the pipeline end-to-end. |
| 9 | Writing PR descriptions & commit messages | **Fully automate** | Standard format enforced by git hooks and commitlint — zero human value to do by hand. |
| 10 | Code formatting & linting | **Fully automate** | Prettier, Ruff, and pre-commit hooks — no reason to spend brain cycles. |
| 11 | Investigating production errors (logs, traces) | **Collaborate with AI** | AI parses stack traces and correlates logs; I understand the user-facing impact and prioritise the fix. |
| 12 | Designing API request/response schemas | **Collaborate with AI** | I draft the endpoint semantics; AI generates OpenAPI spec snippets for review. |
| 13 | Pair programming on complex features | **Just me** | Real-time human collaboration builds shared understanding — AI can't replace synchronous discussion. |
| 14 | Writing shell scripts (automation, data tasks) | **Delegate to AI with review** | AI drafts the script; I test edge cases like missing files, permission errors, and platform differences. |
| 15 | Performance benchmarking & profiling | **Collaborate with AI** | I run the profiler; AI helps interpret flame graphs and suggests optimisation candidates. |

## Three Target Tasks for FL-02 through FL-04

Selected for their recurring nature, measurable output, and room to define "done well":

### Target 1: Debugging API route errors → *Done well*

| Aspect | Definition |
|--------|-----------|
| Task | Diagnose and fix a broken API endpoint (wrong status code, response shape, or DB query). |
| Done well | ① Root cause identified in <30 min (with AI collaboration) ② Fix covered by an existing or new unit test ③ Response matches the OpenAPI spec ④ PR merged with no re-opened bugs on that endpoint in the next sprint. |

### Target 2: Writing unit tests → *Done well*

| Aspect | Definition |
|--------|-----------|
| Task | Write tests for a new or modified backend module (routes, services, models). |
| Done well | ① ≥90% line coverage on the module ② All edge cases documented in test names (empty input, auth failure, DB timeout) ③ Tests pass in CI on first push ④ Reviewers request zero or one minor change. |

### Target 3: Designing API request/response schemas → *Done well*

| Aspect | Definition |
|--------|-----------|
| Task | Define the contract (method, path, request body, response body, error codes) for a new endpoint. |
| Done well | ① Schema is documented in OpenAPI 3.0 before any implementation starts ② Status codes cover success (200/201), client error (400/401/404), and server error (500) ③ Frontend/dev-consumer confirms the contract is clear and sufficient ④ Zero breaking changes during implementation sprint. |

---

## Claude Project Setup

### Project name
Backend AI Engineering — Workflow Audit

### Custom instructions (Project knowledge)

I created a Claude Project called **"Backend AI Engineering — Workflow Audit"** and set these custom instructions:

```
# Who you are helping
Backend AI Engineering intern learning API development, databases, and deployment.

# Tone
Direct and concise. Short paragraphs. Bullet points for lists. No fluff, no introductions, no summaries unless asked. Get straight to the answer.

# Tech stack
- Language: Python 3.14
- Frameworks: FastAPI (preferred) or Flask
- Database: PostgreSQL
- Other: Docker, Git, pytest

# When suggesting code
- Prefer Python standard library first, then widely adopted packages (FastAPI, SQLAlchemy, Pydantic). Avoid obscure or niche libraries.
- Show complete, runnable code snippets — not pseudo-code.
- Follow PEP 8 (Black formatting, ruff linting).
- Always include type hints.

# Testing
- Generate full pytest test files with edge cases (empty input, auth failure, DB timeout, malformed payloads).
- Aim for ≥90% line coverage.
- Use pytest fixtures for test setup.

# Security
Flag security concerns immediately — SQL injection, input validation, auth bypass, hardcoded secrets, unsafe deserialization. Do not wait to be asked.

# Code review
When reviewing my code, point out missing edge cases and error handling before style or naming issues.

# Current goals
1. Improve API test coverage to ≥90%.
2. Reduce endpoint debugging time to under 30 min.
3. Write OpenAPI specs before starting implementation.
4. Build a deploy-ready backend with CI/CD.

# What NOT to do
- Do not add comments to code unless the logic is genuinely non-obvious.
- Do not suggest JavaScript or frontend solutions unless I ask.
- Do not generate placeholder or "TODO" code — either write it properly or say you can't.
- Do not ask "would you like me to explain this?" — just do it.
```

### Evidence
Claude Project with custom instructions
<img width="959" height="539" alt="Screenshot 2026-07-13 173251" src="https://github.com/user-attachments/assets/26e38a76-1315-487a-bb24-0e18d6ea0c96" />
Claude account
<img width="958" height="539" alt="Screenshot 2026-07-13 173309" src="https://github.com/user-attachments/assets/392c161d-ddcf-41e2-9d6e-c04374644514" />
Chatgpt account
<img width="959" height="539" alt="Screenshot 2026-07-13 173325" src="https://github.com/user-attachments/assets/d30b0e14-69df-42a6-aece-695e1b0115f4" />
AI Fluency: Framework & Foundations(Completed)
https://verify.skilljar.com/c/jvoc8egsjcwh
<img width="607" height="401" alt="image" src="https://github.com/user-attachments/assets/b15b00d1-6745-4b4f-ad07-c7fd50d6dfb5" />
<img width="958" height="449" alt="image" src="https://github.com/user-attachments/assets/0261efdc-94b0-4f25-ab33-1ec85fe6d6ee" />







