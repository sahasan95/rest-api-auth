# 🔐 REST API with Authentication

A production-ready RESTful API built with **Python** and **FastAPI**, featuring JWT-based authentication, role-based access control, and PostgreSQL integration.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=flat&logo=jsonwebtokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker&logoColor=white)

---

## ✨ Features

- **JWT Authentication** — Secure token-based login with access & refresh tokens
- **User Registration & Login** — Full auth flow with hashed passwords (bcrypt)
- **Role-Based Access Control** — Admin and standard user roles
- **Protected Routes** — Middleware-guarded endpoints
- **PostgreSQL Integration** — SQLAlchemy ORM with Alembic migrations
- **Input Validation** — Pydantic schemas for all request/response models
- **Auto-generated Docs** — Interactive Swagger UI at `/docs`
- **Rate Limiting** — Prevent abuse on auth endpoints
- **Docker Support** — Containerized for easy deployment

---

## 📁 Project Structure

```
rest-api-auth/
├── app/
│   ├── main.py              # App entry point
│   ├── config.py            # Environment config
│   ├── database.py          # DB connection & session
│   ├── models/
│   │   └── user.py          # SQLAlchemy models
│   ├── schemas/
│   │   └── user.py          # Pydantic schemas
│   ├── routers/
│   │   ├── auth.py          # /auth endpoints
│   │   └── users.py         # /users endpoints
│   └── utils/
│       ├── auth.py          # JWT helpers
│       └── hashing.py       # Password hashing
├── alembic/                 # DB migrations
├── tests/                   # Unit & integration tests
├── .env.example             # Environment variable template
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- (Optional) Docker & Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rest-api-auth.git
cd rest-api-auth
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/authdb
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be running at `http://localhost:8000`

---

## 🐳 Running with Docker

```bash
docker-compose up --build
```

This starts both the FastAPI app and a PostgreSQL container automatically.

---

## 📖 API Endpoints

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive tokens |
| `POST` | `/auth/refresh` | Refresh access token |
| `POST` | `/auth/logout` | Invalidate refresh token |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/users/me` | Get current user profile | ✅ |
| `PUT` | `/users/me` | Update current user | ✅ |
| `GET` | `/users/` | List all users (admin only) | ✅ Admin |
| `DELETE` | `/users/{id}` | Delete a user (admin only) | ✅ Admin |

---

## 📬 Example Requests

**Register a user:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

**Access a protected route:**
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI |
| Language | Python 3.11 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT (python-jose) |
| Password Hashing | bcrypt (passlib) |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Testing | Pytest |
| Containerization | Docker |

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
