from fastapi import FastAPI, HTTPException, status, Header
from typing import List, Dict, Optional, Annotated
from pydantic import BaseModel
from db import init_db, add_user_to_db, get_user_tasks_from_db, add_task_to_db, get_task_by_id, delete_task_by_id, update_task_in_db
import asyncio

app = FastAPI()

init_db()

class UpdateTask(BaseModel):
    new_task: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id : int
    username: str

class Task(BaseModel):
    id: int
    task : str

class TaskCreate(BaseModel):
    task : str

class TaskOut(BaseModel):
    id : int
    task: str
    user_id : int



@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate):
    new_user = add_user_to_db(payload.username, f"hash_{payload.password}")

    if not new_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return new_user

@app.get("/")
async def home() -> dict:
    return {"message" : "Welcome to Task API"}

@app.get("/tasks", response_model=List[TaskOut])
async def tasks(x_user_id: int = Header(...)):
    return get_user_tasks_from_db(x_user_id)

@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def add_task(payload: TaskCreate, x_user_id: int = Header(...)):
    return add_task_to_db(payload.task, x_user_id)

@app.put("/tasks/{task_id}")
async def edit_task(task_id: int, payload: UpdateTask, x_user_id: int = Header(...)):
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not found")
    
    if task["user_id"] != x_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have permisson to edit this task")

    update_task_in_db(task_id, payload.new_task)

    return {"id" : task_id, "task" : payload.new_task, "user_id": x_user_id}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, x_user_id: int = Header(...)):
    task = get_task_by_id(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["user_id"] != x_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have permission to delete this task")

    delete_task_by_id(task_id)
    return {f"status" : f"Task {task_id} succesfully deleted"}

    
