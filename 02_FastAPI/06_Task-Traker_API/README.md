# 📝 Task Tracker API

A simple FastAPI project to manage users and tasks, built as part of my learning journey in backend development and API security.

## 🚀 What I Learned

* ✅ **FastAPI Basics** – Creating APIs using path, query parameters, and request bodies.
* ✅ **Pydantic Models** – Data validation using `BaseModel`, `constr`, `EmailStr`, `Field`, and custom validators.
* ✅ **Dependency Injection** – Implementing simple login validation with FastAPI's `Depends()`.
* ✅ **In-Memory Storage** – Simulating a database using Python dictionaries.
* ✅ **RESTful Design** – Structuring endpoints for CRUD operations (Create, Read, Update).
* ✅ **Security Concepts** – Enforcing access control and basic authentication simulation.

---

## 📌 Endpoints Overview

| Method | Endpoint                 | Description                               |
| ------ | ------------------------ | ----------------------------------------- |
| `POST` | `/users/`                | Register a new user                       |
| `GET`  | `/users/{user_id}`       | Get user info (login required)            |
| `POST` | `/tasks/`                | Create a task for the logged-in user      |
| `GET`  | `/task/{task_id}`        | Get task by ID                            |
| `PUT`  | `/task/{task_id}`        | Update task status (owner only)           |
| `GET`  | `/users/{user_id}/tasks` | Get all tasks for a user (login required) |

---

## 🧪 How Login Works

* Users "log in" by providing their `username` and `password` as query parameters.
* A dependency (`dep_login`) verifies credentials from the in-memory user store.

