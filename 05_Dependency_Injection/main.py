from fastapi import FastAPI, Depends, HTTPException, status, Query
from typing import Annotated, Dict
from pydantic import BaseModel


app = FastAPI()

# fake database
tasks: Dict = {
    1: {"title": "Task 1", "description": "Description of Task 1", "user_id": 1},
    2: {"title": "Task 2", "description": "Description of Task 2", "user_id": 2},
    3: {"title": "Task 3", "description": "Description of Task 3", "user_id": 3},
}


users: Dict = {
    1: {"username": "user1", "password": "password1"},
    2: {"username": "user2", "password": "password2"},
    3: {"username": "user3", "password": "password3"},
}


# dependency to check if user is logged in
def dep_login(username: str = Query(...), password: str = Query(...)):
    
    for user_id, user_info in users.items():
        if username == user_info["username"] and password == user_info["password"]:
            return {"message": "Login Successful", "username": username, "user_id": user_id}
        
        
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
        
        
        
# Dependency to simulate database access
class GetObjectOr404():
    
    def __init__(self, model: dict) -> None:
        self.model = model
        
        
        
    def __call__(self, id: int):
        obj = self.model.get(id)
        
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with id {id} not found",
            )
            
            
        return obj
    
    
# Task Dependency (simulating a database)
task_dependency = GetObjectOr404(tasks)

# User Dependency (simulating a database)
user_dependency = GetObjectOr404(users)



# task model
class Task(BaseModel):
    task_name: str
    user_id: int
    


# Route to get a task (requires authentication and task access)
@app.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    user: Annotated[dict, Depends(dep_login)],
    task: Annotated[dict, Depends(task_dependency)],
):
    
    
    if task["user_id"] != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this task",
        )
        
        
    return task


# Route to create a new task (requires authentication)
@app.post("/tasks")
def create_task(
    task: Task,
    user: Annotated[dict, Depends(dep_login)],
):
    
    
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {'task_name': task.task_name, 'user_id': user['user_id']}
    
    
    return {"task_id": task_id, "task_name": task.task_name, "user_id": user['user_id']}

# Route to delete a task (requires authentication and ownership check)
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    user: Annotated[dict, Depends(dep_login)],
    task: Annotated[dict, Depends(task_dependency)],
):
    
    
    if task["user_id"] != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this task",
        )
        
    del tasks[task_id]
    
    
    return {"detail": "Task deleted successfully"}