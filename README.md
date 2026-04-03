# Simple Task Manager API

**Description:**

This project provides a simple RESTful API for managing tasks. It allows users to create, read, update, and delete tasks. The frontend provides a basic interface for interacting with the API.

**Why it's useful:**

A task manager is a fundamental tool for productivity. This API provides a foundation for building more complex task management applications or integrating task management functionality into existing systems.

**Installation:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/simple-task-manager.git
    cd simple-task-manager
    ```

2.  **Set up the backend:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```

3.  **Set up the frontend:**
    ```bash
    npm install
    npm start
    ```

**Running the Backend:**

```bash
python app.py
```

This will start the Flask server, typically on `http://127.0.0.1:5000/`.

**Running the Frontend:**

The frontend is a simple HTML page served by `index.html`.  It automatically opens in your browser when the backend is running.

**API Endpoints:**

*   `GET /tasks`: Retrieves all tasks.
*   `GET /tasks/<task_id>`: Retrieves a specific task by ID.
*   `POST /tasks`: Creates a new task.  Requires a JSON payload with `title` and `description`.
*   `PUT /tasks/<task_id>`: Updates an existing task. Requires a JSON payload with `title` and/or `description`.
*   `DELETE /tasks/<task_id>`: Deletes a task.

**Example Usage:**

*   **Create a task:**
    `curl -X POST -H "Content-Type: application/json" -d '{"title": "Grocery Shopping", "description": "Buy milk, eggs, and bread"}' http://127.0.0.1:5000/tasks`

*   **Get all tasks:**
    `curl http://127.0.0.1:5000/tasks`

*   **Update a task:**
    `curl -X PUT -H "Content-Type: application/json" -d '{"title": "Grocery Shopping", "description": "Buy milk, eggs, bread, and cheese"}' http://127.0.0.1:5000/tasks/1`

**Configuration:**

Environment variables are used for configuration.  A `.env.example` file is provided to show the expected variables.  You should create a `.env` file in the root directory of the project and populate it with your desired values.

**License:**

MIT License