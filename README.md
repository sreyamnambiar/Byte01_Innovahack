# 🛡️ DarkTrust – Zero Trust Access Control for Decentralized APIs

Developed for the **InnovaHack Hackathon** (`Byte01_Innovahack`).

> *"Never Trust. Always Verify."*

---

## 📌 Problem Statement & Background

### Background
Enterprise applications run across highly distributed multi-cloud and microservice architectures. Traditional perimeter firewalls cannot easily police lateral internal API communications once the outer boundary is passed.

### The Pain Point
Once an attacker breaks into one vulnerable edge microservice, they move laterally across internal networks unhindered, scraping backend databases via unsecured APIs.

### The Solution: DarkTrust
DarkTrust constructs a lightweight, dynamic **Service Mesh Proxy Interceptor** that enforces cryptographic identity verification for every single microservice request. It dynamically evaluates contextual security policies (Time, Geolocation, Payload anomalies, RBAC) and actively re-authenticates endpoints with sub-15ms overhead latency.

---

## ✨ Key Features

- 🔐 **Cryptographic Microservice Identity**: Ephemeral 30s tokens signed with HMAC-SHA256, payload hashes (`phash`), and nonce verification.
- 🌐 **Dynamic Service Mesh Proxy**: Intercepts requests between microservices, tracking exact overhead latency ($\le 15\text{ ms}$ target).
- 🛡️ **Zero-Trust Contextual Policy Engine**: Enforces Geolocation fences, Payload size caps (50KB limit), IP blacklists, and RBAC matrix.
- 📊 **Adaptive Risk & Lateral Movement Detector**: Detects illegal direct hops (e.g. `edge-gateway` ➔ `database-api`), scraping anomalies, and computes dynamic risk scores (0–100).
- ⚡ **Attack Simulation Studio**: Interactive one-click attack triggers (Edge Compromise & Lateral Hop, Ephemeral Token Replay, TOR Exit Node Bypass, Payload Exfiltration Anomaly).
- 📜 **Real-Time Audit Stream & Telemetry**: Live stream of intercepted request events, threat signals, and latency metrics.
- 🎨 **Modern Cyber-Security UI**: Built with React & Vite using a dark obsidian design system.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** (Python 3.10+)
- **PyJWT & Cryptography** (HMAC-SHA256 & Ephemeral Token Signing)
- **Pydantic v2** (Data validation & schemas)
- **Pytest** (Automated test suite)

### Frontend
- **React.js & Vite**
- **Lucide Icons**
- **Custom CSS Cyber Design System** (Glassmorphism, Neon Cyan/Purple glow effects)

---

## 🏗️ System Architecture

```
[ Client / External Ingress ]
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│              DarkTrust Service Mesh Proxy               │
│                                                         │
│  ├── Cryptographic Identity Engine (HMAC / Nonces)       │
│  ├── Contextual Policy Engine (Geo, Time, Payload, RBAC)│
│  ├── Adaptive Risk Engine (Lateral Movement Detector)   │
│  └── Sub-15ms Latency Overhead Interceptor              │
└─────────────────────────────────────────────────────────┘
            │                                    │
    (Allowed Hops)                        (Blocked Hops)
            │                                    │
            ▼                                    ▼
┌─────────────────────────┐            ┌──────────────────┐
│ Target Microservices    │            │ 🚨 Threat Block  │
│ (User, Auth, DB API)    │            │ Audit Log Stream │
└─────────────────────────┘            └──────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Launching the Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
- **API Documentation**: Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

### 2. Launching the Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
- Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Automated Verification & Testing

Run pytest suite to verify proxy latency target ($\le 15\text{ms}$), cryptographic verification, and attack detection:

```bash
cd backend
pytest
```

---

## 👥 Team Contributions

| Member | Focus Area |
| :--- | :--- |
| **Member 1** | Backend API, Cryptographic Identity & Ephemeral Tokens |
| **Member 2** | React Frontend Dashboard, Service Mesh Visualizer & UI |
| **Member 3** | Zero-Trust Policy Engine, Service Mesh Proxy Interceptor |
| **Member 4** | Adaptive Risk Engine, Lateral Movement Detector & Attack Simulator |

---

*DarkTrust – Zero Trust Access Control for Decentralized APIs*
