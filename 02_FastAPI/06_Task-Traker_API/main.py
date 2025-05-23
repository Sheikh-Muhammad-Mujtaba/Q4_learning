from fastapi import FastAPI, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, constr, validator, Field
from datetime import datetime, date
from typing import List


# Database simulation
USERS: dict[int, "UserRead"] = {}
TASKS: dict[int, "Task"] = {}

# configureation for the FastAPI app
app = FastAPI(
    title="Task Tracker API",
    description="A simple API to track tasks and their statuses.",
    version="1.0.0",
)


# pydantic models for user and task validation
class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password: constr(min_length=8)

class UserInDB(UserCreate):
    user_id: int


class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class Task(BaseModel):
    title: str
    description: str
    due_date: datetime
    status: str = Field(..., pattern="^(pending|in-progress|completed)$")

    @validator("due_date")
    def check_due_date(cls, v):
        if v.date() < date.today():
            raise ValueError("due_date must be today or in the future")
        return v


# dependency to check if user is logged in
def dep_login(
    username: str = Query(...),
    password: str = Query(...)
):

    for user_id, user_info in USERS.items():
        # Check if the username and password match
        if username == user_info.username and password == user_info.password:
            return {
                "message": "Logged in successfully",
                "username": username, "user_id": user_id
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )


# Endpoint to create a new user
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):

    user_id = len(USERS) + 1
    user_db  = UserInDB(user_id=user_id, **user.dict())
    USERS[user_id] = user_db 
    return UserRead(user_id=user_id, username=user.username, email=user.email)


# Endpoint to get user details
@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, user: UserRead = Depends(dep_login)):

    if user["user_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this user's information"
        )

    user = USERS.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# Endpoint to create a new task
@app.post("/tasks/", response_model=Task)
def create_task(task: Task, user: UserRead = Depends(dep_login)):

    task_id = len(TASKS) + 1
    new_task = task.dict()
    new_task["user_id"] = user["user_id"]
    TASKS[task_id] = new_task

    return new_task


# Endpoint to get tasks
@app.get("/task/{task_id}")
def get_task(task_id: int):

    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Endpoint to update a task
@app.put("/task/{task_id}", response_model=Task)
def update_task(task_id: int, status: str, user: UserRead = Depends(dep_login)):

    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["user_id"] != user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this task"
        )

    if status not in ["pending", "in-progress", "completed"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    task["status"] = status

    return task


# endpoint to get all tasks for a user
@app.get("/users/{user_id}/tasks", response_model=List[Task])
def get_tasks_by_user(user: UserRead = Depends(dep_login)):

    tasks = [task for task in TASKS.values() if task["user_id"] == user["user_id"]]
    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found for this user"
        )

    return tasks
