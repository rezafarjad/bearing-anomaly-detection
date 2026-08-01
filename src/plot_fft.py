from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from .data_loader import load_de_signal

SAMPLING_RATE = 12000  # Hz
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"

FILES = {
    "Normal": "Normal_1hp.mat",
    "Inner Race Fault (0.007\")": "IR007_1hp.mat",
    "Ball Fault (0.007\")": "B007_1hp.mat",
    "Outer Race Fault (0.007\")": "OR007_1hp.mat",
}

def compute_fft(signal, sampling_rate):
    """Return a one-sided, amplitude-corrected FFT spectrum."""
    signal = np.asarray(signal, dtype=float)

    if signal.ndim != 1 or signal.size < 2:
        raise ValueError("signal must be one-dimensional with at least 2 samples")
    if sampling_rate <= 0:
        raise ValueError("sampling_rate must be positive")

    number_of_samples = signal.size

    # Remove the mean so it does not create a large peak at 0 Hz.
    centered_signal = signal - np.mean(signal)

    # Reduce spectral leakage when a frequency falls between FFT bins.
    window = np.hanning(number_of_samples)
    windowed_signal = centered_signal * window

    frequencies = np.fft.rfftfreq(
        number_of_samples,
        d=1 / sampling_rate,
    )
    spectrum = np.abs(np.fft.rfft(windowed_signal)) / window.sum()

    # Convert the positive-frequency half into a one-sided amplitude spectrum.
    if number_of_samples % 2 == 0:
        spectrum[1:-1] *= 2
    else:
        spectrum[1:] *= 2

    return frequencies, spectrum

def plot_ffts(max_freq=1000):
    fig, axes = plt.subplots(len(FILES), 1, figsize=(10, 8), sharex=True)

    for ax, (label, filename) in zip(axes, FILES.items()):
        signal = load_de_signal(filename)
        freqs, spectrum = compute_fft(signal, SAMPLING_RATE)

        mask = freqs <= max_freq
        ax.plot(freqs[mask], spectrum[mask])
        ax.set_title(label)
        ax.set_ylabel("Magnitude")

    axes[-1].set_xlabel("Frequency (Hz)")
    plt.tight_layout()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "fft_comparison.png"
    plt.savefig(output_path, dpi=150)
    print(f"Saved plot to {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_ffts()
