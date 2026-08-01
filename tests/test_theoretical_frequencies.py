import unittest

from src.theoretical_frequencies import theoretical_frequencies


class TestTheoreticalFrequencies(unittest.TestCase):

    def test_frequencies_at_1772_rpm(self):
        frequencies = theoretical_frequencies(1772)

        self.assertAlmostEqual(frequencies["fr"], 29.53, places=2)
        self.assertAlmostEqual(frequencies["BPFI"], 159.93, places=2)
        self.assertAlmostEqual(frequencies["BPFO"], 105.87, places=2)
        self.assertAlmostEqual(frequencies["BSF"], 69.60, places=2)
        self.assertAlmostEqual(frequencies["FTF"], 11.76, places=2)
        self.assertAlmostEqual(frequencies["2xBSF"], 139.20, places=2)


if __name__ == "__main__":
    unittest.main()