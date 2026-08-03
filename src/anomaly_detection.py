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

    predictions = model.predict(evaluation_features)
    anomaly_scores = -model.decision_function(evaluation_features)

    print(f"Training normal windows: {len(training_rows)}")
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