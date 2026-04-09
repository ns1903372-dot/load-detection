from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "data" / "synthetic_cognitive_load_dataset.csv"
FEATURE_COLUMNS = [
    "eeg_focus_index",
    "theta_beta_ratio",
    "blink_rate_per_min",
    "hrv_rmssd",
    "typing_speed_wpm",
    "typing_error_rate",
    "mouse_hesitation_score",
    "task_switches_per_min",
    "session_duration_min",
]


def main() -> None:
    df = pd.read_csv(DATASET_PATH)

    x = df[FEATURE_COLUMNS]

    x_train_cls, x_test_cls, y_train_cls, y_test_cls = train_test_split(
        x,
        df["load_band"],
        test_size=0.3,
        random_state=42,
        stratify=df["load_band"],
    )
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(x_train_cls, y_train_cls)
    pred_cls = clf.predict(x_test_cls)

    x_train_reg, x_test_reg, y_train_reg, y_test_reg = train_test_split(
        x,
        df["load_score"],
        test_size=0.3,
        random_state=42,
    )
    reg = RandomForestRegressor(n_estimators=200, random_state=42)
    reg.fit(x_train_reg, y_train_reg)
    pred_reg = reg.predict(x_test_reg)

    print("BASELINE_CLASSIFIER")
    print(f"dataset={DATASET_PATH}")
    print(f"accuracy={accuracy_score(y_test_cls, pred_cls):.4f}")
    print("classification_report")
    print(classification_report(y_test_cls, pred_cls, digits=4))

    print("BASELINE_REGRESSOR")
    print(f"mae={mean_absolute_error(y_test_reg, pred_reg):.4f}")
    print(f"r2={r2_score(y_test_reg, pred_reg):.4f}")


if __name__ == "__main__":
    main()
