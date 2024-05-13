from sqlalchemy.orm import Session
import models
import schemas
from schemas import TodoItem, TodoItemCreate, TodoItemUpdate
from uuid import UUID

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_todo_item(db: Session, todo_id: UUID):
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()

def get_todo_items(db: Session):
    return db.query(TodoItem).all()

def create_todo_item(db: Session, todo: TodoItemCreate):
    db_todo = models.Todo(**todo.dict(), id=id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo_item(db: Session, todo_id: UUID, todo_update: TodoItemUpdate):
    db_todo = get_todo_item(db, todo_id)
    if db_todo is None:
        return None
    for attr, value in todo_update.dict().items():
        setattr(db_todo, attr, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo_item(db: Session, todo_id: UUID):
    db_todo = get_todo_item(db, todo_id)
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo