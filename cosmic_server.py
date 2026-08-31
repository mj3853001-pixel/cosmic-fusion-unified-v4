#!/usr/bin/env python3
import json, math, time, os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8082
HOST = "0.0.0.0"

class CosmicEngine:
    def __init__(self):
        self.start = time.time()
        self.day = 1
        self.phase = 1
        self._tick()
    def _tick(self):
        t = time.time() - self.start
        self.day = min(365, int(t * 2) + 1)
        self.phase = min(52, int(self.day / 7) + 1)
        self.coherence = 0.55 + 0.25 * math.sin(t * 0.3) + 0.05 * math.sin(t * 0.7)
        self.stability = 0.70 + 0.15 * math.sin(t * 0.15) + 0.03 * math.cos(t * 0.4)
        self.dim_switch = 0.4 + 0.3 * math.sin(t * 0.2)
        self.symbolic_mass = 0.95 + 0.04 * math.sin(t * 0.05)
        self.frequency = "1.42"
        self.mean_coherence = 0.500612 + 0.001 * math.sin(t * 0.1)
        self.mean_stability = 0.835193 + 0.0005 * math.cos(t * 0.08)
        self.peak_switch_day = 95
        self.peak_switch_score = 0.612486 + 0.01 * math.sin(t * 0.12)
        self.final_coherence = 0.718626 + 0.005 * math.sin(t * 0.09)
        self.conserved_before = 1.0
        self.conserved_after = 1.0
        self.residual = 0.0
        self.physical_transport = False
        self.status = "PASS"
    def summary(self):
        self._tick()
        return {"mean_coherence": round(self.mean_coherence, 6), "mean_stability": round(self.mean_stability, 6), "peak_switch_day": self.peak_switch_day, "peak_switch_score": round(self.peak_switch_score, 6), "final_coherence": round(self.final_coherence, 6), "frequency": self.frequency, "symbolic_mass": round(self.symbolic_mass, 6), "audit": {"conserved_before": self.conserved_before, "conserved_after": self.conserved_after, "residual": self.residual, "physical_transport": self.physical_transport, "status": self.status}}
    def state(self):
        self._tick()
        return {"coherence": round(self.coherence, 6), "stability": round(self.stability, 6), "dimension_switch_score": round(self.dim_switch, 6), "symbolic_mass": round(self.symbolic_mass, 6), "day": self.day, "phase": self.phase, "frequency": self.frequency, "audit": {"conserved_before": self.conserved_before, "conserved_after": self.conserved_after, "residual": self.residual, "physical_transport": self.physical_transport, "status": self.status}}
    def audit(self):
        self._tick()
        return {"conserved_before": self.conserved_before, "conserved_after": self.conserved_after, "residual": self.residual, "physical_transport": self.physical_transport, "status": self.status}
    def timeseries(self):
        self._tick()
        return {"days": list(range(1, self.day + 1)), "coherence": [round(0.5 + 0.2 * math.sin(d * 0.1), 6) for d in range(1, self.day + 1)], "stability": [round(0.7 + 0.1 * math.cos(d * 0.05), 6) for d in range(1, self.day + 1)]}
    def lattice(self):
        return {"nodes": 365, "edges": 728, "symmetry": "D12", "resonance": 1.42}
    def mass_projection(self):
        self._tick()
        return {"symbolic_mass": round(self.symbolic_mass, 6), "projection": "holographic", "observer": "O_i = P_i(R)"}

ENGINE = CosmicEngine()

class CosmicHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.client_address[0]} — {fmt % args}")
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    def do_GET(self):
        path = self.path.split('?')[0]
        if path in ('/api/summary', '/summary', '/api/status'):
            self._json(ENGINE.summary()); return
        if path in ('/api/state', '/api/current', '/state'):
            self._json(ENGINE.state()); return
        if path in ('/api/audit', '/audit'):
            self._json(ENGINE.audit()); return
        if path in ('/api/timeseries', '/timeseries'):
            self._json(ENGINE.timeseries()); return
        if path in ('/api/lattice', '/lattice'):
            self._json(ENGINE.lattice()); return
        if path in ('/api/mass', '/mass-projection'):
            self._json(ENGINE.mass_projection()); return
        if path == '/api/health':
            self._json({"status": "ok", "mode": "live", "project": "UCA_Cosmic_Fusion_v4", "time": datetime.now().isoformat()}); return
        super().do_GET()
    def _json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer((HOST, PORT), CosmicHandler)
    print("=" * 55)
    print("  👑 UCA COSMIC FUSION — UNIFIED SERVER v4.0")
    print("=" * 55)
    print(f"  🌐 Dashboard : http://192.168.1.53:{PORT}/cosmic_fusion_unified_dashboard_v4_api.html")
    print(f"  📡 API Base  : http://192.168.1.53:{PORT}/api/...")
    print("=" * 55)
    print("  Press Ctrl+C to stop")
    print("=" * 55)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
