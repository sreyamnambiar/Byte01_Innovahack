import time
import random
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import router as api_router
from app.core.simulator import attack_simulator

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="DarkTrust Zero-Trust Security Platform for Decentralized APIs with sub-15ms proxy latency & lateral movement threat detection.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "proxy_overhead_target": f"<= {settings.TARGET_PROXY_LATENCY_MS}ms"
    }

# Background worker to seed initial realistic traffic telemetry for the dashboard
def background_traffic_simulator():
    scenarios = ["NORMAL_VERIFIED_REQUEST", "NORMAL_VERIFIED_REQUEST", "LATERAL_MOVEMENT", "NORMAL_VERIFIED_REQUEST", "TOKEN_REPLAY", "GEO_SPOOFING", "PAYLOAD_ANOMALY"]
    while True:
        try:
            scenario = random.choice(scenarios)
            attack_simulator.run_simulation(scenario)
            time.sleep(random.uniform(4.0, 8.0))
        except Exception:
            break

@app.on_event("startup")
def startup_event():
    # Run initial seed simulations
    for _ in range(5):
        attack_simulator.run_simulation("NORMAL_VERIFIED_REQUEST")
    attack_simulator.run_simulation("LATERAL_MOVEMENT")
    attack_simulator.run_simulation("PAYLOAD_ANOMALY")
    
    # Start background simulator thread
    t = threading.Thread(target=background_traffic_simulator, daemon=True)
    t.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
