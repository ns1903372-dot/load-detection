from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from cogload.models import PredictionRequest, PredictionResponse
from cogload.scoring import score_request


ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"

app = FastAPI(
    title="Cognitive Load Detection",
    description="Multimodal cognitive load scoring API and dashboard.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("/assets", StaticFiles(directory=ROOT), name="assets")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/presets")
def presets() -> dict[str, object]:
    return {
        "contexts": ["general", "coding", "learning", "exam", "driving"],
        "signals": {
            "eeg_focus_index": {"min": 0, "max": 100},
            "theta_beta_ratio": {"min": 0.5, "max": 5.0},
            "blink_rate_per_min": {"min": 0, "max": 60},
            "hrv_rmssd": {"min": 5, "max": 150},
            "typing_speed_wpm": {"min": 0, "max": 140},
            "typing_error_rate": {"min": 0, "max": 0.5},
            "mouse_hesitation_score": {"min": 0, "max": 100},
            "task_switches_per_min": {"min": 0, "max": 30},
            "session_duration_min": {"min": 1, "max": 240},
        },
    }


@app.post("/api/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    return score_request(request)


@app.get("/")
def home() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
