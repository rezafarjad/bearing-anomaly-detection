"""Multi-resolution kurtosis band scan for envelope-analysis experiments."""

from dataclasses import dataclass

import numpy as np
from scipy.signal import butter, sosfiltfilt
from scipy.stats import kurtosis


@dataclass(frozen=True)
class BandResult:
    low_hz: float
    high_hz: float
    excess_kurtosis: float


def candidate_bands(
    fs: float,
    widths_hz: tuple[float, ...] = (250.0, 500.0, 1000.0),
    min_freq_hz: float = 500.0,
    max_nyquist_fraction: float = 0.95,
):
    """Yield valid overlapping frequency bands at several bandwidths."""
    max_freq_hz = (fs / 2) * max_nyquist_fraction

    for width_hz in widths_hz:
        step_hz = width_hz / 2

        low_hz = min_freq_hz
        while low_hz + width_hz <= max_freq_hz:
            yield low_hz, low_hz + width_hz
            low_hz += step_hz


def band_excess_kurtosis(
    signal: np.ndarray,
    fs: float,
    low_hz: float,
    high_hz: float,
) -> float:
    """Return excess kurtosis after band-pass filtering one candidate band."""
    sos = butter(4, [low_hz, high_hz], btype="bandpass", fs=fs, output="sos")
    filtered = sosfiltfilt(sos, signal)

    return float(kurtosis(filtered, fisher=True, bias=False))


def select_kurtosis_band(signal: np.ndarray, fs: float) -> BandResult:
    """Select the candidate band with the largest excess kurtosis."""
    signal = np.asarray(signal, dtype=float)

    if signal.ndim != 1 or signal.size < 3:
        raise ValueError("signal must be a one-dimensional array with at least 3 samples")

    results = [
        BandResult(low_hz, high_hz, band_excess_kurtosis(signal, fs, low_hz, high_hz))
        for low_hz, high_hz in candidate_bands(fs)
    ]

    return max(results, key=lambda result: result.excess_kurtosis)