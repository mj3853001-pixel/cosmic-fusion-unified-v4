#!/usr/bin/env python3
# ============================================================
#  UCA CosMIC CLI — Terminal Dashboard
#  Run: python cosmic_cli.py
# ============================================================
import json, urllib.request, time, os, sys

API_URL = "http://127.0.0.1:8083/api/cli"
REFRESH = 0.5

# ANSI Colors
C = {
    'reset': '\033[0m', 'bold': '\033[1m',
    'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m',
    'blue': '\033[94m', 'purple': '\033[95m', 'cyan': '\033[96m',
    'bg': '\033[40m', 'white': '\033[97m'
}

def bar(val, width=30):
    filled = int(val * width)
    empty = width - filled
    color = C['green'] if val > 0.7 else C['yellow'] if val > 0.4 else C['red']
    return f"{color}{'█' * filled}{C['white']}{'░' * empty}{C['reset']}"

def box(title, content):
    lines = content.split('\n')
    width = max(len(l) for l in lines) + 4
    top = f"┌{'─' * (width-2)}┐"
    mid = f"│ {C['cyan']}{title:^{width-4}}{C['reset']} │"
    bot = f"└{'─' * (width-2)}┘"
    body = '\n'.join(f"│  {l:<{width-4}} │" for l in lines)
    return f"{top}\n{mid}\n{body}\n{bot}"

def draw(data):
    os.system('clear' if os.name != 'nt' else 'cls')
    coh = data.get('coherence', 0)
    stab = data.get('stability', 0)
    dim = data.get('dimension_switch_score', 0)
    mass = data.get('symbolic_mass', 0)
    day = data.get('day', 0)
    phase = data.get('phase', 0)
    noise = data.get('noise_level', 0)
    err = data.get('reconstruction_error', 0)
    qm = data.get('quantum_mode', False)
    h = data.get('hash', '0')[:16]
    peers = len(data.get('peers', []))

    print(f"\n{C['bold']}{C['purple']}  ╔═══════════════════════════════════════════════════════════════╗")
    print(f"  ║   👑 UCA COSMIC FUSION — TERMINAL DASHBOARD v4.2           ║")
    print(f"  ╚═══════════════════════════════════════════════════════════════╝{C['reset']}\n")

    print(box("LIVE METRICS", f"""
Coherence    {bar(coh)}  {coh:.4f}
Stability    {bar(stab)}  {stab:.4f}
Dim-Switch   {bar(dim)}  {dim:.4f}
Symb. Mass   {bar(mass)}  {mass:.4f}
    """))

    print(box("TIMELINE", f"""
Day {day:03d} | Phase {phase:02d} | Mode: {'⚛️ QUANTUM' if qm else '🔒 DETERMINISTIC'}
Noise: {noise*100:5.1f}% | Error: {err:.4f} | Peers: {peers}
Hash: {C['yellow']}{h}...{C['reset']}
    """))

    print(f"\n  {C['green']}● LIVE{C['reset']}  |  Refresh: {REFRESH}s  |  Press Ctrl+C to exit\n")

def main():
    print("Connecting to cosmic_server_v3.py ...")
    while True:
        try:
            with urllib.request.urlopen(API_URL, timeout=2) as resp:
                data = json.loads(resp.read().decode())
                draw(data)
        except Exception as e:
            os.system('clear' if os.name != 'nt' else 'cls')
            print(f"\n{C['red']}  ⚠️  Connection lost: {e}{C['reset']}")
            print(f"  Make sure server is running: python cosmic_server_v3.py\n")
        time.sleep(REFRESH)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C['green']}  👋 Goodbye, Observer.{C['reset']}\n")
