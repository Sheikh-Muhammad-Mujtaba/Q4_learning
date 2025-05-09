# FastAPI to use pydanic example practice

This project demonstrates how to use Pydantic with FastAPI ,it simulate simple chatbot API, showcasing Pydantic's powerful data validation features.

## Pydantic:
Pydantic is a Python library for data validation and setting management using python type annotation to define data schemas, rules that specify the structure and types of data. It's is a core dependency of FastAPI used for request/responce validation, type conversion, automatic error handling, serialization, and deserialization. it's perfect for ensuring your API handles data correctly.

## Key Features of Pydantic
- Type-Safety Validation: Validates data against Python type hints (e.g., str, int, List[str]).
- Automatic Type Conversion: Converts data to the correct type (e.g., string "123" to int 123).
- Error Handling: Raises detailed validation errors for invalid data.
- Nested Models: Supports complex, nested data structures.
- Serialization/Deserialization: Converts models to JSON for API responses and back.
- Default Values and Optional Fields: Simplifies schema definitions.
- Custom Validators: Allows custom validation logic.

## Project Overview

In this Project I have simulate simple example of chatbot FastAPI which uses Pydantic to validate user messages and generate responses, demonstrating key Pydantic features like type validation, nested models, default values, and error handling. The API includes three endpoints:

- **Root (`/`):** Returns a welcome message.
- **Get User (`/users/{user_id}`):** Retrieves user information with an optional role.
- **Chat (`/chat/`):** Processes user messages and returns chatbot replies.


The example is inspired by the “DACA tutorial series” (a fictional context for learning purposes) and is designed to be easy to understand and extend.


## Installation

Follow these steps to set up the project:

1. Create a new project directory:
```bash
uv init fastapi_pydantic_example
cd fastapi_pydantic_example
```

2. Set up a virtual environment:
```bash
uv venv
source .venv/bin/activate  
.venv\Scripts\activate # On Windows 
```

3. Install dependencies:
```bash
uv add "fastapi[standard]" 
```

1. **Save the example code:** Create a file named [<main.py and copy the code: 🔗](./main.py)

## Running Application

start the FastAPI server:
```bash
fastapi dev main.py
```
