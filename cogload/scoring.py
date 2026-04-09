from __future__ import annotations

from cogload.models import ModalityBreakdown, PredictionRequest, PredictionResponse


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def _normalize(value: float, lower: float, upper: float) -> float:
    if upper <= lower:
        return 0.0
    return _clamp(((value - lower) / (upper - lower)) * 100.0)


def _inverse_normalize(value: float, lower: float, upper: float) -> float:
    return 100.0 - _normalize(value, lower, upper)


def _band(score: float) -> str:
    if score < 30:
        return "low"
    if score < 55:
        return "moderate"
    if score < 75:
        return "high"
    return "critical"


def score_request(request: PredictionRequest) -> PredictionResponse:
    s = request.signals

    eeg_score = (
        0.55 * _inverse_normalize(s.eeg_focus_index, 30, 95)
        + 0.45 * _normalize(s.theta_beta_ratio, 1.2, 4.2)
    )
    ocular_score = _normalize(s.blink_rate_per_min, 8, 32)
    physiology_score = _inverse_normalize(s.hrv_rmssd, 22, 90)
    typing_score = (
        0.5 * _inverse_normalize(s.typing_speed_wpm, 20, 90)
        + 0.5 * _normalize(s.typing_error_rate, 0.02, 0.22)
    )
    interaction_score = (
        0.55 * _normalize(s.mouse_hesitation_score, 10, 75)
        + 0.45 * _normalize(s.task_switches_per_min, 2, 18)
    )
    endurance_score = _normalize(s.session_duration_min, 20, 140)

    weighted_score = (
        0.26 * eeg_score
        + 0.08 * ocular_score
        + 0.18 * physiology_score
        + 0.18 * typing_score
        + 0.2 * interaction_score
        + 0.1 * endurance_score
    )
    load_score = round(_clamp(weighted_score), 1)
    load_band = _band(load_score)

    spread = max(eeg_score, ocular_score, physiology_score, typing_score, interaction_score, endurance_score) - min(
        eeg_score, ocular_score, physiology_score, typing_score, interaction_score, endurance_score
    )
    confidence = round(_clamp(88 - (spread * 0.22), 55, 96) / 100.0, 2)

    modality_breakdown = [
        ModalityBreakdown(
            modality="EEG attention",
            score=round(eeg_score, 1),
            contribution=0.26,
            status="watch" if eeg_score >= 55 else "stable",
            explanation="Captures sustained attention strain from focus index and theta/beta balance.",
        ),
        ModalityBreakdown(
            modality="Ocular fatigue",
            score=round(ocular_score, 1),
            contribution=0.08,
            status="watch" if ocular_score >= 55 else "stable",
            explanation="Uses blink rate as a fatigue and eye-strain proxy.",
        ),
        ModalityBreakdown(
            modality="Autonomic stress",
            score=round(physiology_score, 1),
            contribution=0.18,
            status="watch" if physiology_score >= 55 else "stable",
            explanation="Lower HRV generally suggests more stress and lower recovery.",
        ),
        ModalityBreakdown(
            modality="Typing behavior",
            score=round(typing_score, 1),
            contribution=0.18,
            status="watch" if typing_score >= 55 else "stable",
            explanation="Combines typing speed drop and error rate increase into a friction signal.",
        ),
        ModalityBreakdown(
            modality="Interaction friction",
            score=round(interaction_score, 1),
            contribution=0.2,
            status="watch" if interaction_score >= 55 else "stable",
            explanation="Captures hesitation and rapid task switching during complex work.",
        ),
        ModalityBreakdown(
            modality="Session endurance",
            score=round(endurance_score, 1),
            contribution=0.1,
            status="watch" if endurance_score >= 55 else "stable",
            explanation="Longer uninterrupted sessions can amplify cognitive fatigue.",
        ),
    ]

    recommendations: list[str] = []
    if load_band in {"high", "critical"}:
        recommendations.append("Trigger a recovery break and reduce simultaneous task demands for the next 10 to 15 minutes.")
    if physiology_score >= 60 or eeg_score >= 60:
        recommendations.append("Lower stimulus intensity and add a short calibration or breathing interval before the next block.")
    if typing_score >= 55 or interaction_score >= 55:
        recommendations.append("Simplify the interface and defer non-essential notifications to reduce interaction friction.")
    if not recommendations:
        recommendations.append("Current workload appears manageable. Continue monitoring for sudden spikes during longer sessions.")

    if load_band == "critical":
        summary = "The subject is showing strong multimodal signs of overload and may be close to performance breakdown."
    elif load_band == "high":
        summary = "The subject appears cognitively strained, with several modalities pointing to rising workload and fatigue."
    elif load_band == "moderate":
        summary = "The subject is handling the session, but a few signals suggest meaningful effort and emerging strain."
    else:
        summary = "The current signal pattern suggests low cognitive load and stable working conditions."

    return PredictionResponse(
        subject_id=request.subject_id,
        context=request.context,
        load_score=load_score,
        load_band=load_band,
        confidence=confidence,
        summary=summary,
        recommendations=recommendations,
        modality_breakdown=modality_breakdown,
    )
