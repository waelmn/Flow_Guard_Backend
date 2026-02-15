"""
Central configuration for FlowGuard
Reads settings from .env file
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ─── Paths ─────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent
MODELS_DIR  = BASE_DIR / "data" / "models"
SAMPLES_DIR = BASE_DIR / "data" / "samples"
DESIGNS_DIR = BASE_DIR / "data" / "reference_designs"

# ─── Model ─────────────────────────────────────
MODEL_NAME            = os.getenv("MODEL_NAME", "yolov8n.pt")
CONFIDENCE_THRESHOLD  = float(os.getenv("CONFIDENCE_THRESHOLD", 0.25))
IMAGE_SIZE            = 640

# ─── API ───────────────────────────────────────
API_HOST     = os.getenv("API_HOST", "0.0.0.0")
API_PORT     = int(os.getenv("API_PORT", 8000))
DEBUG        = os.getenv("DEBUG", "True") == "True"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# ─── Geometric Thresholds ──────────────────────
MIN_BEND_RADIUS_MM = 50   # Minimum acceptable bend radius
MAX_ANGLE_DEGREES  = 90   # Maximum connector angle

def get_model_path() -> Path:
    return MODELS_DIR / MODEL_NAME

def ensure_dirs():
    """Create required directories if missing"""
    for d in [MODELS_DIR, SAMPLES_DIR, DESIGNS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_dirs()
    print("✓ Config loaded")
    print(f"  BASE_DIR    : {BASE_DIR}")
    print(f"  MODEL_NAME  : {MODEL_NAME}")
    print(f"  CONFIDENCE  : {CONFIDENCE_THRESHOLD}")
    print(f"  API_PORT    : {API_PORT}")