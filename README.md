# DarkTrust – Zero Trust Security Platform

> **Zero Trust Access Control for Decentralized APIs**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

---

## 📌 Overview

**DarkTrust** is an enterprise-grade Zero Trust Security Platform that protects communication between decentralized microservices.

Instead of trusting requests based on network location, every API request must be:

- ✅ **Authenticated** – Verified identity via JWT tokens
- ✅ **Authorized** – Policy-based access control per resource
- ✅ **Validated** – Request integrity and schema enforcement
- ✅ **Continuously Verified** – Contextual, real-time trust evaluation

The platform demonstrates a modern Zero Trust architecture suitable for enterprise environments and showcases:

- Secure API communication
- Contextual access control
- Attack detection and simulation
- Centralized monitoring and audit logging

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     DarkTrust Platform                  │
│                                                         │
│   ┌──────────────┐       ┌────────────────────────┐    │
│   │   Frontend   │──────▶│   API Gateway / Auth   │    │
│   │  React + Vite│       │   FastAPI + JWT         │    │
│   └──────────────┘       └────────────┬───────────┘    │
│                                       │                 │
│              ┌────────────────────────┼──────────────┐  │
│              │                        │              │  │
│   ┌──────────▼──────┐   ┌────────────▼──────┐       │  │
│   │  Policy Engine  │   │  Risk Score Engine│       │  │
│   │  (Zero Trust)   │   │  (Threat Context) │       │  │
│   └─────────────────┘   └───────────────────┘       │  │
│                                                      │  │
│              ┌───────────────────────────────────┐   │  │
│              │        PostgreSQL Database        │   │  │
│              │   (Audit Logs, Users, Policies)   │   │  │
│              └───────────────────────────────────┘   │  │
│                                                      │  │
└──────────────────────────────────────────────────────┘  │
```

---

## 🛠️ Tech Stack

### Frontend
| Technology       | Purpose                          |
|-----------------|----------------------------------|
| React 18        | UI framework                     |
| Vite            | Build tool & dev server          |
| Tailwind CSS    | Utility-first styling            |
| React Router DOM| Client-side routing              |
| Axios           | HTTP client / API layer          |

### Backend
| Technology       | Purpose                          |
|-----------------|----------------------------------|
| FastAPI         | High-performance async web API   |
| PostgreSQL 15+  | Primary relational database      |
| SQLAlchemy      | ORM with async support           |
| Alembic         | Database migration manager       |
| JWT / Passlib   | Authentication & password hashing|
| Pydantic v2     | Data validation & settings       |

---

## 📁 Project Structure

```
Byte01_Innovahack/
├── frontend/                   # React + Vite + Tailwind frontend
│   ├── public/
│   ├── src/
│   │   ├── assets/             # Static assets (images, icons)
│   │   ├── components/         # Reusable UI components
│   │   │   └── common/
│   │   ├── context/            # React Context API providers
│   │   ├── hooks/              # Custom React hooks
│   │   ├── layouts/            # Page layout wrappers
│   │   ├── pages/              # Route-level page components
│   │   ├── routes/             # Route definitions (React Router)
│   │   ├── services/           # Axios API service modules
│   │   ├── utils/              # Frontend utility functions
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── package.json
│
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── api/                # API route handlers
│   │   │   └── v1/             # API version 1
│   │   │       └── router.py
│   │   ├── auth/               # Authentication module
│   │   ├── core/               # App-wide configuration
│   │   │   ├── config.py       # Pydantic settings
│   │   │   ├── logging.py      # Structured logging
│   │   │   └── security.py     # JWT configuration stubs
│   │   ├── database/           # DB engine, sessions, base
│   │   │   ├── base.py
│   │   │   ├── engine.py
│   │   │   └── session.py
│   │   ├── middleware/         # Custom ASGI middleware
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business logic service layer
│   │   ├── security/           # Zero Trust security engine
│   │   ├── utils/              # Utility functions
│   │   └── main.py             # FastAPI application entry point
│   ├── alembic/                # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/                  # Test suite
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env.example
│
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+
- **PostgreSQL** 15+
- **Git**

---

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Unix/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc  

---

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your values

# Start development server
npm run dev
```

**Frontend:** http://localhost:5173

---

## 🔒 Zero Trust Principles

DarkTrust is built on the following Zero Trust tenets:

1. **Never Trust, Always Verify** – Every request is treated as potentially hostile
2. **Least Privilege Access** – Users receive only the minimum permissions required
3. **Assume Breach** – Systems are designed as if the network is already compromised
4. **Verify Explicitly** – Authentication and authorization use all available data points
5. **Continuous Validation** – Trust is re-evaluated at every request, not just login

---

## 📋 Planned Modules

| Module               | Description                                     | Status      |
|---------------------|-------------------------------------------------|-------------|
| Auth Engine         | JWT-based authentication & session management   | 🔜 Planned  |
| Policy Engine       | Attribute-based access control (ABAC)           | 🔜 Planned  |
| Risk Score Engine   | Real-time contextual risk assessment            | 🔜 Planned  |
| API Gateway         | Request routing, validation, rate limiting      | 🔜 Planned  |
| Attack Simulator    | Controlled security threat simulation           | 🔜 Planned  |
| Audit Engine        | Tamper-evident security audit logging           | 🔜 Planned  |
| Monitoring Dashboard| Real-time security metrics & visualization      | 🔜 Planned  |

---

## 🤝 Contributing

This is a hackathon project. For contribution guidelines, refer to the team documentation.

---

## 📄 License

This project is licensed under the MIT License.

---

*Built for national-level hackathon competition – Innovahack*
