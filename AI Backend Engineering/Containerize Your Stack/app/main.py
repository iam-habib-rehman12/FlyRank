from contextlib import asynccontextmanager
from os import getenv
from typing import Iterator

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .models import Task, TaskCreate, TaskUpdate
from .postgres_repository import PostgresTaskRepository
from .service import TaskService

_service: TaskService | None = None
_repository: PostgresTaskRepository | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI) -> Iterator[None]:
    global _service, _repository
    database_url = getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required")
    _repository = PostgresTaskRepository(database_url)
    _service = TaskService(_repository)
    yield
    _repository.close()


app = FastAPI(
    title="Containerized Task API",
    version="1.0.0",
    description="Storage-independent CRUD API backed by PostgreSQL.",
    lifespan=lifespan,
)


@app.exception_handler(HTTPException)
async def http_error_handler(_request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _request, _exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid request body"},
    )


def get_task_service() -> TaskService:
    if _service is None:
        raise HTTPException(status_code=503, detail="Service unavailable")
    return _service


@app.get("/health", tags=["System"])
def health(service: TaskService = Depends(get_task_service)):
    if not service.database_is_healthy():
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"status": "ok", "database": "ok"}


@app.get("/tasks", response_model=list[Task], tags=["Tasks"])
def list_tasks(service: TaskService = Depends(get_task_service)):
    return service.list_tasks()


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    return service.get_task(task_id)


@app.post("/tasks", response_model=Task, status_code=201, tags=["Tasks"])
def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return service.create_task(payload)


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    return service.update_task(task_id, payload)


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> Response:
    service.delete_task(task_id)
    return Response(status_code=204)
