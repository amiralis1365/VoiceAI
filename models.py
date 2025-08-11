from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TaskType(Enum):
    PLUMBER = "plumber"
    FEEDBACK = "feedback"
    ABOUT_US = "about_us"
    PROCUREMENT = "procurement"
    SYSTEM_ADMIN = "system_admin"

@dataclass
class MySessionInfo:
    task: TaskType | None = None
    name: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None
    problem: str | None = None
    appointment_time: datetime | None = None
    feedback: str | None = None
    question: str | None = None
