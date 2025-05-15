
# ☁️ Cloud Service Access Management System (MongoDB + FastAPI)

This backend system manages access to cloud services based on user subscription plans. It uses **FastAPI** and **MongoDB (Atlas or local)** to simulate API permissions, quota enforcement, and role-based control.

---

## 🚀 Features

- ✅ Role-based access for `admin` and `customer`
- ✅ Subscription plans with API-level permissions and service usage limits
- ✅ Usage tracking and real-time limit enforcement
- ✅ 6 dummy cloud services: `/compute`, `/storage`, `/container`, `/db`, `/app`, `/ai`
- ✅ Admin-only management of plans and permissions
- ✅ Cookie-based login system

---

## ✅ Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)
- Git (optional, for cloning the repository)

---

## 🧱 Tech Stack

- **FastAPI** (Python web framework)
- **Motor** (async MongoDB client)
- **MongoDB Atlas** or local MongoDB
- **Pydantic v2** for request validation
- **Uvicorn** for development server

---

## 📁 Project Structure

```
.
├── main.py
├── database
│   └── __init__.py
├── routers/
│   ├── plans.py
│   ├── permissions.py
│   ├── subscriptions.py
│   ├── limits.py
│   ├── rbac.py
│   └── auth.py
├── .env
├── util.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone and Install

```bash
git clone <repo-url>
cd cloud-manager
poetry install
```

### 2. Environment Configuration

Create a `.env` file:

```env
DATABASE_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/cloudmanager
```

> Make sure to **percent-encode special characters** in your password

### 3. Run the Server

```bash
poetry run fastapi dev main.py
```

---

## 🔐 Authentication & RBAC

- `POST /auth/register` – Register with username + role
- `POST /auth/login` – Login via cookie
- Admin routes (`/plans`, `/permissions`) require role `admin`
- Cloud services check cookie + access via central `enforce_service_access()`

---

## ☁️ Example Cloud Service APIs

```http
GET /compute
GET /storage
GET /container
GET /db
GET /app
GET /ai
```

Access is allowed only if:
1. User is subscribed to a plan
2. Plan includes permission for the service
3. Usage is within defined limit

---

## 🧪 Sample Data Scripts

```bash
python util.py         # Loads sample users, plans, permissions, subscriptions
```

---

## 📊 Endpoints

### 🔐 Subscription Plan Management (Admin)
- `POST /plans` – Create a new plan
- `GET /plans` – Get all plans
- `GET /plans/{plan_id}` – Get plan by ID
- `PUT /plans/{plan_id}` – Update plan
- `DELETE /plans/{plan_id}` – Delete plan

### 📜 Permission Management (Admin)
- `POST /permissions` – Create a permission
- `GET /permissions` – Get all permissions
- `PUT /permissions/{name}` – Update a permission
- `DELETE /permissions/{name}` – Delete a permission

### 👥 User Subscription Handling
- `POST /subscriptions` – Subscribe to a plan
- `GET /subscriptions/{user_id}` – View user’s plan and usage details per service.
- `PUT /subscriptions/{user_id}` – Change user’s plan

### 🔍 Access Control & Usage Tracking
- `GET /access/{user_id}/{service}` – Check if user can access a service
- `POST /usage/{user_id}` – Log usage
- `GET /usage/{user_id}/limit` – Check limit status

---

## 👥 Roles

- **admin** – Full access to manage plans and permissions
- **customer** – Can access cloud services based on their plan

---

## 👥 Team Members

- Anirudh Ramakrishnan

---
