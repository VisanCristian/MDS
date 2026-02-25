from dataclasses import dataclass, field
from datetime import datetime

DATE_FORMAT = "%d-%m-%Y %H:%M"
PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    description: str
    deadline: str
    start_time: str
    end_time: str
    priority: str
    done: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "priority": self.priority,
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            deadline=data["deadline"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            priority=data["priority"],
            done=data.get("done", False),
        )

    def __str__(self) -> str:
        status = "[x]" if self.done else "[ ]"
        prio = self.priority.upper()
        return (
            f"  {status} #{self.id} | {self.title} [{prio}]\n"
            f"      Descriere:  {self.description}\n"
            f"      Deadline:   {self.deadline}\n"
            f"      Programat:  {self.start_time} -> {self.end_time}\n"
        )


# Validari
def validate_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Format invalid. Foloseste: DD-MM-YYYY HH:MM (ex: 25-02-2026 14:30)")


def validate_future_date(date_str: str) -> datetime:
    dt = validate_date(date_str)
    if dt <= datetime.now():
        raise ValueError("Data trebuie sa fie in viitor.")
    return dt


def validate_priority(priority: str) -> str:
    p = priority.strip().lower()
    if p not in PRIORITIES:
        raise ValueError(f"Prioritate invalida. Alege din: {', '.join(PRIORITIES)}")
    return p


def validate_time_interval(start_str: str, end_str: str) -> tuple[datetime, datetime]:
    start = validate_date(start_str)
    end = validate_date(end_str)
    if end <= start:
        raise ValueError("Ora de sfarsit trebuie sa fie dupa ora de inceput.")
    return start, end
