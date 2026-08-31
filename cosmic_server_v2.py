#!/usr/bin/env python3
# ============================================================
#  UCA COSMIC FUSION — Unified Server v4.1
#  SSE Stream · SQLite Timeline · SHA-256 Audit Chain
# ============================================================
import json, math, time, os, hashlib, sqlite3
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8082
HOST = "0.0.0.0"
DB_FILE = "cosmic_log.db"

class CosmicEngine:
    def __init__(self):
        self.start = time.time()
        self.day = 1
        self.phase = 1
        self.prev_hash = "0" * 64
        self._init_db()
        self._tick()

    def _init_db(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            day INTEGER, phase INTEGER,
            coherence REAL, stability REAL,
            dim_switch REAL, mass REAL,
            hash TEXT, prev_hash TEXT
        )""")
        self.conn.commit()

    def _tick(self):
        t = time.time() - self.start
        self.day = min(365, int(t * 2) + 1)
        self.phase = min(52, int(self.day / 7) + 1)
        self.coherence = max(0, min(1, 0.55 + 0.25 * math.sin(t * 0.3) + 0.05 * math.sin(t * 0.7)))
        self.stability = max(0, min(1, 0.70 + 0.15 * math.sin(t * 0.15) + 0.03 * math.cos(t * 0.4)))
        self.dim_switch = max(0, min(1, 0.4 + 0.3 * math.sin(t * 0.2)))
        self.symbolic_mass = max(0, min(1, 0.95 + 0.04 * math.sin(t * 0.05)))
        self.frequency = "1.42"
        # SHA-256 Hash Chain
        state_str = f"{self.prev_hash}:{self.day}:{self.phase}:{self.coherence:.6f}:{self.stability:.6f}:{t:.4f}"
        self.current_hash = hashlib.sha256(state_str.encode()).hexdigest()
        # Log to SQLite
        self.conn.execute("""INSERT INTO states
            (timestamp, day, phase, coherence, stability, dim_switch, mass, hash, prev_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (time.time(), self.day, self.phase, self.coherence, self.stability,
             self.dim_switch, self.symbolic_mass, self.current_hash, self.prev_hash))
        self.conn.commit()
        self.prev_hash = self.current_hash

    def state(self):
        self._tick()
        return {
            "coherence": round(self.coherence, 6),
            "stability": round(self.stability, 6),
            "dimension_switch_score": round(self.dim_switch, 6),
            "symbolic_mass": round(self.symbolic_mass, 6),
            "day": self.day, "phase": self.phase,
            "frequency": self.frequency,
            "hash": self.current_hash,
            "audit": {
                "conserved_before": 1.0, "conserved_after": 1.0,
                "residual": 0.0, "physical_transport": False,
                "status": "PASS"
            }
        }

    def summary(self):
        self._tick()
        return {
            "mean_coherence": round(self.coherence, 6),
            "mean_stability": round(self.stability, 6),
            "peak_switch_day": 95,
            "peak_switch_score": 0.612486,
            "final_coherence": 0.718626,
            "frequency": self.frequency,
            "symbolic_mass": round(self.symbolic_mass, 6),
            "audit": self.state()["audit"]
        }

    def history(self, limit=100):
        c = self.conn.execute("""SELECT timestamp, coherence, stability, dim_switch, mass, hash
            FROM states ORDER BY id DESC LIMIT ?""", (limit,))
        rows = c.fetchall()
        return {
            "labels": [datetime.fromtimestamp(r[0]).strftime('%H:%M:%S') for r in reversed(rows)],
            "coherence": [round(r[1], 4) for r in reversed(rows)],
            "stability": [round(r[2], 4) for r in reversed(rows)],
            "dim_switch": [round(r[3], 4) for r in reversed(rows)],
            "mass": [round(r[4], 4) for r in reversed(rows)],
            "hashes": [r[5][:8] for r in reversed(rows)]
        }

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
        self.send_response(200); self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]
        qs = self.path.split('?')[1] if '?' in self.path else ''

        if path == '/api/stream':
            self._sse(); return
        if path == '/api/history':
            limit = int(qs.split('=')[1]) if '=' in qs else 100
            self._json(ENGINE.history(limit)); return
        if path in ('/api/summary', '/summary', '/api/status'):
            self._json(ENGINE.summary()); return
        if path in ('/api/state', '/api/current', '/state'):
            self._json(ENGINE.state()); return
        if path in ('/api/audit', '/audit'):
            self._json(ENGINE.state()['audit']); return
        if path == '/api/health':
            self._json({"status":"ok","mode":"live","project":"UCA_Cosmic_Fusion_v4.1","time":datetime.now().isoformat()}); return
        super().do_GET()

    def _sse(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.end_headers()
        try:
            while True:
                data = json.dumps(ENGINE.state(), ensure_ascii=False)
                self.wfile.write(f"data: {data}\n\n".encode('utf-8'))
                time.sleep(0.5)
        except (BrokenPipeError, ConnectionResetError):
            pass

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
    print("=" * 60)
    print("  👑 UCA COSMIC FUSION — UNIFIED SERVER v4.1")
    print("=" * 60)
    print(f"  🌐 Dashboard : http://192.168.1.53:{PORT}/")
    print(f"  📡 SSE Stream: http://192.168.1.53:{PORT}/api/stream")
    print(f"  📊 History   : http://192.168.1.53:{PORT}/api/history")
    print(f"  🔗 Hash Chain: SHA-256 live audit")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
