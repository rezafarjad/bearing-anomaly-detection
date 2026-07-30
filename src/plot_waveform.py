import matplotlib.pyplot as plt
from data_loader import load_de_signal

SAMPLING_RATE = 12000  # Hz, confirmed from CWRU 12k Drive End dataset

FILES = {
    "Normal": "Normal_1hp.mat",
    "Inner Race Fault (0.007\")": "IR007_1hp.mat",
    "Ball Fault (0.007\")": "B007_1hp.mat",
    "Outer Race Fault (0.007\")": "OR007_1hp.mat",
}

def plot_waveforms(duration_sec=0.1):
    n_samples = int(SAMPLING_RATE * duration_sec)

    fig, axes = plt.subplots(len(FILES), 1, figsize=(10, 8), sharex=True)

    for ax, (label, filename) in zip(axes, FILES.items()):
        signal = load_de_signal(filename)
        t = [i / SAMPLING_RATE for i in range(n_samples)]
        ax.plot(t, signal[:n_samples])
        ax.set_title(label)
        ax.set_ylabel("Amplitude")

    axes[-1].set_xlabel("Time (s)")
    plt.tight_layout()

    output_path = "../figures/raw_waveforms_comparison.png"
    plt.savefig(output_path, dpi=150)
    print(f"Saved plot to {output_path}")
    plt.show()

if __name__ == "__main__":
    plot_waveforms()