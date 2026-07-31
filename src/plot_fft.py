import numpy as np
import matplotlib.pyplot as plt
from data_loader import load_de_signal

SAMPLING_RATE = 12000  # Hz

FILES = {
    "Normal": "Normal_1hp.mat",
    "Inner Race Fault (0.007\")": "IR007_1hp.mat",
    "Ball Fault (0.007\")": "B007_1hp.mat",
    "Outer Race Fault (0.007\")": "OR007_1hp.mat",
}

def compute_fft(signal, fs):
    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1/fs)
    spectrum = np.abs(np.fft.rfft(signal)) / n
    return freqs, spectrum

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

    output_path = "../figures/fft_comparison.png"
    plt.savefig(output_path, dpi=150)
    print(f"Saved plot to {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_ffts()