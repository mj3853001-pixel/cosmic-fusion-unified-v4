#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../structural_core'))
from quantum_observer_lab import QuantumObserverLab

class TestQuantumObserver(unittest.TestCase):
    def setUp(self):
        self.lab = QuantumObserverLab(dimensions=2)

    def test_initial_state(self):
        self.assertEqual(len(self.lab.psi), 2)
        self.assertAlmostEqual(abs(self.lab.psi[0]), 1.0, places=5)

    def test_apply_noise(self):
        self.lab.apply_noise(0.1)
        self.assertNotAlmostEqual(abs(self.lab.psi[0]), 1.0, places=5)

    def test_measure_copenhagen(self):
        outcome = self.lab.measure("spin")
        self.assertIn(outcome, [0, 1])
        self.assertEqual(self.lab.measurement_history[-1]["interpretation"], "copenhagen")

    def test_state(self):
        state = self.lab.to_cosmic_state()
        self.assertIn("mode", state)
        self.assertIn("coherence", state)

if __name__ == '__main__':
    unittest.main()
