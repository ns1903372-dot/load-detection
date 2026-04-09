# Synthetic Dataset

This folder contains a small synthetic dataset for the Cognitive Load Detection project.

Files:

- `synthetic_cognitive_load_dataset.csv`

Notes:

- This is not a real medical or experimental dataset.
- It is intended for demo use, exploratory model prototyping, and UI testing.
- The columns mirror the app inputs in [app.py](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/app.py) and the scoring logic in [cogload/scoring.py](C:/Users/ns190/OneDrive/Documents/New%20project/load-detection/cogload/scoring.py).

Columns:

- `subject_id`: synthetic record identifier
- `context`: scenario type such as `coding`, `exam`, or `driving`
- `eeg_focus_index`: normalized EEG focus proxy from `0-100`
- `theta_beta_ratio`: EEG cognitive strain proxy
- `blink_rate_per_min`: eye-fatigue proxy
- `hrv_rmssd`: heart-rate-variability proxy
- `typing_speed_wpm`: typing speed
- `typing_error_rate`: typing error fraction
- `mouse_hesitation_score`: interaction-friction score from `0-100`
- `task_switches_per_min`: context switching rate
- `session_duration_min`: uninterrupted workload duration
- `load_score`: synthetic target score from `0-100`
- `load_band`: target class label

Suggested uses:

- train a baseline classifier for `load_band`
- train a regressor for `load_score`
- drive charts or example scenarios in the frontend
