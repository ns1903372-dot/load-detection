
---
title: Cognitive Load Detection Lab
emoji: brain
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Cognitive Load Detection Lab

This repository now includes a complete frontend and backend for a deployable cognitive load detection demo inspired by the original research notebooks in the repo.

## What's in the app

- A FastAPI backend for multimodal cognitive-load scoring
- A browser-based dashboard for entering EEG, HRV, typing, and mouse interaction signals
- A live prediction workflow with recommendations and modality breakdowns
- Docker packaging for Hugging Face Spaces deployment
- The original notebooks and architecture diagrams preserved for reference

## Product flow

1. Enter or load a scenario
2. Send the signal bundle to `/api/predict`
3. Receive a cognitive load score, band, confidence, and mitigation suggestions
4. Review the supporting modality breakdown in the UI

## API

### `GET /health`

Returns:

```json
{"status":"ok"}
```

### `POST /api/predict`

Example request:

```json
{
  "subject_id": "demo-subject-01",
  "context": "coding",
  "signals": {
    "eeg_focus_index": 46,
    "theta_beta_ratio": 3.2,
    "blink_rate_per_min": 24,
    "hrv_rmssd": 24,
    "typing_speed_wpm": 38,
    "typing_error_rate": 0.17,
    "mouse_hesitation_score": 62,
    "task_switches_per_min": 15,
    "session_duration_min": 118
  }
}
```

## Local run

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open `http://127.0.0.1:8000`.

## Hugging Face deployment

This repo is ready for a Docker Space.

1. Create a new Hugging Face Space with SDK `Docker`
2. Push this repository to the Space remote
3. Hugging Face will build the app automatically using the included Dockerfile

## Research assets kept in the repo

- `DEEPLEARNING_EEG.ipynb`
- `DWT.ipynb`
- `MAT_Preprocessing.ipynb`
- `high_level_architecture_clean.png`

