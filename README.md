
# 🌩️ cloud-manager

This project is a backend system built using **FastAPI** to manage access to cloud services based on user subscription plans. It supports role-based access control (RBAC), subscription handling, API permission enforcement, and usage limit tracking.

---

## ✅ Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)
- Git (optional, for cloning the repository)

---

## 📦 Features

- ✅ **Role-based access control (RBAC)** for Admins and Customers
- 🔐 **Subscription plans** with API permissions and usage limits
- 📊 **Usage tracking** and limit enforcement
- ⚙️ Admin can **create, update, delete** plans and permissions
- 👤 Customers can **subscribe, view plans, and monitor usage**
- 🌐 Includes 6 dummy APIs representing cloud services

---

## 🚀 Tech Stack

- **FastAPI** (Python web framework)
- **Uvicorn** (ASGI server)
- **SQLite/PostgreSQL** (You can choose either)
- **SQLAlchemy / Tortoise ORM** (for async DB interaction)
- **Pydantic** (data validation)

---

## 📂 Project Structure

```
cloud-manager/
├── main.py
├── routers/
│   ├── plans.py
│   ├── permissions.py
│   ├── subscriptions.py
│   ├── access.py
│   ├── usage.py
├── models/
│   ├── (database models here)
├── schemas/
│   ├── (Pydantic schemas here)
├── database/
│   ├── (connection setup)
├── utils/
│   ├── (RBAC checks, usage logic)
├── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cloud-manager.git
cd cloud-manager
```

### 2. Set Up Environment with Poetry

```bash
poetry install
```

### 3. Run the Development Server

```bash
poetry run uvicorn main:app --reload
```

> Poetry handles all dependencies automatically based on the `pyproject.toml` file.
### 4. Run the Server

```bash
uvicorn main:app --reload
```

Server will run at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔌 Example Endpoints

### 🔐 Subscription Plan Management (Admin)
- `POST /plans` – Create a new plan
- `PUT /plans/{plan_id}` – Update plan
- `DELETE /plans/{plan_id}` – Delete plan

### 📜 Permission Management (Admin)
- `POST /permissions`
- `PUT /permissions/{permission_id}`
- `DELETE /permissions/{permission_id}`

### 👥 User Subscription Handling
- `POST /subscriptions` – Subscribe to a plan
- `GET /subscriptions/{user_id}` – View user’s plan
- `GET /subscriptions/{user_id}/usage` – View usage
- `PUT /subscriptions/{user_id}` – Change user’s plan

### 🔍 Access Control & Usage Tracking
- `GET /access/{user_id}/{api_request}` – Check access
- `POST /usage/{user_id}` – Log usage
- `GET /usage/{user_id}/limit` – Check limit status

---

## 🧪 Dummy Cloud Services

These are example APIs:
- `GET /service1` to `GET /service6`

They simply return mock responses for testing access control logic.

---

## 📹 Deliverables

- ✅ **GitHub Repository** with full code
- ✅ **README** with setup and API details
- ✅ **Demo Video** showing features and implementation

---

## 👥 Team Members

- Anirudh Ramakrishnan

---

## 📝 License

MIT License. Feel free to fork and modify!
