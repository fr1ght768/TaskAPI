# Multi-user Task Manager API

A simple and efficient backend application for task management (To-Do) featuring multi-user support. The project is fully containerized using Docker and is ready for deployment.

## Key Features
* Multi-user Architecture: Users register in the system and can only access their own tasks. Access is denied without providing the proper X-User-Id header.
* Full CRUD Support: Implements all major operations — viewing tasks (GET), creating (POST), updating content (PUT), and deleting (DELETE).
* Data Security and Authorization: Includes access rights checks. Users cannot modify or delete other people's tasks (returns a 403 Forbidden error).
* Data Persistence: Data persists across container restarts by leveraging an SQLite database bound to Docker Volumes.

## Tech Stack
* Language: Python 3.11+
* Framework: FastAPI (with data validation via Pydantic)
* Database: SQLite3 (built-in standard library module)
* DevOps: Docker, Docker Compose

---

## Getting Started

You can run the project in two ways: using Docker Compose (recommended) or running it locally.

### Method 1: Running with Docker Compose (Recommended)

Make sure you have Docker and Docker Compose installed on your system.

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <https://github.com/fr1ght768/TaskAPI.git>
   cd TaskAPI
   ```

2. Build and start the container in detached (background) mode:
   ```bash
   docker compose up -d
   ```

3. Open your browser and go to the interactive API documentation (Swagger UI):
   * http://127.0.0

Note for Fedora/RHEL users: If the container starts successfully but you receive a Connection Refused error in your browser, allow Docker traffic through your system firewall:
```bash
sudo firewall-cmd --zone=trusted --add-interface=docker0 --permanent
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

### Method 2: Local Setup (Without Docker)

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server using Uvicorn:
   ```bash
   uvicorn todolist:app --reload
   ```
   The API documentation will be available at http://127.0.0.

---

## API Specification and Usage Examples

To simulate user session and authorization, all task-related endpoints require the X-User-Id HTTP header.

* POST /register — Registers a new user (expects username and password in JSON body).
* GET /tasks — Retrieves the task list for the current user (requires X-User-Id header).
* POST /tasks — Creates a new task (expects task text in JSON body, binds it to the current X-User-Id).
* PUT /tasks/{task_id} — Updates the text of an existing task (allowed for the task owner only).
* DELETE /tasks/{task_id} — Deletes a task from the database (allowed for the task owner only).
