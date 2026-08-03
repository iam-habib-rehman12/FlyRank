from app.models import Task, TaskCreate, TaskUpdate
from app.service import TaskService


class InMemoryTaskRepository:
    def __init__(self):
        self.tasks = {
            1: Task(id=1, title="Existing task", done=False),
        }
        self.next_id = 2

    def list(self):
        return list(self.tasks.values())

    def get(self, task_id):
        return self.tasks.get(task_id)

    def create(self, title, done=False):
        task = Task(id=self.next_id, title=title, done=done)
        self.tasks[task.id] = task
        self.next_id += 1
        return task

    def update(self, task_id, title, done):
        if task_id not in self.tasks:
            return None
        task = Task(id=task_id, title=title, done=done)
        self.tasks[task_id] = task
        return task

    def delete(self, task_id):
        return self.tasks.pop(task_id, None) is not None

    def ping(self):
        return True

    def close(self):
        pass


def test_crud_contract_is_storage_independent():
    service = TaskService(InMemoryTaskRepository())

    created = service.create_task(TaskCreate(title="Containerize stack"))
    assert created.id == 2
    assert created.done is False

    fetched = service.get_task(created.id)
    assert fetched.title == "Containerize stack"

    updated = service.update_task(
        created.id,
        TaskUpdate(title="Containerize stack", done=True),
    )
    assert updated.done is True

    service.delete_task(created.id)
    assert [task.id for task in service.list_tasks()] == [1]


def test_database_health_contract():
    service = TaskService(InMemoryTaskRepository())
    assert service.database_is_healthy() is True
