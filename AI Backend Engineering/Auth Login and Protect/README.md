# Auth - Login & Protect

A secure FastAPI backend that uses Supabase Auth for account creation, login, logout, JWT verification, and reusable protection of private endpoints.

## What this project demonstrates

- Supabase as the Identity Provider
- Sign-up and password login
- Access and refresh token responses
- Strict `Authorization: Bearer <token>` parsing
- Server-side access-token verification with `supabase.auth.get_user(token)`
- Reusable FastAPI authentication dependency
- Public and protected endpoints
- JSON error responses with the required HTTP status codes
- Swagger UI bearer authorization
- Secret-safe environment configuration
- Automated API tests with a mocked Supabase client

## Authentication flow

1. A client signs up or logs in with email and password.
2. Supabase validates the credentials and returns a signed access token.
3. The client sends the token to this API in the Authorization header.
4. The reusable `get_current_user` dependency asks Supabase to verify the token.
5. Valid requests reach the protected route; missing, malformed, expired, or altered tokens receive `401`.

## Project structure

```text
Auth Login and Protect/
|-- app/
|   |-- __init__.py
|   |-- config.py
|   |-- main.py
|   |-- schemas.py
|   |-- security.py
|   `-- supabase_client.py
|-- tests/
|   `-- test_api.py
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Setup

### 1. Create a Supabase project

Create a free project at [Supabase](https://supabase.com/). From the project dashboard, copy:

- Project URL
- Anon/public key

Do not use the `service_role` key. For simple local testing, either confirm the sign-up email or temporarily disable email confirmation in the Supabase Auth settings.

### 2. Clone and enter the assignment

```bash
git clone https://github.com/iam-habib-rehman12/FlyRank.git
cd "FlyRank/AI Backend Engineering/Auth Login and Protect"
```

### 3. Create a virtual environment and install dependencies

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and replace the placeholders:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
PORT=8000
```

The real `.env` is ignored by Git and must never be committed.

### 5. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

Open:

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## API reference

| Method | Endpoint | Authentication | Success |
|---|---|---|---:|
| `POST` | `/auth/signup` | Public | `201` |
| `POST` | `/auth/login` | Public | `200` |
| `POST` | `/auth/logout` | Bearer JWT | `204` |
| `GET` | `/public/info` | Public | `200` |
| `GET` | `/protected/profile` | Bearer JWT | `200` |
| `GET` | `/protected/dashboard` | Bearer JWT | `200` |
| `GET` | `/health` | Public | `200` |

Required error behavior:

| Situation | Status | JSON response |
|---|---:|---|
| Missing email or password | `400` | `{"error": "Email and password are required"}` |
| Incorrect login | `401` | `{"error": "Invalid login credentials"}` |
| Missing/malformed bearer token | `401` | `{"error": "Access token required"}` |
| Invalid/expired bearer token | `401` | `{"error": "Invalid or expired token"}` |

## Test the complete flow

### Sign up

```bash
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Expected: `201 Created`.

### Log in

```bash
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Expected: `200 OK` with `access_token` and `refresh_token`. Copy the access token.

### Call the protected profile

```bash
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer PASTE_ACCESS_TOKEN_HERE"
```

Expected: `200 OK` with safe user metadata.

Change one character in the token and repeat. Expected: `401 Unauthorized`.

### Log out

```bash
curl -i -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer PASTE_ACCESS_TOKEN_HERE"
```

Expected: `204 No Content`.

## Swagger UI

Run the server and visit http://localhost:8000/docs.

1. Expand `POST /auth/login` and log in.
2. Copy the returned access token.
3. Click **Authorize**.
4. Enter the token in the bearer authorization dialog.
5. Run `GET /protected/profile` with **Try it out**.
6. Confirm protected routes show lock icons and the valid call returns `200`.

FastAPI generates the OpenAPI bearer security scheme from `HTTPBearer`, so protected endpoints are visibly locked in Swagger.

## Automated tests

The tests replace the real Supabase client with a deterministic fake. This verifies routing, response bodies, status codes, token rejection, valid authentication, and reuse of the authentication dependency without using real credentials.

```bash
pytest -q
```

Test cases cover:

- public access;
- successful signup;
- missing login input;
- successful login and token response;
- invalid credentials;
- missing token;
- tampered token;
- valid protected profile;
- a second route protected by the same dependency.

## Security decisions

- Passwords are sent to Supabase Auth and never stored by this API.
- Access tokens are verified through Supabase before protected logic runs.
- The bearer prefix is checked strictly.
- Only safe user fields (`id`, `email`, `created_at`) are returned.
- The Supabase anon key is loaded from environment variables.
- `.env` is ignored while `.env.example` documents required keys.
- No access tokens or credentials are logged.
- Logout calls Supabase's Auth logout endpoint using the caller's access token.
- `401` is used when the caller is unknown; `403` would be used when an authenticated user lacks permission.

## Assignment checklist

- [x] Single documented server command
- [x] Supabase environment configuration
- [x] `.env` ignored and `.env.example` committed
- [x] Signup and login routes
- [x] Access and refresh tokens returned by login
- [x] Public information route
- [x] Protected profile route
- [x] Reusable bearer-token verification dependency
- [x] Second protected route demonstrating reuse
- [x] Logout route
- [x] Required success and error status codes
- [x] Swagger bearer authorization configuration
- [x] Automated tests
- [x] Public GitHub repository with incremental commits

## Assignment source

FlyRank Backend AI Engineering - BE-03 - Auth: Login & Protect.
