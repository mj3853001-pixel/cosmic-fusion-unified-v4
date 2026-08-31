#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'structural_core'))
from quantum_observer_lab import QuantumObserverLab
import numpy as np

class TestQuantumObserverLab(unittest.TestCase):
    def setUp(self):
        self.lab = QuantumObserverLab(dimensions=4)
        
    def test_initial_state(self):
        self.assertAlmostEqual(abs(self.lab.psi[0]), 1.0, places=5)
        print("  [✓] Initial Quantum State — PASS")
        
    def test_copenhagen_collapse(self):
        self.lab.set_interpretation("copenhagen")
        outcome = self.lab.measure("spin_z")
        self.assertIn(outcome, [0, 1, 2, 3])
        self.assertAlmostEqual(abs(self.lab.psi[outcome]), 1.0, places=5)
        print(f"  [✓] Copenhagen Collapse — PASS (outcome: {outcome})")
        
    def test_many_worlds_branching(self):
        self.lab.set_interpretation("many_worlds")
        self.lab.measure("spin_z")
        self.lab.measure("spin_z")
        self.assertGreaterEqual(len(self.lab.worlds), 2)
        print(f"  [✓] Many-Worlds Branching — PASS ({len(self.lab.worlds)} branches)")
        
    def test_noise_injection(self):
        self.lab.apply_noise(0.2)
        self.assertGreater(self.lab.reconstruction_error, 0)
        print(f"  [✓] Noise Injection (PROJ-002) — PASS (error: {self.lab.reconstruction_error})")
        
    def test_snr_positive(self):
        snr = self.lab.snr()
        self.assertGreater(snr, 0)
        print(f"  [✓] SNR Test — PASS (SNR: {snr})")
        
    def test_cosmic_state(self):
        state = self.lab.to_cosmic_state()
        self.assertIn("mode", state)
        self.assertIn("reconstruction_error", state)
        print("  [✓] UCA State Conversion — PASS")

if __name__ == '__main__':
    unittest.main(verbosity=2)
