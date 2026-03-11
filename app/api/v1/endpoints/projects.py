from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.shemas.project import ProjectCreate, ProjectUpdate, ProjectRead
from app.services import project as project_service

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=list[ProjectRead])
async def list_projects(
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    return await project_service.get_projects(db, current_user.id)

@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    data : ProjectCreate,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    return await project_service.create_project(db, data, current_user.id)

@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
        project_id : int,
        db : AsyncSession = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    project = await project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Project not found"
        )
    return project

@router.put("/{project_id}", response_class=ProjectRead)
async def update_project(
    project_id : int,
    data : ProjectUpdate,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):
    project = await project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Project not found"
        )
    return await project_service.update_project(db, project, data)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id : int,
    db : AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user),
):
    project = await project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Project not found"
        )
    return await project_service.delete_project(db, project)