@echo off
title Quick Install - Modul 2 Cyber Security
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║         QUICK INSTALL - MODUL 2 CYBER SECURITY              ║
echo ║                  Yoga Arfiyanto                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: Cek Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo Install Python dari https://python.org
    pause
    exit /b
)

:: Install dependencies dasar
echo [INFO] Menginstall Python dependencies...
pip install requests colorama tqdm

:: Jalankan installer
echo.
echo [INFO] Menjalankan integrated installer...
python tools\install_all.py

echo.
echo [SUKSES] Selesai!
echo Jalankan: cd scripts ^&^& python 05_master_controller.py
pause