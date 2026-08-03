"""Train and evaluate a baseline novelty detector on vibration features."""

import csv
from pathlib import Path

import numpy as np
from sklearn.ensemble import IsolationForest


FEATURE_NAMES = ("rms", "kurtosis", "crest_factor")
FEATURE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "processed"
    / "window_features.csv"
)


def load_feature_rows(path: Path) -> list[dict[str, str]]:
    """Load generated window-level features from CSV."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def rows_to_matrix(rows: list[dict[str, str]]) -> np.ndarray:
    """Convert feature rows into a numerical matrix."""
    return np.array(
        [[float(row[feature]) for feature in FEATURE_NAMES] for row in rows],
        dtype=float,
    )


def calibrate_anomaly_threshold(
    training_scores: np.ndarray,
    quantile: float = 0.95,
) -> float:
    """Set an anomaly threshold from the normal training-score distribution."""
    training_scores = np.asarray(training_scores, dtype=float)

    if training_scores.ndim != 1 or training_scores.size == 0:
        raise ValueError("training_scores must be a non-empty one-dimensional array")

    if not 0 < quantile < 1:
        raise ValueError("quantile must be between 0 and 1")

    return float(np.quantile(training_scores, quantile))


def split_train_and_evaluation_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Train on early normal windows; evaluate later normal and all fault windows."""
    normal_rows = [row for row in rows if row["condition"] == "normal"]

    if len(normal_rows) < 2:
        raise ValueError("At least two normal windows are required")

    split_index = len(normal_rows) // 2
    training_rows = normal_rows[:split_index]

    evaluation_rows = normal_rows[split_index:] + [
        row for row in rows if row["condition"] != "normal"
    ]

    return training_rows, evaluation_rows


def main() -> None:
    rows = load_feature_rows(FEATURE_PATH)
    training_rows, evaluation_rows = split_train_and_evaluation_rows(rows)

    training_features = rows_to_matrix(training_rows)
    evaluation_features = rows_to_matrix(evaluation_rows)

    model = IsolationForest(
        contamination="auto",
        random_state=42,
    )
    model.fit(training_features)

    training_scores = -model.score_samples(training_features)
    anomaly_threshold = calibrate_anomaly_threshold(training_scores)

    anomaly_scores = -model.score_samples(evaluation_features)
    predictions = np.where(anomaly_scores > anomaly_threshold, -1, 1)

    print(f"Training normal windows: {len(training_rows)}")
    print(f"Calibrated anomaly threshold: {anomaly_threshold:.4f}")
    print("\nMean anomaly score by condition (higher means more unusual):")

    conditions = sorted({row["condition"] for row in evaluation_rows})
    for condition in conditions:
        indices = [
            index
            for index, row in enumerate(evaluation_rows)
            if row["condition"] == condition
        ]

        condition_scores = anomaly_scores[indices]
        condition_predictions = predictions[indices]
        anomaly_rate = np.mean(condition_predictions == -1)

        print(
            f"{condition:18} "
            f"mean_score={np.mean(condition_scores):.4f} "
            f"flagged={anomaly_rate:.0%}"
        )


if __name__ == "__main__":
    main()