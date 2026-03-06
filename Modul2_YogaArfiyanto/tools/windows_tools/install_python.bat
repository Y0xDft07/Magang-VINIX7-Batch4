@echo off
title Install Python untuk Tugas Modul 2
color 0A

echo ===================================================
echo        INSTALL PYTHON - TUGAS MODUL 2
echo ===================================================
echo.

:: Mendapatkan direktori script
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%..\.."

:: Cek apakah Python sudah terinstall
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] Python sudah terinstall:
    python --version
    goto :install_packages
)

echo [ℹ] Python belum terinstall
echo [ℹ] Download Python dari https://www.python.org/downloads/
echo [ℹ] Install dengan centang "Add Python to PATH"
echo.
echo Setelah install, jalankan script ini lagi
pause
exit /b

:install_packages
echo.
echo [ℹ] Menginstall Python packages...
echo.

:: Upgrade pip dulu
python -m pip install --upgrade pip

:: Install packages dasar
echo [ℹ] Menginstall packages untuk tugas...
pip install requests
pip install beautifulsoup4
pip install colorama
pip install mechanize
pip install selenium
pip install pycryptodome
pip install passlib
pip install pandas
pip install matplotlib
pip install tabulate
pip install tqdm
pip install pyyaml
pip install markdown
pip install weasyprint

:: Install packages tambahan untuk network
pip install python-nmap
pip install paramiko
pip install scapy

echo.
echo [✓] Semua packages terinstall!
echo.
echo Packages yang terinstall:
pip list | findstr /i "requests beautifulsoup4 colorama pandas matplotlib markdown weasyprint"

echo.
echo [ℹ] Langkah selanjutnya:
echo 1. Jalankan install_tools.ps1 (sebagai Administrator) untuk setup lengkap
echo 2. Atau jalankan setup_environment.bat untuk membuat struktur folder
echo.
echo Tekan tombol untuk keluar...
pause >nul