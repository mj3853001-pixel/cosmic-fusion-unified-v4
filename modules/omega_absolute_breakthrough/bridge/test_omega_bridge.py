#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omega_bridge import NexusZeroTreeBridge

class TestOmegaBridge(unittest.TestCase):
    def setUp(self):
        self.tree = NexusZeroTreeBridge()
        
    def test_zero_heap(self):
        self.assertTrue(self.tree.enforce_zero_heap())
        print("  [✓] Zero-Heap Enforcement — PASS")
        
    def test_pulse_computation(self):
        pulse = self.tree.compute_pulse(1.0)
        expected = 1.0 * 0.6065306597  # e^(-0.5)
        self.assertAlmostEqual(pulse, expected, places=5)
        print(f"  [✓] Deterministic Pulse — PASS ({pulse:.4f})")
        
    def test_thousand_threads(self):
        self.assertEqual(self.tree.braid_thousand_threads(), 1000)
        print("  [✓] Thousand Threads Braid — PASS")
        
    def test_manifestation(self):
        state = self.tree.manifest()
        self.assertEqual(state, "AbsoluteSovereignty")
        print("  [✓] Absolute Sovereignty Manifestation — PASS")
        
    def test_master_pipeline(self):
        result = self.tree.execute_master_pipeline(2.0)
        self.assertTrue(result["origin_execution"])
        self.assertTrue(result["zero_heap_enforced"])
        self.assertEqual(result["threads_braided"], 1000)
        self.assertEqual(result["sovereign_state"], "AbsoluteSovereignty")
        print("  [✓] Master Pipeline — PASS")
        
    def test_cosmic_state_conversion(self):
        cosmic = self.tree.to_cosmic_state()
        self.assertEqual(cosmic["mode"], "omega_absolutesovereignty")
        self.assertTrue(cosmic["zero_heap"])
        self.assertEqual(cosmic["threads"], 1000)
        self.assertTrue(cosmic["navier_stokes_verified"])
        print("  [✓] UCA Cosmic State Conversion — PASS")

if __name__ == '__main__':
    unittest.main(verbosity=2)
