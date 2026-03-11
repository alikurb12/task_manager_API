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

async def create_task(db: AsyncSession, task_data: dict, project_id: int):
    task_data["project_id"] = project_id
    task = Task(**task_data)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def update_task(db: AsyncSession, task: Task, update_data: dict):
    for field, value in update_data.items():
        setattr(task, field, value)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db : AsyncSession, task : Task) -> None:
    await db.delete(task)