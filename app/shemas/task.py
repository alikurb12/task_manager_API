from datetime import datetime
from pydantic import BaseModel, field_validator
from app.models.task import TaskPriority, TaskStatus


def strip_timezone(v):
    if isinstance(v, datetime) and v.tzinfo is not None:
        return v.replace(tzinfo=None)
    return v


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: datetime | None = None
    assignee_id: int | None = None

    @field_validator("due_date", mode="before")
    @classmethod
    def remove_timezone(cls, v):
        return strip_timezone(v)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None

    @field_validator("due_date", mode="before")
    @classmethod
    def remove_timezone(cls, v):
        return strip_timezone(v)


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    created_at: datetime
    project_id: int
    assignee_id: int | None

    model_config = {"from_attributes": True}