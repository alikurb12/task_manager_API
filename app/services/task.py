from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.shemas.task import TaskCreate, TaskUpdate

async def get_tasks(
        db : AsyncSession,
        project_id : int,
) -> list[Task]:
    result = await db.execute(select(Task).where(Task.project_id == project_id))
    return result.scalars().all()

async def get_task(
        db : AsyncSession,
        task_id : int,
        project_id : int,
) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.project_id == project_id)
    )

    return result.scalar_one_or_none()

async def create_task(
        db : AsyncSession,
        data : TaskCreate,
        project_id : int,
) -> Task:
    task = Task(**data.model_dump(), project_id=project_id)
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return task

async def update_task(
        db : AsyncSession,
        task : Task,
        data : TaskUpdate,
) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    
    await db.flush()
    await db.refresh(task)
    return task

async def delete_task(db : AsyncSession, task : Task) -> None:
    await db.delete(task)