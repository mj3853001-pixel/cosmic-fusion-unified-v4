#!/usr/bin/env python3
# ============================================================
#  PROJ-002: Noisy Observer Reconstruction Tests
#  python -m unittest test_proj002.py -v
# ============================================================
import unittest, math, time, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cosmic_server_v3 import CosmicEngine

class TestNoisyObserver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = CosmicEngine()
        cls.engine.start = time.time()
        print("\n[⚡] PROJ-002: Noisy Observer Reconstruction Test...")

    def test_01_noise_injection_increases_error(self):
        """Higher noise must produce higher reconstruction error"""
        self.engine.set_noise(0.0)
        self.engine._tick()
        err_zero = self.engine.reconstruction_error
        
        self.engine.set_noise(0.5)
        errors = []
        for _ in range(100):
            self.engine._tick()
            errors.append(self.engine.reconstruction_error)
        avg_err = sum(errors) / len(errors)
        
        self.assertGreater(avg_err, err_zero, "Noise did not increase error")
        print(f"  [✓] Noise Injection — PASS (error: {avg_err:.4f})")

    def test_02_quantum_vs_deterministic(self):
        """Quantum mode must use different entropy source"""
        self.engine.set_quantum(False)
        self.engine.set_noise(0.1)
        self.engine._tick()
        hash_det = self.engine.current_hash
        
        self.engine.set_quantum(True)
        self.engine._tick()
        hash_qtm = self.engine.current_hash
        
        # Hashes should differ because entropy source changed
        self.assertNotEqual(hash_det, hash_qtm, "Quantum mode not affecting output")
        print("  [✓] Quantum Mode — PASS")

    def test_03_reconstruction_bounds(self):
        """Error must never exceed noise_level * 2"""
        for level in [0.1, 0.3, 0.5, 0.9]:
            self.engine.set_noise(level)
            for _ in range(50):
                self.engine._tick()
                self.assertLessEqual(self.engine.reconstruction_error, level * 2.0,
                    f"Error {self.engine.reconstruction_error} exceeded bound for noise {level}")
        print("  [✓] Reconstruction Bounds — PASS")

    def test_04_signal_to_noise_ratio(self):
        """At low noise, signal must dominate (SNR > 1)"""
        self.engine.set_noise(0.05)
        signals, noises = [], []
        for _ in range(100):
            self.engine._tick()
            signals.append(self.engine.coherence)
            noises.append(self.engine.reconstruction_error)
        avg_signal = sum(signals) / len(signals)
        avg_noise = sum(noises) / len(noises)
        snr = avg_signal / (avg_noise + 0.0001)
        self.assertGreater(snr, 1.0, f"SNR too low: {snr:.2f}")
        print(f"  [✓] SNR Test — PASS (SNR: {snr:.2f})")

if __name__ == '__main__':
    unittest.main(verbosity=2)
