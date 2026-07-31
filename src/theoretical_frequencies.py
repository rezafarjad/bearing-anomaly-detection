import math
from pathlib import Path

import scipy.io


DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# CWRU SKF 6205-2RS JEM drive-end bearing geometry
N_BALLS = 9
BALL_DIAMETER = 0.3126  # inches
PITCH_DIAMETER = 1.537  # inches
CONTACT_ANGLE_DEG = 0


def get_rpm(filename):
    """Read the motor RPM stored inside a CWRU MATLAB file."""
    filepath = DATA_DIR / filename
    mat = scipy.io.loadmat(filepath)

    rpm_key = next((key for key in mat if key.endswith("RPM")), None)

    if rpm_key is None:
        raise ValueError(f"No RPM key found in {filename}")

    return float(mat[rpm_key].flatten()[0])


def theoretical_frequencies(rpm):
    """Calculate theoretical bearing frequencies from motor speed."""
    fr = rpm / 60

    diameter_ratio = BALL_DIAMETER / PITCH_DIAMETER
    contact_angle = math.radians(CONTACT_ANGLE_DEG)
    cos_theta = math.cos(contact_angle)

    bpfi = (
        (N_BALLS / 2)
        * fr
        * (1 + diameter_ratio * cos_theta)
    )

    bpfo = (
        (N_BALLS / 2)
        * fr
        * (1 - diameter_ratio * cos_theta)
    )

    bsf = (
        (PITCH_DIAMETER / (2 * BALL_DIAMETER))
        * fr
        * (1 - (diameter_ratio * cos_theta) ** 2)
    )

    ftf = (
        0.5
        * fr
        * (1 - diameter_ratio * cos_theta)
    )

    rolling_element_frequency = 2 * bsf

    return {
        "fr": fr,
        "BPFI": bpfi,
        "BPFO": bpfo,
        "BSF": bsf,
        "FTF": ftf,
        "2xBSF": rolling_element_frequency,
    }


if __name__ == "__main__":
    rpm = get_rpm("IR007_1hp.mat")
    frequencies = theoretical_frequencies(rpm)

    print(f"RPM (from file): {rpm}")
    print(
        f"Shaft rotation frequency: "
        f"{frequencies['fr']:.2f} Hz"
    )
    print(f"Theoretical BPFI:  {frequencies['BPFI']:.2f} Hz")
    print(f"Theoretical BPFO:  {frequencies['BPFO']:.2f} Hz")
    print(f"Theoretical BSF:   {frequencies['BSF']:.2f} Hz")
    print(f"Theoretical FTF:   {frequencies['FTF']:.2f} Hz")
    print(f"Theoretical 2xBSF: {frequencies['2xBSF']:.2f} Hz")