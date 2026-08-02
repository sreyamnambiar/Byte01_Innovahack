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
# 🌐 Dynamic Service Mesh

  Secure Service Mesh Communication.

<img width="1600" height="822" alt="Dynamic Service Mesh" src="https://github.com/user-attachments/assets/a88ba660-f24b-46b0-9f0b-c715d88c83b6" />


DarkTrust securely manages communication between distributed services while preventing unauthorized lateral movement across the network.

---

# 🛡️ Zero-Trust Policy Engine

 Context-Aware Policy Evaluation.

<img width="1600" height="832" alt="Contextual Policy Engine" src="https://github.com/user-attachments/assets/a87b140b-1be0-4774-9131-78fa7d4951b4" />


Every request is evaluated using contextual security policies including RBAC, payload validation, geolocation, and IP restrictions before access is granted.

---

# ⚡ Attack Simulation Studio

 Attack Simulation & Threat Detection.

<img width="1600" height="821" alt="Attack Simulation Studio" src="https://github.com/user-attachments/assets/d746d67b-f5a9-415b-ae54-5ed7c82aa9dc" />


DarkTrust safely simulates real-world attacks such as token replay, payload anomalies, and lateral movement to validate the effectiveness of the implemented security mechanisms.

---

# 📊 Audit Stream & Security Dashboard

 Real-Time Security Monitoring.

<img width="1600" height="737" alt="Audit Log Stream" src="https://github.com/user-attachments/assets/beb93c20-8e7a-4233-93e0-b3d32cd52761" />


The dashboard provides live security insights including detected threats, blocked attacks, proxy latency, intercepted traffic, and audit events.

---

# 📚 API Documentation & Database Schema

 Swagger API Documentation and Database Schema.

<img width="1600" height="805" alt="Backend API" src="https://github.com/user-attachments/assets/5f047f85-d6ac-4fac-984e-2567edd17522" />
<img width="1600" height="541" alt="Schemas" src="https://github.com/user-attachments/assets/64d519c9-0ac4-47c2-9cd6-8480920e7481" />



Interactive Swagger API documentation and a structured database schema simplify API testing and provide a clear representation of the application's data structure.



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
