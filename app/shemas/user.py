from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password : str

class UserRead(BaseModel):
    id : int
    email : str
    username : str
    is_active : bool

    model_config = {"from_attributes" : True}

class UserLogin(BaseModel):
    email : EmailStr
    password : str