"""
FlowGuard API Entry Point
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import FRONTEND_URL, DEBUG, ensure_dirs

from api.routes import health, inspection, reports

# ─── Create directories on startup ─────────────
ensure_dirs()

# ─── App ───────────────────────────────────────
app = FastAPI(
    title="FlowGuard API",
    description="AI Visual Inspection System for Single-use Flowkits",
    version="0.1.0",
    debug=DEBUG,
)

# ─── CORS ──────────────────────────────────────
# Allows the frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ────────────────────────────────────
app.include_router(health.router,      prefix="/api",        tags=["Health"])
app.include_router(inspection.router,  prefix="/api",        tags=["Inspection"])
app.include_router(reports.router,     prefix="/api",        tags=["Reports"])

# ─── Root ──────────────────────────────────────
@app.get("/")
def root():
    return {"message": "FlowGuard API is running 🚀"}