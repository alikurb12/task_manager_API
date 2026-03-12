# 📋 Task Manager API

> A RESTful API for managing tasks and projects, built with FastAPI, PostgreSQL, and Docker.

---

## 🛠 Tech Stack

| Technology | Description |
|------------|-------------|
| **FastAPI** | Async web framework |
| **PostgreSQL** | Relational database |
| **SQLAlchemy 2.0** | Async ORM |
| **Alembic** | Database migrations |
| **JWT** | Authentication |
| **Docker** | Containerization |
| **Pydantic v2** | Data validation |

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose

### Run the project

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/task-manager-api.git
cd task-manager-api

# 2. Create the .env file
cp .env.example .env

# 3. Start the containers
docker compose up --build

# 4. Apply migrations (in a separate terminal)
docker compose exec app alembic upgrade head
```

API is available at `http://localhost:8000`  
Interactive Swagger docs: `http://localhost:8000/docs`

---

## 📡 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Login and receive a JWT token |
| `GET` | `/api/v1/auth/me` | Get current user profile |

### 📁 Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/projects/` | List all projects |
| `POST` | `/api/v1/projects/` | Create a project |
| `GET` | `/api/v1/projects/{id}` | Get a project by ID |
| `PUT` | `/api/v1/projects/{id}` | Update a project |
| `DELETE` | `/api/v1/projects/{id}` | Delete a project |

### ✅ Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/projects/{id}/tasks/` | List all tasks in a project |
| `POST` | `/api/v1/projects/{id}/tasks/` | Create a task |
| `GET` | `/api/v1/projects/{id}/tasks/{task_id}` | Get a task by ID |
| `PUT` | `/api/v1/projects/{id}/tasks/{task_id}` | Update a task |
| `DELETE` | `/api/v1/projects/{id}/tasks/{task_id}` | Delete a task |

---

## 🔐 Authentication

All endpoints except `/register` and `/login` require a Bearer token:

```
Authorization: Bearer <your_jwt_token>
```

### Usage Examples

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "user", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Create a project
curl -X POST http://localhost:8000/api/v1/projects/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Project", "description": "Project description"}'

# Create a task
curl -X POST http://localhost:8000/api/v1/projects/1/tasks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "priority": "high", "status": "todo"}'
```

---

## 🗂 Project Structure

```
task_manager/
├── app/
│   ├── api/v1/
│   │   └── endpoints/      # auth, projects, tasks
│   ├── core/               # config, security, dependencies
│   ├── db/                 # session, base
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── main.py
├── alembic/                # Migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## 📊 Data Models

```
User
├── id, email, username, hashed_password, is_active
├── → projects (one-to-many)
└── → tasks (one-to-many)

Project
├── id, title, description, owner_id
└── → tasks (one-to-many)

Task
├── id, title, description
├── status: todo | in_progress | done
├── priority: low | medium | high
├── due_date, created_at, updated_at
└── project_id, assignee_id
```

---

## ⚙️ Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `postgresql+asyncpg://postgres:postgres@db:5432/taskmanager` |
| `SECRET_KEY` | Secret key for JWT signing | `your-super-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time in minutes | `30` |

---

## 🐳 Docker Commands

```bash
# Start all services
docker compose up --build

# Stop all services
docker compose down

# Apply migrations
docker compose exec app alembic upgrade head

# Create a new migration
docker compose exec app alembic revision --autogenerate -m "migration name"

# View logs
docker compose logs -f app
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
