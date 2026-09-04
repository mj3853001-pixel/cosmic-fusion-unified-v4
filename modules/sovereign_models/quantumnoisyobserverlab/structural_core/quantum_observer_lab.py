#!/usr/bin/env python3
# ============================================================
#  QuantumNoisyObserverLab - Pure Python (Zero Dependencies)
#  Model ID: see manifest.json
#  Extends: PROJ-002 (Noisy Observer Reconstruction)
# ============================================================
import random, math, cmath, json
from datetime import datetime

class QuantumObserverLab:
    """
    معمل الملاحظ الضوضائي الكمي (Pure Python)
    يحاكي: 1) انهيار الدالة الموجية (Copenhagen)
           2) الانشقاق الكوني (Many-Worlds)
           3) حقن ضوضاء متحكم فيه (PROJ-002)
    """
    HBAR = 1.054571817e-34  # J·s

    def __init__(self, dimensions=2):
        self.dim = dimensions
        self.psi = [0.0 + 0.0j] * dimensions
        self.psi[0] = 1.0 + 0.0j  # |0> initial state
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

    def _gauss(self):
        """مولدة أرقام غاوسية باستخدام random (بديل لـ np.random.randn)"""
        # Box-Muller transform
        u1 = max(random.random(), 1e-12)
        u2 = random.random()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

    def apply_noise(self, level):
        """PROJ-002: حقن ضوضاء كمية"""
        self.noise_level = max(0.0, min(1.0, level))
        noise_real = [self._gauss() for _ in range(self.dim)]
        noise_imag = [self._gauss() for _ in range(self.dim)]
        for i in range(self.dim):
            self.psi[i] += (noise_real[i] + 1j * noise_imag[i]) * (self.noise_level / math.sqrt(2))
        
        # Normalization
        norm = math.sqrt(sum(abs(x)**2 for x in self.psi)) + 1e-12
        self.psi = [x / norm for x in self.psi]
        self._compute_reconstruction_error()

    def _compute_reconstruction_error(self):
        """حساب خطأ إعادة بناء الحالة الأصلية"""
        ideal = [0.0 + 0.0j] * self.dim
        ideal[0] = 1.0 + 0.0j
        # vdot (conjugate dot product)
        fidelity = abs(sum(a.conjugate() * b for a, b in zip(ideal, self.psi)))**2
        self.reconstruction_error = round(float(1.0 - fidelity), 6)

    def measure(self, observable):
        """عملية قياس كمية"""
        if self.interpretation == "copenhagen":
            return self._measure_copenhagen(observable)
        else:
            return self._measure_many_worlds(observable)

    def _measure_copenhagen(self, observable):
        """انهيار الدالة الموجية لقيمة واحدة"""
        probs = [abs(x)**2 for x in self.psi]
        total_prob = sum(probs)
        if total_prob == 0: return 0
        probs = [p / total_prob for p in probs]
        
        # Weighted random choice (بديل لـ np.random.choice)
        r = random.random()
        cumulative = 0.0
        outcome = 0
        for i, p in enumerate(probs):
            cumulative += p
            if r <= cumulative:
                outcome = i
                break
        
        # Collapse
        self.psi = [0.0 + 0.0j] * self.dim
        self.psi[outcome] = 1.0 + 0.0j
        self.measurement_history.append({
            "interpretation": "copenhagen",
            "outcome": int(outcome),
            "probability": round(float(probs[outcome]), 6),
            "collapsed": True
        })
        return outcome

    def _measure_many_worlds(self, observable):
        """انشقاق الكون — كل النتائج تحدث في عوالم موازية"""
        probs = [abs(x)**2 for x in self.psi]
        total_prob = sum(probs)
        if total_prob == 0: return 0
        probs = [p / total_prob for p in probs]
        
        r = random.random()
        cumulative = 0.0
        outcome = 0
        for i, p in enumerate(probs):
            cumulative += p
            if r <= cumulative:
                outcome = i
                break
        
        # Branch: keep superposition, spawn new world
        self.worlds.append({
            "branch_id": len(self.worlds),
            "outcome": int(outcome),
            "probability": round(float(probs[outcome]), 6),
            "psi_snapshot": [complex(x) for x in self.psi]
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
        signal = abs(self.psi[0])**2
        noise = 1.0 - signal
        return round(float(signal / (noise + 1e-12)), 2)

    def to_cosmic_state(self):
        """تحويل لصيغة UCA Cosmic Fusion"""
        return {
            "coherence": round(float(abs(self.psi[0])**2), 6),
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
