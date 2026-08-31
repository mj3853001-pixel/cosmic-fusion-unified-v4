#!/usr/bin/env python3
import unittest, math, time, sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cosmic_server_v2 import CosmicEngine

class TestInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = CosmicEngine()
        cls.engine.start = time.time()
        print("\n[⚡] Running invariant stress test...")

    def test_01_finite_bounds(self):
        for i in range(1000):
            self.engine._tick()
            self.assertGreaterEqual(self.engine.coherence, 0)
            self.assertLessEqual(self.engine.coherence, 1)
            self.assertGreaterEqual(self.engine.stability, 0)
            self.assertLessEqual(self.engine.stability, 1)
            self.assertGreaterEqual(self.engine.dim_switch, 0)
            self.assertLessEqual(self.engine.dim_switch, 1)
            self.assertGreaterEqual(self.engine.symbolic_mass, 0)
            self.assertLessEqual(self.engine.symbolic_mass, 1)
        print("  [✓] Finite Bounds — PASS")

    def test_02_phase_domain(self):
        for _ in range(1000):
            self.engine._tick()
            self.assertGreaterEqual(self.engine.phase, 1)
            self.assertLessEqual(self.engine.phase, 52)
        print("  [✓] Phase Domain — PASS")

    def test_03_day_domain(self):
        for _ in range(1000):
            self.engine._tick()
            self.assertGreaterEqual(self.engine.day, 1)
            self.assertLessEqual(self.engine.day, 365)
        print("  [✓] Day Domain — PASS")

    def test_04_determinism_smoothness(self):
        self.engine._tick()
        prev_coh, prev_stab = self.engine.coherence, self.engine.stability
        for _ in range(500):
            self.engine._tick()
            self.assertLess(abs(self.engine.coherence - prev_coh), 0.20)
            self.assertLess(abs(self.engine.stability - prev_stab), 0.20)
            prev_coh, prev_stab = self.engine.coherence, self.engine.stability
        print("  [✓] Determinism / Smoothness — PASS")

    def test_05_conservation_mass(self):
        total = 0
        for _ in range(1000):
            self.engine._tick()
            total += self.engine.symbolic_mass
        avg = total / 1000
        self.assertAlmostEqual(avg, 0.95, delta=0.05)
        print("  [✓] Conservation of Symbolic Mass — PASS")

    def test_06_hash_chain_integrity(self):
        hashes = []
        for _ in range(200):
            self.engine._tick()
            hashes.append(self.engine.current_hash)
            self.assertEqual(len(self.engine.current_hash), 64)
        self.assertEqual(len(set(hashes)), len(hashes))
        print("  [✓] Hash Chain Integrity — PASS")

    def test_07_no_silent_transport(self):
        for _ in range(500):
            self.engine._tick()
            state = self.engine.state()
            self.assertFalse(state['audit']['physical_transport'])
            self.assertEqual(state['audit']['status'], 'PASS')
            self.assertAlmostEqual(state['audit']['residual'], 0.0, places=6)
        print("  [✓] No Silent Transport — PASS")

    def test_08_coherence_stability_tension(self):
        for _ in range(10):
            self.engine._tick()
        prev_c, prev_s = self.engine.coherence, self.engine.stability
        rises_together = 0
        falls_together = 0
        for _ in range(2000):
            self.engine._tick()
            if self.engine.coherence > prev_c and self.engine.stability > prev_s:
                rises_together += 1
            if self.engine.coherence < prev_c and self.engine.stability < prev_s:
                falls_together += 1
            prev_c, prev_s = self.engine.coherence, self.engine.stability
        together_rate = (rises_together + falls_together) / 2000
        self.assertLess(together_rate, 0.90, f"Too correlated: {together_rate:.2f}")
        self.assertGreater(together_rate, 0.20, f"Too anti-correlated: {together_rate:.2f}")
        print(f"  [✓] Cosmic Tension — PASS (correlation: {together_rate:.2f})")

if __name__ == '__main__':
    unittest.main(verbosity=2)
