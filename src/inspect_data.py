import scipy.io
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def inspect_file(filename):
    filepath = DATA_DIR / filename
    mat = scipy.io.loadmat(filepath)

    print(f"\n--- {filename} ---")
    print("Keys found in this file:")
    for key in mat.keys():
        if not key.startswith("__"):  # skip metadata keys
            value = mat[key]
            print(f"  {key}: shape={value.shape}, dtype={value.dtype}")

if __name__ == "__main__":
    inspect_file("Normal_1hp.mat")
    inspect_file("IR007_1hp.mat")
    inspect_file("B007_1hp.mat")