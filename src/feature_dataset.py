"""Build a window-level feature dataset from CWRU vibration recordings."""

import csv
from pathlib import Path

import numpy as np

from .data_loader import load_de_signal
from .features import extract_time_features, split_into_windows


SAMPLING_RATE = 12000
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "window_features.csv"

SIGNALS = [
    ("normal", "Normal_1hp.mat"),
    ("inner_race_fault", "IR007_1hp.mat"),
    ("ball_fault", "B007_1hp.mat"),
    ("outer_race_fault", "OR007_1hp.mat"),
]


def build_feature_rows(
    signal: np.ndarray,
    condition: str,
    window_size: int = SAMPLING_RATE,
) -> list[dict[str, float | int | str]]:
    """Create one feature row for each non-overlapping signal window."""
    windows = split_into_windows(signal, window_size)
    rows = []

    for window_index, window in enumerate(windows):
        rows.append(
            {
                "condition": condition,
                "window_index": window_index,
                **extract_time_features(window),
            }
        )

    return rows


def write_feature_dataset(rows: list[dict[str, float | int | str]], output_path: Path) -> None:
    """Write window-level features to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    all_rows = []

    for condition, filename in SIGNALS:
        signal = load_de_signal(filename)
        rows = build_feature_rows(signal, condition)
        all_rows.extend(rows)
        print(f"{condition}: {len(rows)} windows")

    write_feature_dataset(all_rows, OUTPUT_PATH)
    print(f"Saved {len(all_rows)} feature rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()