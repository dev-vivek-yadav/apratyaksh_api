# User Pydantic schemas
# schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

