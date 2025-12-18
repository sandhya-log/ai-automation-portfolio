from pydantic import BaseModel, EmailStr
from typing import Optional 

class UserCreate(BaseModel):
    email : EmailStr
    password: str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id : int
    email : EmailStr

    class Config:
        orm_mode = True 

