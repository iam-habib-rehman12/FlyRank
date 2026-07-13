# Minimal API Server

A minimal Python API server with two JSON endpoints built using only the standard library (no external dependencies).

## Endpoints

| Method | Path       | Response                        |
|--------|------------|---------------------------------|
| GET    | `/`        | `{"message": "Hello, world!"}` |
| GET    | `/health`  | `{"status": "ok"}`             |
| GET    | any other  | `{"error": "not found"}` (404) |

## Usage

```bash
python server.py
```

Server runs on `http://localhost:8000`.

Test with curl:

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```
