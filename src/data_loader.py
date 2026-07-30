import scipy.io
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def load_de_signal(filename):
    """Load the Drive-End (DE) vibration signal from a CWRU .mat file,
    regardless of the file's internal numeric ID prefix."""
    filepath = DATA_DIR / filename
    mat = scipy.io.loadmat(filepath)

    de_key = next((k for k in mat.keys() if k.endswith("_DE_time")), None)
    if de_key is None:
        raise ValueError(f"No DE_time channel found in {filename}")

    signal = mat[de_key].flatten()
    return signal

if __name__ == "__main__":
    sig = load_de_signal("Normal_1hp.mat")
    print(f"Loaded signal, length={len(sig)}, first 5 values={sig[:5]}")