import unittest

import numpy as np

from src.anomaly_detection import rows_to_matrix, split_train_and_evaluation_rows


class TestAnomalyDetection(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"condition": "normal", "rms": "1.0", "kurtosis": "0.0", "crest_factor": "2.0"},
            {"condition": "normal", "rms": "1.1", "kurtosis": "0.1", "crest_factor": "2.1"},
            {"condition": "inner_race_fault", "rms": "2.0", "kurtosis": "4.0", "crest_factor": "5.0"},
        ]

    def test_rows_to_matrix(self):
        matrix = rows_to_matrix(self.rows)

        self.assertEqual(matrix.shape, (3, 3))
        np.testing.assert_array_equal(matrix[0], [1.0, 0.0, 2.0])

    def test_normal_windows_are_split_for_training_and_evaluation(self):
        training_rows, evaluation_rows = split_train_and_evaluation_rows(self.rows)

        self.assertEqual(len(training_rows), 1)
        self.assertEqual(training_rows[0]["condition"], "normal")
        self.assertEqual(len(evaluation_rows), 2)
        self.assertEqual(evaluation_rows[0]["condition"], "normal")
        self.assertEqual(evaluation_rows[1]["condition"], "inner_race_fault")


if __name__ == "__main__":
    unittest.main()