from sqlalchemy.orm import Session
import models
import schemas
from schemas import Todo, TodoCreate, TodoUpdate
from uuid import UUID

# users 
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "fakepassword"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# todos
def get_todo(db: Session, user_id: int, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.user_id == user_id, models.Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def create_todo_item(db: Session, todo: TodoCreate):
    db_todo = models.Todo(**todo.dict(), id=id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo_item(db: Session, payload: schemas.TodoUpdate, todo_id: int):
    todo_query = db.query(models.Todo).filter(models.Todo.id==todo_id)
    todo = todo_query.first()
    update_todo = payload.dict(exclude_unset=True)
    todo_query.filter(models.Todo.id==todo_id).update(update_todo, synchronize_session=False)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo_item(db: Session, todo_id:int):
    todo_query = db.query(models.Todo).filter(models.Todo.id==todo_id)
    todo = todo_query.first()
    todo_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "Todo task deleted successfully!"}
    
