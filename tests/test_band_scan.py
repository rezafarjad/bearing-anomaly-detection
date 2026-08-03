import unittest

import numpy as np

from src.band_scan import candidate_bands, select_kurtosis_band


class TestBandScan(unittest.TestCase):
    def test_candidate_bands_have_valid_width_and_limits(self):
        bands = list(candidate_bands(fs=12000, widths_hz=(1000.0,)))

        self.assertEqual(bands[0], (500.0, 1500.0))

        for low_hz, high_hz in bands:
            self.assertAlmostEqual(high_hz - low_hz, 1000.0)
            self.assertGreaterEqual(low_hz, 500.0)
            self.assertLessEqual(high_hz, 5700.0)

    def test_selected_band_is_valid(self):
        rng = np.random.default_rng(42)
        signal = rng.normal(size=12000)
        signal[3000] += 10.0

        result = select_kurtosis_band(signal, fs=12000)

        self.assertGreaterEqual(result.low_hz, 500.0)
        self.assertLessEqual(result.high_hz, 5700.0)
        self.assertIn(result.high_hz - result.low_hz, (250.0, 500.0, 1000.0))


if __name__ == "__main__":
    unittest.main()