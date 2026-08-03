import unittest

import numpy as np

from src.feature_dataset import build_feature_rows


class TestFeatureDataset(unittest.TestCase):
    def test_builds_one_row_per_window(self):
        signal = np.arange(8, dtype=float)

        rows = build_feature_rows(signal, "normal", window_size=4)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["condition"], "normal")
        self.assertEqual(rows[0]["window_index"], 0)
        self.assertEqual(rows[1]["window_index"], 1)
        self.assertIn("rms", rows[0])
        self.assertIn("kurtosis", rows[0])
        self.assertIn("crest_factor", rows[0])


if __name__ == "__main__":
    unittest.main()