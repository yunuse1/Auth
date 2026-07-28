# FastAPI Supabase Auth API

A lightweight, production-ready RESTful Authentication API built with **FastAPI** and integrated with **Supabase Auth**. This project provides secure user signup, authentication, token verification via HTTP Bearer scheme, and role-separated route protection.

---

## 🚀 Features

- **User Authentication**: Register new users and log in using email and password powered by Supabase.
- **Bearer Token Security**: Custom FastAPI dependency (`check_token`) validating JWT tokens against Supabase Auth.
- **Protected & Public Endpoints**: Clean separation between public access routes and token-guarded routes.
- **Interactive Documentation**: Auto-generated interactive API docs via Swagger UI and ReDoc.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Backend / Auth Provider**: [Supabase](https://supabase.com/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Environment Management**: `python-dotenv`

---

## ⚙️ Environment Variables Setup

Before running the application, configure your local environment variables.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and fill in your Supabase project credentials:
   ```env
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   PORT=8000
   ```

> **Note**: You can retrieve your `SUPABASE_URL` and `SUPABASE_KEY` (anon public key) from your **Supabase Dashboard** under `Project Settings > API`.

---

## 🏃 How to Run

### Prerequisites
- Python 3.10 or higher
- A Supabase account and active project

### 1. Clone the Repository
```bash
git clone https://github.com/yunuse1/Auth.git
cd Auth
```

### 2. Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Application

You can start the development server using either the `fastapi` CLI or `uvicorn`:

Using FastAPI CLI:
```bash
fastapi dev
```

Using Uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

The server will start running at `http://localhost:8000`.

---

## 📑 API Reference

| HTTP Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Root endpoint returning a welcome message | ❌ No |
| `POST` | `/auth/signup` | Registers a new user with email and password | ❌ No |
| `POST` | `/auth/login` | Authenticates credentials and returns Supabase JWT tokens | ❌ No |
| `POST` | `/auth/logout` | Signs out the current user session | ✅ Yes (Bearer Token) |
| `GET` | `/public/info` | Public informational endpoint | ❌ No |
| `GET` | `/protected/profile` | Fetches profile information for the authenticated user | ✅ Yes (Bearer Token) |
| `GET` | `/protected/dashboard` | Returns user stats for the authenticated session | ✅ Yes (Bearer Token) |

---

## 📸 Swagger UI Screenshots

Once the server is running, access the interactive API documentation at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

### 1. Authenticated Profile Endpoint Execution (`GET /protected/profile`)
Using the **Authorize** button in Swagger UI to attach the `Bearer <access_token>` allows access to protected resources.

![Swagger UI Protected Profile Execution](assets/swagger-protected-profile.png)

### 2. User Authentication Response (`POST /auth/login`)
Executing the `/auth/login` endpoint returns the session tokens (`access_token`, `refresh_token`) and user metadata from Supabase.

![Swagger UI Login Response](assets/swagger-login.png)

---

