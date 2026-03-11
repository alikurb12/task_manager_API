from datetime import datetime
from pydantic import BaseModel
from app.models.task import TaskPriority, TaskStatus

class TaskCreate(BaseModel):
    title : str
    description : str | None = None
    status : TaskStatus = TaskStatus.todo
    priority : TaskPriority = TaskPriority.medium
    due_date : datetime | None = None
    assignee_id : int | None = None

class TaskUpdate(BaseModel):
    title : str | None = None
    description : str | None = None
    status : TaskStatus | None = None
    priority : TaskPriority | None = None
    due_date : datetime | None = None
    assignee_id : int | None = None

class TaskRead(BaseModel):
    id : int
    title : str
    description : str | None
    status : TaskStatus
    priority : TaskPriority
    due_date : datetime | None
    creater_at : datetime
    project_id : int
    assignee_id : int | None

    model_config = {"from_attributes" : True}