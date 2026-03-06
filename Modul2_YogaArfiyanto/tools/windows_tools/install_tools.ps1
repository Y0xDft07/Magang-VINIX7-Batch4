# ===================================================
# INSTALLASI TOOLS KEAMANAN SIBER - WINDOWS
# Untuk Tugas Modul 2 Cyber Security
# Author: Yoga Arfiyanto
# ===================================================

# PowerShell script untuk install tools di Windows

# Mendapatkan direktori project
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptDir = Split-Path $ScriptPath -Parent
$ProjectDir = Resolve-Path "$ScriptDir\..\.."

# Warna untuk output
$Host.UI.RawUI.ForegroundColor = "Cyan"
Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║         AUTO INSTALLER - TOOLS KEAMANAN SIBER                ║
║              Tugas Modul 2 - Cyber Security                  ║
║                  Yoga Arfiyanto                               ║
╚══════════════════════════════════════════════════════════════╝
"@
$Host.UI.RawUI.ForegroundColor = "White"
Write-Host "Project Directory: $ProjectDir" -ForegroundColor Yellow
Write-Host ""

# Fungsi untuk print dengan warna
function Write-Color($text, $color) {
    $Host.UI.RawUI.ForegroundColor = $color
    Write-Host $text
    $Host.UI.RawUI.ForegroundColor = "White"
}

function Write-Success($text) {
    Write-Color "[✓] $text" -color "Green"
}

function Write-Info($text) {
    Write-Color "[ℹ] $text" -color "Blue"
}

function Write-Warning($text) {
    Write-Color "[⚠] $text" -color "Yellow"
}

function Write-Error($text) {
    Write-Color "[✗] $text" -color "Red"
}

function Write-Section($text) {
    Write-Host ""
    Write-Color ("=" * 60) -color "Cyan"
    Write-Color "  $text" -color "Cyan"
    Write-Color ("=" * 60) -color "Cyan"
}

# Fungsi untuk cek admin rights
function Test-AdminRights {
    $identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object System.Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Fungsi untuk install Chocolatey
function Install-Chocolatey {
    Write-Info "Menginstall Chocolatey (Package Manager)..."
    
    if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        if (Get-Command choco -ErrorAction SilentlyContinue) {
            Write-Success "Chocolatey installed"
        } else {
            Write-Error "Failed to install Chocolatey"
        }
    } else {
        Write-Success "Chocolatey already installed"
    }
}

# Fungsi untuk install Python
function Install-Python {
    Write-Info "Menginstall Python..."
    
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        choco install python -y
        refreshenv
        
        if (Get-Command python -ErrorAction SilentlyContinue) {
            Write-Success "Python installed"
            python --version
        } else {
            Write-Error "Failed to install Python"
        }
    } else {
        Write-Success "Python already installed"
        python --version
    }
}

# Fungsi untuk install Git
function Install-Git {
    Write-Info "Menginstall Git..."
    
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        choco install git -y
        refreshenv
        
        if (Get-Command git -ErrorAction SilentlyContinue) {
            Write-Success "Git installed"
        } else {
            Write-Error "Failed to install Git"
        }
    } else {
        Write-Success "Git already installed"
    }
}

# Fungsi untuk install WSL (Windows Subsystem for Linux)
function Install-WSL {
    Write-Info "Menginstall WSL (Windows Subsystem for Linux)..."
    
    # Cek apakah WSL sudah terinstall
    if (-not (Get-Command wsl -ErrorAction SilentlyContinue)) {
        dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
        dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
        
        Write-Warning "WSL diinstall. Silakan restart komputer setelah instalasi selesai."
        Write-Warning "Setelah restart, jalankan: wsl --install -d Ubuntu"
    } else {
        Write-Success "WSL already installed"
    }
}

# Fungsi untuk install tools Windows
function Install-WindowsTools {
    Write-Info "Menginstall tools Windows..."
    
    $tools = @(
        "wget",
        "curl",
        "7zip",
        "notepadplusplus",
        "vscode",
        "googlechrome",
        "firefox",
        "wireshark",
        "nmap",
        "putty"
    )
    
    foreach ($tool in $tools) {
        Write-Info "Installing $tool..."
        choco install $tool -y
        if ($?) {
            Write-Success "$tool installed"
        } else {
            Write-Warning "Failed to install $tool"
        }
    }
}

# Fungsi untuk install Python packages
function Install-PythonPackages {
    Write-Section "INSTALL PYTHON PACKAGES"
    
    $packages = @(
        "requests",
        "beautifulsoup4",
        "colorama",
        "mechanize",
        "selenium",
        "pycryptodome",
        "passlib",
        "python-nmap",
        "paramiko",
        "scapy",
        "pandas",
        "matplotlib",
        "tabulate",
        "tqdm",
        "pyyaml",
        "markdown",
        "weasyprint"
    )
    
    # Upgrade pip dulu
    Write-Info "Upgrading pip..."
    python -m pip install --upgrade pip
    
    foreach ($package in $packages) {
        Write-Info "Installing $package..."
        pip install $package --quiet
        if ($?) {
            Write-Success "$package installed"
        } else {
            Write-Error "Failed to install $package"
        }
    }
}

# Fungsi untuk download Cain & Abel (manual download - hanya panduan)
function Show-CainAbelGuide {
    Write-Section "CAIN & ABEL - PANDUAN DOWNLOAD"
    
    Write-Warning "Cain & Abel tidak didownload otomatis karena ukuran file besar (~20 MB)"
    Write-Host ""
    Write-Host "📥 LINK DOWNLOAD:" -ForegroundColor Yellow
    Write-Host "  1. Cain & Abel: https://josh.rootbrain.com/cain/ca_setup.exe"
    Write-Host "  2. WinPcap: https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe"
    Write-Host ""
    Write-Host "📁 SIMPAN DI:" -ForegroundColor Yellow
    Write-Host "  $ProjectDir\tools\cain_abel\"
    Write-Host ""
    Write-Host "📌 CARA INSTALASI:" -ForegroundColor Yellow
    Write-Host "  1. Download kedua file di atas"
    Write-Host "  2. Jalankan WinPcap_4_1_3.exe sebagai Administrator"
    Write-Host "  3. Jalankan ca_setup.exe sebagai Administrator"
    Write-Host "  4. Restart komputer jika diperlukan"
    Write-Host ""
    
    # Buat folder jika belum ada
    New-Item -ItemType Directory -Force -Path "$ProjectDir\tools\cain_abel" | Out-Null
    
    # Buat README
    $readmeContent = @"
CAIN & ABEL - PANDUAN INSTALASI
========================================

📥 LINK DOWNLOAD:
----------------------------------------------------------------
1. Cain & Abel v4.9.56
   URL: https://josh.rootbrain.com/cain/ca_setup.exe

2. WinPcap 4.1.3
   URL: https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe

📌 CARA INSTALASI:
----------------------------------------------------------------
1. Download kedua file di atas
2. Simpan di folder: tools\cain_abel\
3. Jalankan WinPcap_4_1_3.exe (install sebagai Administrator)
4. Jalankan ca_setup.exe (install sebagai Administrator)
5. Restart komputer jika diperlukan

⚠️ CATATAN:
----------------------------------------------------------------
- Jalankan installer sebagai Administrator
- Cain & Abel hanya berjalan di Windows
- WinPcap diperlukan untuk network capture

---
© 2024 Yoga Arfiyanto - Tugas Modul 2 Cyber Security
"@
    
    Set-Content -Path "$ProjectDir\tools\cain_abel\README.txt" -Value $readmeContent
    Write-Success "Panduan dibuat di tools\cain_abel\README.txt"
}

# Fungsi untuk download wordlists
function Download-Wordlists {
    Write-Section "DOWNLOAD WORDLISTS"
    
    # Buat direktori wordlists
    New-Item -ItemType Directory -Force -Path "$ProjectDir\wordlists" | Out-Null
    Set-Location "$ProjectDir\wordlists"
    
    # Download Indonesian wordlist
    Write-Info "Downloading Indonesian wordlist..."
    try {
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mychaelgo/indonesia-wordlist/master/indonesian.txt" -OutFile "indonesian.txt"
        $lines = (Get-Content "indonesian.txt").Count
        $size = (Get-Item "indonesian.txt").Length
        Write-Success "Indonesian wordlist downloaded ($lines lines, $($size/1MB) MB)"
    } catch {
        Write-Error "Failed to download Indonesian wordlist"
    }
    
    # Download target wordlists
    Write-Info "Downloading target wordlists..."
    try {
        Invoke-WebRequest -Uri "https://target.rootbrain.com/web101/username.txt" -OutFile "username.txt"
        $lines = (Get-Content "username.txt").Count
        Write-Success "Username list downloaded ($lines entries)"
    } catch {
        Write-Error "Failed to download username list"
    }
    
    try {
        Invoke-WebRequest -Uri "https://target.rootbrain.com/web101/passwords.txt" -OutFile "passwords.txt"
        $lines = (Get-Content "passwords.txt").Count
        Write-Success "Password list downloaded ($lines entries)"
    } catch {
        Write-Error "Failed to download password list"
    }
    
    # Download common wordlists
    Write-Info "Downloading common wordlists..."
    try {
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt" -OutFile "common_passwords.txt"
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt" -OutFile "common_usernames.txt"
        Write-Success "Common wordlists downloaded"
    } catch {
        Write-Error "Failed to download common wordlists"
    }
    
    Set-Location "$ProjectDir\scripts"
}

# Fungsi untuk setup environment dengan struktur folder baru (results/, bukan attacks/)
function Setup-Environment {
    Write-Section "SETUP ENVIRONMENT"
    
    # Buat direktori yang diperlukan (struktur baru dengan results)
    $dirs = @(
        "docs",
        "tools\cain_abel",
        "wordlists\custom",
        "hashes",
        "scripts",
        "modules",
        "results",
        "results\password_attack",
        "results\live_cracking",
        "results\sql_injection",
        "logs",
        "logs\archive",
        "screenshots",
        "screenshots\01_installation",
        "screenshots\02_password_attack",
        "screenshots\03_live_cracking",
        "screenshots\04_sql_injection",
        "backups"
    )
    
    foreach ($dir in $dirs) {
        $fullPath = Join-Path $ProjectDir $dir
        New-Item -ItemType Directory -Force -Path $fullPath | Out-Null
        Write-Success "Created $dir"
    }
    
    # Buat file hash target
    Write-Info "Creating hash files..."
    
    $hashTarget = @"
HASH TARGET - TUGAS MODUL 2
========================================

HASH 1 (SHA-1):
9B19C083DF8E73507433F0862CCAAB803582BE52

HASH 2 (SHA-512):
4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093
565327D8754E4390F276B06B8EC4EB3931ED9

HASH 3 (SHA-256):
4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD
4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF69
57BE213A2E
"@
    
    Set-Content -Path "$ProjectDir\hashes\hash_target.txt" -Value $hashTarget
    Set-Content -Path "$ProjectDir\hashes\hash_sha1.txt" -Value "9B19C083DF8E73507433F0862CCAAB803582BE52"
    Set-Content -Path "$ProjectDir\hashes\hash_sha256.txt" -Value "4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E"
    Set-Content -Path "$ProjectDir\hashes\hash_sha512.txt" -Value "4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9"
    
    Write-Success "Hash files created"
}

# Fungsi untuk verifikasi instalasi
function Verify-Installation {
    Write-Section "VERIFIKASI INSTALASI"
    
    Write-Color "`n🔍 Python:" -color "Cyan"
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $version = python --version 2>&1
        Write-Success $version
    } else {
        Write-Error "Python not found"
    }
    
    Write-Color "`n📦 Python Packages:" -color "Cyan"
    $packages = @("requests", "beautifulsoup4", "colorama", "markdown", "weasyprint")
    foreach ($pkg in $packages) {
        $result = pip show $pkg 2>$null
        if ($result) {
            $version = ($result | Select-String "Version:").ToString().Replace("Version:", "").Trim()
            Write-Success "$pkg $version"
        } else {
            Write-Error "$pkg not installed"
        }
    }
    
    Write-Color "`n📁 Wordlists:" -color "Cyan"
    $wordlists = @("indonesian.txt", "username.txt", "passwords.txt", "common_passwords.txt")
    foreach ($wl in $wordlists) {
        $path = "$ProjectDir\wordlists\$wl"
        if (Test-Path $path) {
            $size = (Get-Item $path).Length
            $lines = (Get-Content $path).Count
            Write-Success "$wl - $lines lines, $([math]::Round($size/1KB, 2)) KB"
        } else {
            Write-Error "$wl not found"
        }
    }
    
    Write-Color "`n📂 Folder Structure:" -color "Cyan"
    $folders = @("docs", "hashes", "scripts", "modules", "results", "logs", "screenshots", "backups")
    foreach ($folder in $folders) {
        $path = "$ProjectDir\$folder"
        if (Test-Path $path) {
            Write-Success "$folder/ exists"
        } else {
            Write-Error "$folder/ not found"
        }
    }
    
    Write-Color "`n🛠️  Cain & Abel:" -color "Cyan"
    $cainPath = "$ProjectDir\tools\cain_abel"
    if (Test-Path "$cainPath\ca_setup.exe") {
        $size = (Get-Item "$cainPath\ca_setup.exe").Length
        Write-Success "ca_setup.exe found ($([math]::Round($size/1MB, 2)) MB)"
    } else {
        Write-Warning "ca_setup.exe not found (download manually)"
    }
    
    if (Test-Path "$cainPath\WinPcap_4_1_3.exe") {
        $size = (Get-Item "$cainPath\WinPcap_4_1_3.exe").Length
        Write-Success "WinPcap_4_1_3.exe found ($([math]::Round($size/1MB, 2)) MB)"
    } else {
        Write-Warning "WinPcap_4_1_3.exe not found (download manually)"
    }
}

# Fungsi untuk show menu
function Show-Menu {
    $Host.UI.RawUI.ForegroundColor = "Cyan"
    Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║                      MENU INSTALASI                          ║
╠══════════════════════════════════════════════════════════════╣
║  1) Install Semua Tools (Lengkap)                            ║
║  2) Install Python + Packages                                ║
║  3) Download Wordlists Only                                  ║
║  4) Panduan Cain & Abel                                      ║
║  5) Setup Environment Only                                    ║
║  6) Install WSL (Untuk Linux Tools)                          ║
║  7) Verifikasi Instalasi                                      ║
║  8) Exit                                                      ║
╚══════════════════════════════════════════════════════════════╝
"@
    $Host.UI.RawUI.ForegroundColor = "White"
    
    $choice = Read-Host "`nPilihan [1-8]"
    
    switch ($choice) {
        "1" {
            Write-Section "INSTALASI LENGKAP"
            if (-not (Test-AdminRights)) {
                Write-Error "Jalankan PowerShell sebagai Administrator!"
                return
            }
            Install-Chocolatey
            Install-Python
            Install-Git
            Install-WindowsTools
            Install-PythonPackages
            Show-CainAbelGuide
            Download-Wordlists
            Setup-Environment
            Verify-Installation
        }
        "2" {
            Write-Section "INSTALASI PYTHON + PACKAGES"
            Install-Python
            Install-PythonPackages
        }
        "3" {
            Write-Section "DOWNLOAD WORDLISTS"
            Download-Wordlists
        }
        "4" {
            Write-Section "PANDUAN CAIN & ABEL"
            Show-CainAbelGuide
        }
        "5" {
            Write-Section "SETUP ENVIRONMENT"
            Setup-Environment
        }
        "6" {
            Write-Section "INSTALL WSL"
            Install-WSL
        }
        "7" {
            Write-Section "VERIFIKASI INSTALASI"
            Verify-Installation
        }
        "8" {
            Write-Info "Keluar..."
            exit
        }
        default {
            Write-Error "Pilihan tidak valid!"
        }
    }
    
    Write-Host "`n"
    pause
    Show-Menu
}

# Main program
Write-Section "WINDOWS INSTALLER - MODUL 2"
Write-Info "Project Directory: $ProjectDir"

if (-not (Test-AdminRights)) {
    Write-Warning "Beberapa fitur memerlukan Administrator rights!"
    Write-Warning "Disarankan: Close PowerShell dan jalankan sebagai Administrator"
    $continue = Read-Host "`nTetap lanjutkan? (y/n)"
    if ($continue -ne "y") { exit }
}

Show-Menu
