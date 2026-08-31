#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'structural_core'))
from hydrogen_line_receiver import HydrogenLineReceiver

class TestHydrogenLineReceiver(unittest.TestCase):
    def setUp(self):
        self.rx = HydrogenLineReceiver()
        
    def test_frequency_accuracy(self):
        self.assertAlmostEqual(self.rx.FREQUENCY_HYDROGEN, 1.420405751, places=9)
        print("  [✓] Hydrogen Line Frequency — PASS")
        
    def test_capture_generates_samples(self):
        samples = self.rx.capture_signal(duration_sec=0.1)
        self.assertGreater(len(samples), 0)
        print("  [✓] Signal Capture — PASS")
        
    def test_spectrum_analysis(self):
        samples = self.rx.capture_signal(duration_sec=0.1)
        result = self.rx.analyze_spectrum(samples)
        self.assertIn("peak_power_db", result)
        self.assertIn("snr_db", result)
        print(f"  [✓] Spectrum Analysis — PASS (SNR: {result['snr_db']:.2f} dB)")
        
    def test_cosmic_state_output(self):
        samples = self.rx.capture_signal(duration_sec=0.1)
        self.rx.analyze_spectrum(samples)
        state = self.rx.to_cosmic_state()
        self.assertIn("coherence", state)
        self.assertIn("frequency", state)
        self.assertEqual(state["mode"], "hydrogen_observation")
        print("  [✓] UCA Cosmic State Conversion — PASS")

if __name__ == '__main__':
    unittest.main(verbosity=2)
