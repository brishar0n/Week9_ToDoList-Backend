from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String)

    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean)
    isEditing = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")
