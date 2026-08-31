#!/bin/bash
# ============================================================
#  UCA Cosmic Fusion — Termux Setup Script
#  One command to rule them all.
# ============================================================

echo "=============================================="
echo "  🌌 UCA Cosmic Fusion — Termux Installer"
echo "=============================================="

# Check Python
if ! command -v python &> /dev/null; then
    echo "[+] Installing Python..."
    pkg install python -y
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo "[+] Installing Git..."
    pkg install git -y
fi

# Get IP
IP=$(ip addr show wlan0 2>/dev/null | grep "inet " | awk '{print $2}' | cut -d/ -f1)
if [ -z "$IP" ]; then
    IP="127.0.0.1"
fi

echo ""
echo "[✓] Ready to launch."
echo ""
echo "  IP detected: $IP"
echo ""
echo "  Starting server..."
echo ""

python cosmic_server.py &

sleep 2

echo ""
echo "=============================================="
echo "  🌐 Open in browser:"
echo "  http://$IP:8082/"
echo "=============================================="
echo ""
echo "  Press Enter to stop server..."
read

kill %1 2>/dev/null
echo "[✓] Server stopped."
