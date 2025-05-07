# FastAPI Hello World Practice

This repository contains a simple FastAPI program designed to practice working with FastAPI. It defines two routes:

### 1. **Root Route (`/`)**

* **Method**: `GET`
* **Description**: Returns a simple "Hello World" message.
* **URL**: `/`
* **Response**:

  ```json
  {
    "Message": "Hello World!"
  }
  ```

### 2. **Dynamic Item Route (`/items/{item_id}`)**

* **Method**: `GET`
* **Description**: Accepts an `item_id` as a path parameter (integer) and an optional query parameter `q` (string). If `q` is not provided, it returns `None`.
* **URL**: `/items/{item_id}?q={q}`

  * `item_id` is required and should be an integer.
  * `q` is an optional query parameter that, if provided, returns its value; otherwise, it returns `None`.
* **Example Requests and Responses**:

  * **Request 1**: `/items/42?q=apple`

    * **Response**:

      ```json
      {
        "item_id": 42,
        "q": "apple"
      }
      ```

  * **Request 2**: `/items/42`

    * **Response**:

      ```json
      {
        "item_id": 42,
        "q": null
      }
      ```

### Key Features:

* **Root Route**: Returns a basic "Hello World" message to confirm the server is running.
* **Dynamic Route**: Accepts path parameters and optional query parameters, demonstrating FastAPI's powerful automatic request parsing and validation.

