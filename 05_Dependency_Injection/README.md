# **Task Management System with FastAPI**

This is a simple **Task Management System** built with **FastAPI** that demonstrates the usage of **Dependency Injection** to manage common tasks such as authentication and database access. It contains routes for users to **register, log in, create tasks, view tasks, and delete tasks**, while ensuring that users can only manage their own tasks.

### **What is Dependency Injection?**

**Dependency Injection (DI)** is a design pattern that allows you to **inject** dependencies (like services or resources) into your code without tightly coupling them with your main logic. In FastAPI, DI is used to manage dependencies in an efficient and clean way. It allows us to:

1. Share common logic (e.g., authentication).
2. Avoid repetitive code.
3. Keep the code clean and modular.

### **Why Use Dependency Injection?**

* **Code Reusability**: Write a function once, and use it across multiple endpoints. For example, the `dep_login` function is used to handle login for various endpoints.
* **Separation of Concerns**: Each endpoint focuses on its specific task, while dependencies handle authentication, database access, etc.
* **Testability**: It's easier to test individual components by mocking dependencies.
* **Organization**: Keeps the code structured and clean, ensuring common logic is centralized.

### **Project Details**

#### **Features**:

* **User Authentication**: Users log in using a username and password.
* **Task Management**: Users can create, view, and delete their own tasks.
* **Role-based Access**: Only the user who created the task can view or delete it.
* **Dependency Injection**: Used for login validation, task access, and user verification.

#### **Endpoints**:

1. **POST /task**: Create a new task (requires authentication).
2. **GET /task/{task\_id}**: View a specific task (only accessible by the user who created it).
3. **DELETE /task/{task\_id}**: Delete a task (only accessible by the user who created it).

### **Setup and Running the Application**:

1. Setup new project using Uv:

   ```bash
   uv init dep_injection
   ```
2. activate enviournment :
   
   ```bash
    uv venv
    source .venv/bin/activate  
    .venv\Scripts\activate  # On Windows
   ```

3. Install FastAPI:

   ```bash
   uv add fastapi[standard]
   ```

4. Run the application:

   ```bash
   fastapi dev main.py
   ```

5. Access the API at `http://127.0.0.1:8000/docs`.

---

### Key Takeaways:

* **Dependency Injection** is a powerful pattern to manage shared logic and resources across your FastAPI app.
* By using DI, we can keep our code **modular** and **easy to maintain**.
* FastAPI provides a very simple and effective way to handle DI with the `Depends` function.

