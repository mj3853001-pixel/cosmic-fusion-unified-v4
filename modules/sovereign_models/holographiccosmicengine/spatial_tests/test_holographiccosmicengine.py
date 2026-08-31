#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'structural_core'))
from holographic_engine import HolographicEngine
import numpy as np

class TestHolographicEngine(unittest.TestCase):
    def setUp(self):
        self.engine = HolographicEngine(boundary_nodes=64)
        
    def test_initialization(self):
        self.assertEqual(self.engine.nodes, 64)
        self.assertGreater(self.engine.entropy_bound, 0)
        print("  [✓] Holographic Init — PASS")
        
    def test_entropy_bound_positive(self):
        self.assertGreater(self.engine.entropy_bound, 0)
        print(f"  [✓] Entropy Bound — PASS ({self.engine.entropy_bound:.2e})")
        
    def test_bulk_boundary_projection(self):
        bulk = np.sin(np.linspace(0, 2*np.pi, 64))
        boundary = self.engine.encode_bulk_to_boundary(bulk)
        self.assertEqual(len(boundary), 64)
        print("  [✓] Bulk→Boundary Projection — PASS")
        
    def test_holographic_principle(self):
        result = self.engine.verify_holographic_principle()
        self.assertIn("principle_satisfied", result)
        self.assertIn("boundary_entropy", result)
        print(f"  [✓] Holographic Principle — PASS (satisfied: {result['principle_satisfied']})")
        
    def test_cosmic_state(self):
        state = self.engine.to_cosmic_state()
        self.assertEqual(state["mode"], "holographic_ads_cft")
        self.assertGreaterEqual(state["coherence"], 0)
        print("  [✓] UCA State Conversion — PASS")

if __name__ == '__main__':
    unittest.main(verbosity=2)
