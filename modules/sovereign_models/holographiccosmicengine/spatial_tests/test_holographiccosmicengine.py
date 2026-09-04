#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../structural_core'))
from holographic_engine import HolographicCosmicEngine

class TestHolographicEngine(unittest.TestCase):
    def setUp(self):
        self.engine = HolographicCosmicEngine(8)

    def test_initialization(self):
        self.assertEqual(self.engine.boundary_nodes, 8)
        self.assertEqual(len(self.engine.bulk_data), 8)

    def test_entropy_not_zero(self):
        self.engine.encode_bulk()
        self.assertNotEqual(self.engine.entropy, 0.0)

    def test_state(self):
        self.engine.encode_bulk()
        state = self.engine.to_cosmic_state()
        self.assertIn("mode", state)
        self.assertEqual(state["mode"], "holographic_projection")

if __name__ == '__main__':
    unittest.main()
