from fastapi import FastAPI, Depends, HTTPException
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
import crud
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index():
    return {"Todo List Webapp Database by Brigitte - 2602119190"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{id}", response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get('/todos/all', response_model=List[schemas.TodoItem])
def get_all_todos(db: Session = Depends(get_db)):
    return crud.get_todo_items(db)

@app.get('/todos/get/{id}', response_model=schemas.TodoItem)
def get_todo(id: UUID, db: Session = Depends(get_db)):
    todo = crud.get_todo_item(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Task does not exist!")
    return todo

@app.post('/todos', response_model=schemas.TodoItem)
def post_todo(todo: schemas.TodoItemCreate, db: Session = Depends(get_db)):
    return crud.create_todo_item(db, todo)

@app.put("/todos/edit/{id}", response_model=schemas.TodoItem)
async def update_todo(id: UUID, todo: schemas.TodoItemUpdate, db: Session = Depends(get_db)):
    updated_todo = crud.update_todo_item(db, id, todo)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="ID does not exist!")
    return updated_todo

@app.delete("/todos/delete/{id}", response_model=schemas.TodoItem)
async def delete_todo(id: UUID, db: Session = Depends(get_db)):
    deleted_todo = crud.delete_todo_item(db, id)
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="ID does not exist!")
    return deleted_todo

@app.delete("/todos/delete_all")
def delete_all_todos(db: Session = Depends(get_db)):
    crud.delete_all_todo_items(db)
    return {"Msg": "Todo list cleared successfully!"}