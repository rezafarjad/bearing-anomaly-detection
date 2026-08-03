import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft, butter, filtfilt, hilbert, find_peaks
from .data_loader import load_de_signal
from pathlib import Path


SAMPLING_RATE = 12000  # Hz


def spectral_kurtosis(signal, fs, nperseg=256):
    """Compute kurtosis at each frequency band using STFT, to find
    which frequency region contains the most impulsive (fault-related) energy."""
    f, t, Zxx = stft(signal, fs=fs, nperseg=nperseg)
    magnitude = np.abs(Zxx)

    mean = magnitude.mean(axis=1, keepdims=True)
    std = magnitude.std(axis=1, keepdims=True)
    std[std == 0] = 1e-12  # avoid divide-by-zero
    kurt = ((magnitude - mean) ** 4).mean(axis=1) / (std.flatten() ** 4) - 3

    return f, kurt


def best_band(freqs, kurt, fs, min_freq=500, bandwidth=1000):
    """Select the most impulsive band that fits at the full bandwidth."""
    nyquist = fs / 2
    max_freq = nyquist * 0.95
    half_bandwidth = bandwidth / 2

    minimum_center = min_freq + half_bandwidth
    maximum_center = max_freq - half_bandwidth

    mask = (
        (freqs >= minimum_center)
        & (freqs <= maximum_center)
    )

    if not np.any(mask):
        raise ValueError(
            "No valid band centre can fit the requested bandwidth"
        )

    peak_index = np.argmax(kurt[mask])
    center_freq = freqs[mask][peak_index]

    low = center_freq - half_bandwidth
    high = center_freq + half_bandwidth

    return low, high, center_freq


def bandpass_filter(signal, fs, low, high, order=4):
    nyq = fs / 2
    b, a = butter(order, [low / nyq, high / nyq], btype="band")
    return filtfilt(b, a, signal)


def envelope_spectrum(signal, fs):
    envelope = np.abs(hilbert(signal))
    envelope = envelope - envelope.mean()  # remove DC offset
    n = len(envelope)
    freqs = np.fft.rfftfreq(n, d=1 / fs)
    spectrum = np.abs(np.fft.rfft(envelope)) / n
    return freqs, spectrum


def analyze(filename, label):
    signal = load_de_signal(filename)

    sk_freqs, kurt = spectral_kurtosis(signal, SAMPLING_RATE)
    low, high, center = best_band(sk_freqs, kurt, SAMPLING_RATE)
    print(f"\n--- {label} ---")
    print(f"Selected band via spectral kurtosis: {low:.0f}-{high:.0f} Hz (center {center:.0f} Hz)")

    filtered = bandpass_filter(signal, SAMPLING_RATE, low, high)

    env_freqs, env_spectrum = envelope_spectrum(filtered, SAMPLING_RATE)

    mask = env_freqs <= 500
    peak_idx, _ = find_peaks(env_spectrum[mask], distance=5)
    peak_freqs = env_freqs[mask][peak_idx]
    peak_mags = env_spectrum[mask][peak_idx]
    top = sorted(zip(peak_freqs, peak_mags), key=lambda x: -x[1])[:5]

    print("Top envelope spectrum peaks (likely fault frequency candidates):")
    for f, mag in top:
        print(f"  {f:.1f} Hz   magnitude={mag:.5f}")

    return env_freqs, env_spectrum, label


if __name__ == "__main__":
    results = []
    for label, filename in [
    ("Normal", "Normal_1hp.mat"),
    ("Inner Race Fault (0.007\")", "IR007_1hp.mat"),
    ("Ball Fault (0.007\")", "B007_1hp.mat"),
    ("Outer Race Fault (0.007\")", "OR007_1hp.mat"),
]:
        results.append(analyze(filename, label))

    fig, axes = plt.subplots(len(results), 1, figsize=(10, 6), sharex=True)
    for ax, (freqs, spectrum, label) in zip(axes, results):
        mask = freqs <= 500
        ax.plot(freqs[mask], spectrum[mask])
        ax.set_title(f"Envelope Spectrum: {label}")
        ax.set_ylabel("Magnitude")
    axes[-1].set_xlabel("Frequency (Hz)")
    plt.tight_layout()
    output_path = Path(__file__).resolve().parent.parent / "figures" / "envelope_spectrum_comparison.png"
    fig.savefig(output_path, dpi=150)
    print("\nSaved plot to ../figures/envelope_spectrum_comparison.png")
    plt.show()