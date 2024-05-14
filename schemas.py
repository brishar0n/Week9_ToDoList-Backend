from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

# todos
class TodoBase(BaseModel):
    task: str

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TodoUpdate(BaseModel):
    task: Optional[str] = None
    completed: Optional[bool] = None
    
# user
class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    todos: List[Todo] = []

    class Config:
        orm_mode = True
