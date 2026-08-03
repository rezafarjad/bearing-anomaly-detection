import unittest

import numpy as np

from src.features import extract_time_features, split_into_windows


class TestFeatures(unittest.TestCase):
    def test_split_into_equal_windows(self):
        signal = np.arange(10)

        windows = split_into_windows(signal, window_size=4)

        self.assertEqual(windows.shape, (2, 4))
        np.testing.assert_array_equal(windows[0], [0, 1, 2, 3])
        np.testing.assert_array_equal(windows[1], [4, 5, 6, 7])

    def test_extract_time_features(self):
        features = extract_time_features(np.array([0.0, 0.0, 0.0, 4.0]))

        self.assertAlmostEqual(features["rms"], 2.0)
        self.assertAlmostEqual(features["crest_factor"], 2.0)
        self.assertIn("kurtosis", features)


if __name__ == "__main__":
    unittest.main()