from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.shemas.task import TaskCreate, TaskUpdate, TaskRead
from app.services import project as project_service
from app.services import task as task_service

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])

async def get_project_or_404(
        project_id : int,
        db : AsyncSession,
        user_id : int,
):
    project = await project_service.get_project(db, project_id, user_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.get("/", response_model=list[TaskRead])
async def list_tasks(
    project_id : int,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    await get_project_or_404(project_id, db, current_user.id)
    return await task_service.get_tasks(db, project_id)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id : int,
    data : TaskCreate,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):
    await get_project_or_404(project_id, db, current_user.id)
    task_data = data.model_dump()
    task_data["assignee_id"] = current_user.id
    return await task_service.create_task(db, task_data, project_id)

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    project_id : int,
    task_id : int,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):
    await get_project_or_404(project_id, db, current_user.id)
    task = await task_service.get_task(db, task_id, project_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    project_id : int,
    task_id : int,
    data : TaskUpdate,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):
    await get_project_or_404(project_id, db, current_user.id)
    task = await task_service.get_task(db, task_id, project_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Task not found")
    update_data = data.model_dump(exclude_unset=True)
    update_data.pop('assignee_id', None)
    
    return await task_service.update_task(db, task, update_data)

@router.delete("/{delete_task}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    project_id : int,
    task_id : int,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):
    await get_project_or_404(project_id, db, current_user.id)
    task = await task_service.get_task(db, task_id, project_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Task not found")
    await task_service.delete_task(db, task)