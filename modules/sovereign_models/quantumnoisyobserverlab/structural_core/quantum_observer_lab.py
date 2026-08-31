#!/usr/bin/env python3
# ============================================================
#  QuantumNoisyObserverLab — Copenhagen vs Many-Worlds Simulation
#  Model ID: see manifest.json
#  Extends: PROJ-002 (Noisy Observer Reconstruction)
# ============================================================
import numpy as np
import random, math, json
from datetime import datetime

class QuantumObserverLab:
    """
    معمل الملاحظ الضوضائي الكمي
    يحاكي: 1) انهيار الدالة الموجية (Copenhagen)
           2) الانشقاق الكوني (Many-Worlds)
           3) حقن ضوضاء متحكم فيه (PROJ-002)
    """
    HBAR = 1.054571817e-34  # J·s
    
    def __init__(self, dimensions=2):
        self.dim = dimensions
        self.psi = np.zeros(dimensions, dtype=complex)
        self.psi[0] = 1.0  # |0⟩ initial state
        self.worlds = []   # Many-Worlds branches
        self.noise_level = 0.0
        self.interpretation = "copenhagen"
        self.measurement_history = []
        self.reconstruction_error = 0.0
        self.timestamp = datetime.now().isoformat()
        
    def set_interpretation(self, mode):
        """التبديل بين Copenhagen و Many-Worlds"""
        assert mode in ("copenhagen", "many_worlds")
        self.interpretation = mode
        
    def apply_noise(self, level):
        """PROJ-002: حقن ضوضاء كمية"""
        self.noise_level = max(0.0, min(1.0, level))
        noise = (np.random.randn(self.dim) + 1j * np.random.randn(self.dim))
        noise *= self.noise_level / np.sqrt(2)
        self.psi += noise
        self.psi /= np.linalg.norm(self.psi) + 1e-12
        self._compute_reconstruction_error()
        
    def _compute_reconstruction_error(self):
        """حساب خطأ إعادة بناء الحالة الأصلية"""
        ideal = np.zeros(self.dim, dtype=complex)
        ideal[0] = 1.0
        fidelity = np.abs(np.vdot(ideal, self.psi))**2
        self.reconstruction_error = round(float(1.0 - fidelity), 6)
        
    def measure(self, observable):
        """عملية قياس كمية"""
        if self.interpretation == "copenhagen":
            return self._measure_copenhagen(observable)
        else:
            return self._measure_many_worlds(observable)
            
    def _measure_copenhagen(self, observable):
        """انهيار الدالة الموجية لقيمة واحدة"""
        probs = np.abs(self.psi)**2
        outcome = np.random.choice(self.dim, p=probs)
        # Collapse
        self.psi = np.zeros(self.dim, dtype=complex)
        self.psi[outcome] = 1.0
        self.measurement_history.append({
            "interpretation": "copenhagen",
            "outcome": int(outcome),
            "probability": round(float(probs[outcome]), 6),
            "collapsed": True
        })
        return outcome
        
    def _measure_many_worlds(self, observable):
        """انشقاق الكون — كل النتائج تحدث في عوالم موازية"""
        probs = np.abs(self.psi)**2
        outcome = np.random.choice(self.dim, p=probs)
        # Branch: keep superposition, spawn new world
        self.worlds.append({
            "branch_id": len(self.worlds),
            "outcome": int(outcome),
            "probability": round(float(probs[outcome]), 6),
            "psi_snapshot": self.psi.copy().tolist()
        })
        self.measurement_history.append({
            "interpretation": "many_worlds",
            "outcome": int(outcome),
            "branches": len(self.worlds),
            "collapsed": False
        })
        return outcome
        
    def snr(self):
        """Signal-to-Noise Ratio"""
        signal = np.abs(self.psi[0])**2
        noise = 1.0 - signal
        return round(float(signal / (noise + 1e-12)), 2)
        
    def to_cosmic_state(self):
        """تحويل لصيغة UCA Cosmic Fusion"""
        return {
            "coherence": round(float(np.abs(self.psi[0])**2), 6),
            "stability": round(0.5 + 0.5 * (1 - self.reconstruction_error), 6),
            "symbolic_mass": round(0.9 if self.interpretation == "copenhagen" else 0.95, 6),
            "dimension_switch_score": round(len(self.worlds) / 10.0, 6),
            "frequency": "1.42",
            "mode": f"quantum_{self.interpretation}",
            "reconstruction_error": self.reconstruction_error,
            "snr": self.snr(),
            "branches": len(self.worlds)
        }

if __name__ == "__main__":
    lab = QuantumObserverLab(dimensions=4)
    print("[*] QuantumNoisyObserverLab initialized")
    print("[*] Interpretation: Copenhagen")
    lab.apply_noise(0.1)
    result = lab.measure("spin_z")
    print(f"[+] Outcome: {result}")
    print(f"[+] Reconstruction Error: {lab.reconstruction_error}")
    print(f"[+] SNR: {lab.snr()}")
    print("[*] Switching to Many-Worlds...")
    lab.set_interpretation("many_worlds")
    lab.measure("spin_z")
    print(f"[+] Branches: {len(lab.worlds)}")
    print(f"[+] Cosmic State: {json.dumps(lab.to_cosmic_state(), indent=2)}")
