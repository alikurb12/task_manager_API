from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title : str
    description : str | None = None

class ProjectUpdate(BaseModel):
    title : str
    description : str | None = None

class ProjectRead(BaseModel):
    id : int
    title : str
    description : str | None
    owner_id : int

    model_config = {"from_attributes" : True}