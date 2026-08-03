from fastapi import HTTPException

from .models import Task, TaskCreate, TaskUpdate
from .repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def list_tasks(self) -> list[Task]:
        return self._repository.list()

    def get_task(self, task_id: int) -> Task:
        task = self._repository.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def create_task(self, payload: TaskCreate) -> Task:
        title = (payload.title or "").strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
        return self._repository.create(title=title, done=payload.done)

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task:
        title = (payload.title or "").strip()
        if not title or payload.done is None:
            raise HTTPException(
                status_code=400,
                detail="Title and done are required",
            )
        task = self._repository.update(
            task_id=task_id,
            title=title,
            done=payload.done,
        )
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def delete_task(self, task_id: int) -> None:
        if not self._repository.delete(task_id):
            raise HTTPException(status_code=404, detail="Task not found")

    def database_is_healthy(self) -> bool:
        return self._repository.ping()
