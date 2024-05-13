from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class UserBase(BaseModel):
    email: str
    profileURL: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class TodoItemBase(BaseModel):
    task: str

class TodoItemCreate(TodoItemBase):
    pass

class TodoItemUpdate(BaseModel):
    task: Optional[str] = None
    completed: Optional[bool] = None

class TodoItem(TodoItemBase):
    id: UUID
    completed: bool

    class Config:
        orm_mode = True
        
class UserWithTodos(User):
    todos: List[TodoItem] = []

    class Config:
        orm_mode = True