from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SignalInput(BaseModel):
    eeg_focus_index: float = Field(..., ge=0, le=100)
    theta_beta_ratio: float = Field(..., ge=0.5, le=5.0)
    blink_rate_per_min: float = Field(..., ge=0, le=60)
    hrv_rmssd: float = Field(..., ge=5, le=150)
    typing_speed_wpm: float = Field(..., ge=0, le=140)
    typing_error_rate: float = Field(..., ge=0, le=0.5)
    mouse_hesitation_score: float = Field(..., ge=0, le=100)
    task_switches_per_min: float = Field(..., ge=0, le=30)
    session_duration_min: float = Field(..., ge=1, le=240)


class PredictionRequest(BaseModel):
    subject_id: str = Field(..., min_length=1, max_length=80)
    context: Literal["exam", "coding", "learning", "driving", "general"] = "general"
    signals: SignalInput


class ModalityBreakdown(BaseModel):
    modality: str
    score: float
    contribution: float
    status: str
    explanation: str


class PredictionResponse(BaseModel):
    subject_id: str
    context: str
    load_score: float
    load_band: Literal["low", "moderate", "high", "critical"]
    confidence: float
    summary: str
    recommendations: list[str]
    modality_breakdown: list[ModalityBreakdown]

