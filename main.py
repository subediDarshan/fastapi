from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import IntEnum

app = FastAPI()




class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=2, max_length=254, description="Name for todo")
    todo_description: str = Field(..., min_length=2, max_length=254, description="Description for todo")
    todo_priority: Priority = Field(default=Priority.LOW, description="Priority for todo")

class Todo(TodoBase):
    todo_id: int = Field(..., description="Id of todo")

class Todo_create(TodoBase):
    pass

class Todo_update(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=2, max_length=254, description="Name for todo")
    todo_description: Optional[str] = Field(None, min_length=2, max_length=254, description="Description for todo")
    todo_priority: Optional[Priority] = Field(None, description="Priority for todo")



all_todos = [
    Todo(todo_id=1, todo_name="Typescript", todo_description="OS in rocket.chat", todo_priority=Priority.HIGH),
    Todo(todo_id=2, todo_name="Python", todo_description="OS in gitlab", todo_priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name="Ruby", todo_description="For OS in gitlab", todo_priority=Priority.LOW)
]






@app.get('/all-todo', response_model=List[Todo])
def get_all_todo():
    return all_todos


@app.get('/todo/{id}', response_model=Todo)
def get_todo(id: int):
    for todo in all_todos:
        if todo.todo_id == id:
            return todo
    raise HTTPException(status_code=404, detail="todo of that id not found")


@app.post('/todo', response_model=Todo)
def create_todo(new_todo: Todo_create):
    new_id = max(todo.todo_id for todo in all_todos) + 1
    todo = Todo(
        todo_id=new_id, 
        todo_name=new_todo.todo_name,
        todo_description=new_todo.todo_description,
        todo_priority=new_todo.todo_priority
        )
    all_todos.append(todo)
    return todo


@app.put('/todo/{id}', response_model=Todo)
def update_todo(id: int, new_todo: Todo_update):
    for todo in all_todos:
        if todo.todo_id == id:
            if new_todo.todo_name is not None:
                todo.todo_name = new_todo.todo_name
            if new_todo.todo_description is not None:
                todo.todo_description = new_todo.todo_description
            if new_todo.todo_priority is not None:
                todo.todo_priority = new_todo.todo_priority
            return todo
    raise HTTPException(status_code=404, detail="no todo with that id")



@app.delete('/todo/{id}', response_model=Todo)
def delete_todo(id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == id:
            deleted_todo = todo
            all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="no todo with that id")
