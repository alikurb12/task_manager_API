from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.shemas.project import ProjectCreate, ProjectUpdate

async def get_projects(
        db : AsyncSession,
        owner_id : int,
) -> list[Project]:
    result = await db.execute(select(Project).where(Project.owner_id == owner_id))
    return result.scalars().all()

async def get_project(
        db : AsyncSession,
        project_id : int,
        owner_id : int,
) -> Project | None:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.owner_id == owner_id)
    )
    return result.scalar_one_or_none()

async def create_project(
        db : AsyncSession,
        data : ProjectCreate,
        owner_id : int,
) -> Project:
    project = Project(**data.model_dump(), owner_id=owner_id)
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project

async def update_project(
        db : AsyncSession,
        project : Project,
        data : ProjectUpdate,
) -> Project:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    await db.flush()
    await db.refresh(project)
    return project

async def delete_project(db: AsyncSession, project: Project) -> None:
    await db.delete(project)