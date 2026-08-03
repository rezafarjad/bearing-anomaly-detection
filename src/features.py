"""Windowing and interpretable time-domain features for vibration signals."""

import numpy as np
from scipy.stats import kurtosis


def split_into_windows(signal: np.ndarray, window_size: int) -> np.ndarray:
    """Split a one-dimensional signal into equal non-overlapping windows."""
    signal = np.asarray(signal, dtype=float)

    if signal.ndim != 1:
        raise ValueError("signal must be one-dimensional")

    if window_size <= 0:
        raise ValueError("window_size must be positive")

    number_of_windows = len(signal) // window_size

    if number_of_windows == 0:
        raise ValueError("signal is shorter than one window")

    usable_samples = number_of_windows * window_size
    return signal[:usable_samples].reshape(number_of_windows, window_size)


def extract_time_features(window: np.ndarray) -> dict[str, float]:
    """Calculate RMS, excess kurtosis, and crest factor for one window."""
    window = np.asarray(window, dtype=float)

    if window.ndim != 1 or window.size == 0:
        raise ValueError("window must be a non-empty one-dimensional array")

    rms = float(np.sqrt(np.mean(window ** 2)))
    peak = float(np.max(np.abs(window)))
    crest_factor = peak / rms if rms > 0 else 0.0

    if np.std(window) == 0:
        excess_kurtosis = 0.0
    else:
        excess_kurtosis = float(kurtosis(window, fisher=True, bias=False))

    return {
        "rms": rms,
        "kurtosis": excess_kurtosis,
        "crest_factor": crest_factor,
    }