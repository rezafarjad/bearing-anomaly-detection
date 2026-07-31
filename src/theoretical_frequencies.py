import scipy.io
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# CWRU SKF 6205-2RS JEM drive-end bearing geometry
N_BALLS = 9
BALL_DIAMETER = 0.3126   # inches
PITCH_DIAMETER = 1.537   # inches
CONTACT_ANGLE_DEG = 0

def get_rpm(filename):
    filepath = DATA_DIR / filename
    mat = scipy.io.loadmat(filepath)
    rpm_key = next((k for k in mat.keys() if k.endswith("RPM")), None)
    if rpm_key is None:
        raise ValueError(f"No RPM key found in {filename}")
    return float(mat[rpm_key].flatten()[0])

def theoretical_frequencies(rpm):
    import math
    fr = rpm / 60
    d_over_D = BALL_DIAMETER / PITCH_DIAMETER
    cos_theta = math.cos(math.radians(CONTACT_ANGLE_DEG))

    bpfi = (N_BALLS / 2) * fr * (1 + d_over_D * cos_theta)
    bpfo = (N_BALLS / 2) * fr * (1 - d_over_D * cos_theta)
    bsf = (PITCH_DIAMETER / (2 * BALL_DIAMETER)) * fr * (1 - (d_over_D * cos_theta) ** 2)

    return {"fr": fr, "BPFI": bpfi, "BPFO": bpfo, "BSF": bsf}

if __name__ == "__main__":
    rpm = get_rpm("IR007_1hp.mat")
    freqs = theoretical_frequencies(rpm)

    print(f"RPM (from file): {rpm}")
    print(f"Shaft rotation frequency (fr): {freqs['fr']:.2f} Hz")
    print(f"Theoretical BPFI: {freqs['BPFI']:.2f} Hz")
    print(f"Theoretical BPFO: {freqs['BPFO']:.2f} Hz")
    print(f"Theoretical BSF:  {freqs['BSF']:.2f} Hz")