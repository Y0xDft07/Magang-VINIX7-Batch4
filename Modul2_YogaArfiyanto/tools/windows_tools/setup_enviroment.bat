@echo off
title Setup Environment Tugas Modul 2
color 0B

echo ===================================================
echo        SETUP ENVIRONMENT - TUGAS MODUL 2
echo ===================================================
echo.

:: Mendapatkan direktori project
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%..\.."
echo Project Directory: %PROJECT_DIR%
echo.

:: Buat struktur folder (dengan results/, bukan attacks/)
echo [ℹ] Membuat struktur folder...

mkdir "%PROJECT_DIR%\docs" 2>nul
mkdir "%PROJECT_DIR%\tools\cain_abel" 2>nul
mkdir "%PROJECT_DIR%\wordlists" 2>nul
mkdir "%PROJECT_DIR%\wordlists\custom" 2>nul
mkdir "%PROJECT_DIR%\hashes" 2>nul
mkdir "%PROJECT_DIR%\scripts" 2>nul
mkdir "%PROJECT_DIR%\modules" 2>nul
mkdir "%PROJECT_DIR%\results" 2>nul
mkdir "%PROJECT_DIR%\results\password_attack" 2>nul
mkdir "%PROJECT_DIR%\results\live_cracking" 2>nul
mkdir "%PROJECT_DIR%\results\sql_injection" 2>nul
mkdir "%PROJECT_DIR%\logs" 2>nul
mkdir "%PROJECT_DIR%\logs\archive" 2>nul
mkdir "%PROJECT_DIR%\screenshots" 2>nul
mkdir "%PROJECT_DIR%\screenshots\01_installation" 2>nul
mkdir "%PROJECT_DIR%\screenshots\02_password_attack" 2>nul
mkdir "%PROJECT_DIR%\screenshots\03_live_cracking" 2>nul
mkdir "%PROJECT_DIR%\screenshots\04_sql_injection" 2>nul
mkdir "%PROJECT_DIR%\backups" 2>nul

echo [✓] Struktur folder selesai dibuat!
echo.

:: Buat file hash target
echo [ℹ] Membuat file hash target...

(
echo HASH TARGET - TUGAS MODUL 2
echo ========================================
echo.
echo HASH 1 (SHA-1^):
echo 9B19C083DF8E73507433F0862CCAAB803582BE52
echo.
echo HASH 2 (SHA-512^):
echo 4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093
echo 565327D8754E4390F276B06B8EC4EB3931ED9
echo.
echo HASH 3 (SHA-256^):
echo 4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD
echo 4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF69
echo 57BE213A2E
) > "%PROJECT_DIR%\hashes\hash_target.txt"

:: Buat file hash individual
echo 9B19C083DF8E73507433F0862CCAAB803582BE52 > "%PROJECT_DIR%\hashes\hash_sha1.txt"
echo 4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E > "%PROJECT_DIR%\hashes\hash_sha256.txt"
echo 4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9 > "%PROJECT_DIR%\hashes\hash_sha512.txt"

echo [✓] File hash target dibuat!
dir "%PROJECT_DIR%\hashes\*.txt"
echo.

:: Buat panduan Cain & Abel
echo [ℹ] Membuat panduan Cain & Abel...

(
echo CAIN ^& ABEL - PANDUAN INSTALASI
echo ========================================
echo.
echo 📥 LINK DOWNLOAD:
echo ----------------------------------------
echo 1. Cain ^& Abel: https://josh.rootbrain.com/cain/ca_setup.exe
echo 2. WinPcap: https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe
echo.
echo 📁 SIMPAN DI:
echo %PROJECT_DIR%\tools\cain_abel\
echo.
echo 📌 CARA INSTALASI:
echo ----------------------------------------
echo 1. Download kedua file di atas
echo 2. Jalankan WinPcap_4_1_3.exe sebagai Administrator
echo 3. Jalankan ca_setup.exe sebagai Administrator
echo 4. Restart komputer jika diperlukan
echo.
echo ⚠️ CATATAN:
echo ----------------------------------------
echo - Jalankan installer sebagai Administrator
echo - Cain ^& Abel hanya berjalan di Windows
echo - WinPcap diperlukan untuk network capture
) > "%PROJECT_DIR%\tools\cain_abel\README.txt"

echo [✓] Panduan Cain & Abel dibuat!
echo.

:: Buat file README sederhana
echo [ℹ] Membuat README...

(
echo # TUGAS MODUL 2 - CYBER SECURITY
echo.
echo ## Yoga Arfiyanto
echo.
echo ### Struktur Folder:
echo - 📁 docs/ : Dokumentasi tugas
echo - 📁 tools/ : Tools pendukung
echo - 📁 wordlists/ : Daftar kata untuk cracking
echo - 📁 hashes/ : File hash target
echo - 📁 scripts/ : Script otomatisasi
echo - 📁 modules/ : Modul pendukung
echo - 📁 results/ : Hasil serangan
echo - 📁 logs/ : Log file
echo - 📁 screenshots/ : Dokumentasi gambar
echo - 📁 backups/ : Backup hasil
echo.
echo ### Cara Menjalankan:
echo 1. Install Python 3.8+ dari python.org
echo 2. Install dependencies: pip install -r requirements.txt
echo 3. Jalankan: cd scripts ^&^& python 05_master_controller.py
echo.
echo ### Download Wordlists:
echo Jalankan: python tools\install_all.py
echo.
echo ### Cain ^& Abel:
echo Download manual dari panduan di tools\cain_abel\README.txt
) > "%PROJECT_DIR%\README.md"

echo [✓] README.md dibuat!
echo.

echo [✓] Environment setup selesai!
echo.
echo Ringkasan folder yang dibuat:
dir "%PROJECT_DIR%" /AD /B
echo.
echo Langkah selanjutnya:
echo 1. Jalankan install_python.bat untuk install Python packages
echo 2. Jalankan install_tools.ps1 (sebagai Administrator) untuk setup lengkap
echo 3. Atau jalankan python tools\install_all.py
echo.
pause