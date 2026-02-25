import json
import os
from models import Task

DEFAULT_FILE = "tasks.json"


def load_tasks(filepath: str = DEFAULT_FILE) -> list[Task]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(item) for item in data]


def save_tasks(tasks: list[Task], filepath: str = DEFAULT_FILE) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)


def get_next_id(tasks: list[Task]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1


def find_task_by_id(tasks: list[Task], task_id: int) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            return task
    return None
