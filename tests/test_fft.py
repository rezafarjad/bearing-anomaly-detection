import unittest

import numpy as np

from src.plot_fft import compute_fft


class TestFFT(unittest.TestCase):
    def test_detects_known_sine_frequency_and_amplitude(self):
        sampling_rate = 12000
        expected_frequency = 160
        time = np.arange(sampling_rate) / sampling_rate
        signal = np.sin(2 * np.pi * expected_frequency * time)

        frequencies, spectrum = compute_fft(signal, sampling_rate)
        peak_index = np.argmax(spectrum)

        self.assertAlmostEqual(
            frequencies[peak_index],
            expected_frequency,
            places=2,
        )
        self.assertAlmostEqual(spectrum[peak_index], 1.0, places=3)

    def test_removes_constant_dc_offset(self):
        signal = np.full(12000, 5.0)

        _, spectrum = compute_fft(signal, sampling_rate=12000)

        self.assertTrue(np.allclose(spectrum, 0.0, atol=1e-12))


if __name__ == "__main__":
    unittest.main()
