import unittest

import numpy as np

from src.envelope_analysis import best_band


class TestBestBand(unittest.TestCase):
    def test_selects_full_width_band_below_nyquist(self):
        freqs = np.array([1000.0, 5000.0, 5700.0])
        kurt = np.array([1.0, 2.0, 3.0])

        low, high, center = best_band(freqs, kurt, fs=12000)

        self.assertAlmostEqual(center, 5000.0)
        self.assertAlmostEqual(high - low, 1000.0)
        self.assertLessEqual(high, 5700.0)

    def test_rejects_an_impossible_band(self):
        freqs = np.array([5000.0])
        kurt = np.array([1.0])

        with self.assertRaises(ValueError):
            best_band(freqs, kurt, fs=12000, min_freq=5500, bandwidth=1000)


if __name__ == "__main__":
    unittest.main()