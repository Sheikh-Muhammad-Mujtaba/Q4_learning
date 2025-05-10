# API Parameters

This project demonstrate how to use Path, Query and Body parameters in FastAPI, and explai about other API parameters.

## What is API Parameters?

API parameters are inputs you send to an API to control how it behaves or what data it returns. They tell the server what you want, how you want it, or what data you're sending.


## Types of API Parameters

### 1. Path Parameters

Used in the URL path to identify a specific resource.
- #### Use Case:
    When you want to fetch/update/delete a specific item by its ID.

- #### Syntax:

    ```python
    @app.get("/items/{item_id}")
    async def read_item(item_id: int):
        return {"item_id": item_id}
    ```
- #### URL Example:
    ```bash
    GET /items/42
    ```

### 2. Query Parameters
Sent after a ? in the URL, usually used to filter or paginate data.

- #### Use Case:
    Filtering search results, sorting, pagination.

- #### Syntax:
    ```python
    @app.get("/items/")
    async def list_items(skip: int = 0, limit: int = 10):
        return {"skip": skip, "limit": limit}
    ```

- #### URL Example:
    ```bash
    GET /items?skip=10&limit=5
    ```

### 3. Request Body Parameters
    Data sent in the body of the request (usually JSON), often used in POST, PUT, or PATCH.

- #### Use Case:
    Creating or updating resources with multiple fields.

- #### Syntax:
    ```python
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        price: float

    @app.post("/items/")
    async def create_item(item: Item):
        return {"item": item}
    ```

- #### Example:
    ```bash
    POST /items/
    Content-Type: application/json

    {
        "name": "Laptop",
        "price": 999.99
    }
    ```

### 4. Header Parameters
Sent in HTTP headers, often used for authentication, language preference, etc.

- #### Use Case:
    Passing tokens, custom headers.

- #### Syntax:
    ```python
    from fastapi import Header

    @app.get("/secure-data/")
    async def get_data(user_agent: str = Header(...)):
        return {"User-Agent": user_agent}
    ```

- #### Example:
    ```bash
    GET /secure-data/
    Headers:
    User-Agent: Mozilla/5.0
    ```

### 5. Cookie Parameters
Sent by the client as cookies. Useful for session-based auth.

- #### Use Case:
    Tracking sessions, auth tokens, preferences.

- #### Syntax:
    ```python
    from fastapi import Cookie

    @app.get("/me")
    async def read_me(session_id: str = Cookie(None)):
        return {"session_id": session_id}
    ```

- #### Example:
    ```bash
    GET /me
    Cookie: session_id=abc123
    ```


### 6. Form Data
Sent via application/x-www-form-urlencoded. Used in HTML forms.

- #### Use Case:
    Login forms, signups, contact forms.

- #### Syntax:
    ```python
    from fastapi import Form

    @app.post("/login/")
    async def login(username: str = Form(...), password: str = Form(...)):
        return {"username": username}
    ```

- #### Example:
    ```bash
    POST /login/
    Content-Type: application/x-www-form-urlencoded

    username=admin&password=1234
    ```


### 7. File Uploads
Used to handle file uploads through a form.

- #### Use Case:
    Uploading images, PDFs, docs.

- #### Syntax:
    ```python
    from fastapi import File, UploadFile

    @app.post("/upload/")
    async def upload_file(file: UploadFile = File(...)):
        return {"filename": file.filename}
    ```

- #### Example:
    Upload form with `multipart/form-data`









# Project Overview
This project implements a FastAPI application that demonstrates three key parameter types:

Path Parameters: Used to capture values from the URL (e.g., item IDs).
Query Parameters: Used to handle optional or filtering inputs (e.g., search queries or pagination).
Body Parameters: Used to process structured data sent in the request body (e.g., JSON payloads).

### The API includes three endpoints:

**GET /items/{item_id}:** Retrieves an item by its ID, using a Path parameter with validation (e.g., ID must be ≥ 1).
**GET /items/:** Lists items with optional Query parameters for filtering (e.g., search query, skip, limit).
**PUT /items/validated/{item_id}:** Updates an item, combining Path, Query, and Body parameters with Pydantic validation.

# Installation
## Follow these steps to set up the project:

### Create a new project directory:
```bash
mkdir fastapi-parameters-demo
cd fastapi-parameters-demo
```

### Set up a virtual environment:
```bash
uv venv
source .venv/bin/activate  
.venv\Scripts\activate  # On Windows
```

### Install dependencies:
```bash
uv add "fastapi[standard]" pydantic
```

### Save the example code:[Create a file named main.py and copy the following code:](./main.py)


## Running the Application

### Start the FastAPI server:
```bash
fastapi dev ./main.py
```

This runs the app with auto-reload for development at http://127.0.0.1:8000.

Access the documentation:Open your browser and visit:

http://127.0.0.1:8000/docs for interactive Swagger UI.
http://127.0.0.1:8000/redoc for alternative documentation.
