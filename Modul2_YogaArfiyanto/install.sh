#!/bin/bash

# Quick Install Script untuk Linux/macOS
# Yoga Arfiyanto

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         QUICK INSTALL - MODUL 2 CYBER SECURITY              ║"
echo "║                  Yoga Arfiyanto                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Cek Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 tidak ditemukan. Install dahulu."
    exit 1
fi

# Install dependencies dasar
echo "📦 Installing Python dependencies..."
pip3 install requests colorama tqdm

# Jalankan installer
echo ""
echo "🚀 Menjalankan integrated installer..."
python3 tools/install_all.py

# Beri executable permission
chmod +x scripts/*.py 2>/dev/null

echo ""
echo "✅ Selesai! Jalankan: cd scripts && python3 05_master_controller.py"