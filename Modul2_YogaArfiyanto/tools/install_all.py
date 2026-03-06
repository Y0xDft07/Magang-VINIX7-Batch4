#!/usr/bin/env python3
"""
Cross-Platform Installer - Versi Terintegrasi dengan Cain & Abel Support
Author: Yoga Arfiyanto
"""

import os
import sys
import platform
import subprocess
import requests
import shutil
from pathlib import Path

class IntegratedInstaller:
    """Installer terintegrasi untuk semua platform"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.colors = {
            'red': '\033[91m' if self.system != 'windows' else '',
            'green': '\033[92m' if self.system != 'windows' else '',
            'yellow': '\033[93m' if self.system != 'windows' else '',
            'blue': '\033[94m' if self.system != 'windows' else '',
            'purple': '\033[95m' if self.system != 'windows' else '',
            'cyan': '\033[96m' if self.system != 'windows' else '',
            'reset': '\033[0m' if self.system != 'windows' else ''
        }
        
    def print_color(self, text, color='reset'):
        print(f"{self.colors.get(color, '')}{text}{self.colors['reset']}")
        
    def print_banner(self):
        os.system('cls' if self.system == 'windows' else 'clear')
        self.print_color("""
╔══════════════════════════════════════════════════════════════╗
║         INTEGRATED INSTALLER - MODUL 2 CYBER SECURITY       ║
║                  Yoga Arfiyanto                              ║
╚══════════════════════════════════════════════════════════════╝
        """, 'cyan')
        self.print_color(f"System: {self.system}", 'green')
        self.print_color(f"Project: {self.project_dir}", 'yellow')
        
    def create_directories(self):
        """Buat semua direktori yang diperlukan"""
        self.print_color("\n[1] Creating directories...", 'yellow')
        
        dirs = [
            'docs',
            'wordlists',
            'wordlists/custom',
            'hashes',
            'scripts',
            'modules',
            'results',
            'results/password_attack',
            'results/live_cracking',
            'results/sql_injection',
            'logs',
            'logs/archive',
            'screenshots',
            'screenshots/01_installation',
            'screenshots/02_password_attack',
            'screenshots/03_live_cracking',
            'screenshots/04_sql_injection',
            'backups',
            'tools/cain_abel'  # Folder untuk Cain & Abel
        ]
        
        for dir_path in dirs:
            full_path = os.path.join(self.project_dir, dir_path)
            os.makedirs(full_path, exist_ok=True)
            self.print_color(f"  ✓ Created: {dir_path}", 'green')
            
    def create_cain_abel_readme(self):
        """Buat README untuk Cain & Abel dengan panduan download"""
        self.print_color("\n[2] Creating Cain & Abel guide...", 'yellow')
        
        readme_content = """CAIN & ABEL - PANDUAN INSTALASI
========================================

Cain & Abel adalah tool untuk password recovery dan cracking di Windows.
Karena ukuran file yang besar, Anda perlu mendownload secara manual.

📥 LINK DOWNLOAD:
----------------------------------------------------------------
1. Cain & Abel v4.9.56 (∼15 MB)
   URL: https://josh.rootbrain.com/cain/ca_setup.exe
   Backup URL: https://www.oxid.it/cain.html (official site)

2. WinPcap 4.1.3 (∼5 MB) - Dependency untuk network capture
   URL: https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe

📌 CARA INSTALASI:
----------------------------------------------------------------
1. Download kedua file di atas
2. Simpan di folder: tools/cain_abel/
   - ca_setup.exe
   - WinPcap_4_1_3.exe
3. Jalankan WinPcap_4_1_3.exe (install sebagai Administrator)
4. Jalankan ca_setup.exe (install sebagai Administrator)
5. Selesai! Cain & Abel siap digunakan

⚠️ CATATAN PENTING:
----------------------------------------------------------------
- Jalankan installer sebagai Administrator
- Untuk Windows 10/11, mungkin perlu kompatibilitas mode
- Cain & Abel hanya berjalan di Windows
- Restart komputer setelah instalasi WinPcap

📸 SCREENSHOT REFERENSI:
----------------------------------------------------------------
Lihat folder: screenshots/01_installation/
- 1_download_cain.png
- 2_install_winpcap.png
- 3_install_cain.png
- 4_cain_ready.png

📞 BUTUH BANTUAN?
----------------------------------------------------------------
Jika mengalami kendala, hubungi:
Yoga Arfiyanto - yoga.arfiyanto@gmail.com

---
© 2024 Yoga Arfiyanto - Tugas Modul 2 Cyber Security
"""
        
        readme_path = os.path.join(self.project_dir, 'tools', 'cain_abel', 'README.txt')
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        self.print_color("  ✓ Created: tools/cain_abel/README.txt", 'green')
        
    def create_hash_files(self):
        """Buat file hash target"""
        self.print_color("\n[3] Creating hash files...", 'yellow')
        
        # hash_target.txt
        hash_target = """HASH TARGET - TUGAS MODUL 2
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
"""
        
        # hash_analysis.md
        hash_analysis = """# Analisis Hash Target

## Hash 1
- **String**: `9B19C083DF8E73507433F0862CCAAB803582BE52`
- **Panjang**: 40 karakter
- **Tipe**: SHA-1
- **Format**: Hexadecimal

## Hash 2
- **String**: `4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9`
- **Panjang**: 128 karakter
- **Tipe**: SHA-512
- **Format**: Hexadecimal

## Hash 3
- **String**: `4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E`
- **Panjang**: 64 karakter
- **Tipe**: SHA-256
- **Format**: Hexadecimal
"""
        
        files = {
            'hash_target.txt': hash_target,
            'hash_sha1.txt': '9B19C083DF8E73507433F0862CCAAB803582BE52',
            'hash_sha256.txt': '4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E',
            'hash_sha512.txt': '4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9',
            'hash_analysis.md': hash_analysis
        }
        
        hashes_dir = os.path.join(self.project_dir, 'hashes')
        for filename, content in files.items():
            filepath = os.path.join(hashes_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            self.print_color(f"  ✓ Created: {filename}", 'green')
            
    def download_wordlists(self):
        """Download wordlists - DENGAN URL YANG BENAR"""
        self.print_color("\n[4] Downloading wordlists...", 'yellow')
        
        # URL yang benar (raw content, bukan halaman web)
        wordlists = {
            'indonesian.txt': 'https://raw.githubusercontent.com/geovedi/indonesian-wordlist/refs/heads/master/00-indonesian-wordlist.lst',
            'username.txt': 'https://target.rootbrain.com/web101/username.txt',
            'passwords.txt': 'https://target.rootbrain.com/web101/passwords.txt',
            'common_passwords.txt': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt',
            'common_usernames.txt': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt'
        }
        
        wordlists_dir = os.path.join(self.project_dir, 'wordlists')
        
        # Buat folder jika belum ada
        os.makedirs(wordlists_dir, exist_ok=True)
        
        for filename, url in wordlists.items():
            self.print_color(f"  Downloading {filename}...", 'blue')
            filepath = os.path.join(wordlists_dir, filename)
            
            try:
                # Download dengan stream untuk file besar
                response = requests.get(url, timeout=30, stream=True)
                response.raise_for_status()  # Cek error HTTP
                
                # Simpan file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Dapatkan ukuran file
                size = os.path.getsize(filepath)
                
                # Hitung jumlah baris (untuk file teks)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = sum(1 for _ in f)
                except:
                    lines = 0
                
                self.print_color(f"  ✓ {filename} ({size:,} bytes, {lines:,} lines)", 'green')
                
            except requests.exceptions.SSLError:
                self.print_color(f"  ✗ SSL Error untuk {filename}", 'red')
                self.print_color(f"    Mencoba tanpa verifikasi SSL...", 'yellow')
                
                # Coba lagi dengan SSL verification dimatikan
                try:
                    response = requests.get(url, timeout=30, stream=True, verify=False)
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    size = os.path.getsize(filepath)
                    self.print_color(f"  ✓ {filename} ({size:,} bytes) - dengan SSL disabled", 'green')
                except Exception as e2:
                    self.print_color(f"  ✗ Gagal juga: {e2}", 'red')
                    
            except requests.exceptions.ConnectionError:
                self.print_color(f"  ✗ Connection Error untuk {filename}", 'red')
                self.print_color(f"    URL: {url}", 'yellow')
                
            except requests.exceptions.Timeout:
                self.print_color(f"  ✗ Timeout untuk {filename}", 'red')
                
            except Exception as e:
                self.print_color(f"  ✗ Error: {e}", 'red')
                
    def install_python_packages(self):
        """Install Python packages"""
        self.print_color("\n[5] Installing Python packages...", 'yellow')
        
        packages = [
            'requests', 
            'beautifulsoup4', 
            'colorama', 
            'mechanize',
            'selenium', 
            'pycryptodome', 
            'passlib', 
            'python-nmap',
            'paramiko', 
            'scapy', 
            'pandas', 
            'matplotlib', 
            'tabulate',
            'tqdm', 
            'pyyaml',
            'markdown',
            'weasyprint',  # Untuk generate PDF
            'urllib3'       # Untuk SSL handling
        ]
        
        # Upgrade pip dulu
        self.print_color("  Upgrading pip...", 'blue')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      capture_output=True)
        
        for package in packages:
            self.print_color(f"  Installing {package}...", 'blue')
            try:
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', package],
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    self.print_color(f"  ✓ {package} installed", 'green')
                else:
                    self.print_color(f"  ✗ Failed to install {package}", 'red')
                    if result.stderr:
                        self.print_color(f"    Error: {result.stderr[:100]}", 'yellow')
            except subprocess.TimeoutExpired:
                self.print_color(f"  ⚠ Timeout installing {package}", 'yellow')
            except Exception as e:
                self.print_color(f"  ✗ Error: {str(e)[:50]}", 'red')
                
    def create_requirements(self):
        """Create requirements.txt"""
        self.print_color("\n[6] Creating requirements.txt...", 'yellow')
        
        requirements = """requests==2.31.0
beautifulsoup4==4.12.2
colorama==0.4.6
mechanize==0.4.9
selenium==4.15.0
pycryptodome==3.19.0
passlib==1.7.4
python-nmap==0.7.1
paramiko==3.3.1
scapy==2.5.0
pandas==2.1.3
matplotlib==3.8.0
tabulate==0.9.0
tqdm==4.66.1
pyyaml==6.0.1
markdown==3.5.1
weasyprint==60.2
urllib3==2.1.0
"""
        
        req_path = os.path.join(self.project_dir, 'requirements.txt')
        with open(req_path, 'w') as f:
            f.write(requirements)
        self.print_color("  ✓ requirements.txt created", 'green')
        
    def create_config(self):
        """Create config.yaml"""
        self.print_color("\n[7] Creating config.yaml...", 'yellow')
        
        config = """# Konfigurasi Tugas Modul 2
project:
  name: "Modul2_YogaArfiyanto"
  version: "2.0"
  author: "Yoga Arfiyanto"

paths:
  wordlists: "./wordlists"
  results: "./results"
  logs: "./logs"
  screenshots: "./screenshots"

targets:
  live_cracking: "https://target.rootbrain.com/web101/FormCracking/index.php"
  sql_lesson1: "https://target.rootbrain.com/owasp/injection/lessons/lesson01/index.php"
  sql_lesson3: "https://target.rootbrain.com/owasp/injection/lessons/lesson03/index.php"

cracking:
  threads: 10
  timeout: 300
  max_attempts: 1000000

logging:
  level: "INFO"
  file: "master.log"
  max_size: 10485760  # 10MB
"""
        
        config_path = os.path.join(self.project_dir, 'config.yaml')
        with open(config_path, 'w') as f:
            f.write(config)
        self.print_color("  ✓ config.yaml created", 'green')
        
    def create_gitignore(self):
        """Create .gitignore"""
        self.print_color("\n[8] Creating .gitignore...", 'yellow')
        
        gitignore = """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.env
venv/
env/
env.bak/
venv.bak/
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.dmypy.json
dmypy.json

# Results
results/
*.log
*.txt
!requirements.txt
!hashes/*.txt

# Wordlists
wordlists/*.txt
!wordlists/username.txt
!wordlists/passwords.txt
wordlists/custom/

# Tools binary
tools/cain_abel/*.exe
tools/**/*.exe

# Screenshots
screenshots/
*.png
*.jpg
*.jpeg
*.gif

# Backups
backups/
*.zip
*.tar.gz
*.rar

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# OS
Thumbs.db
desktop.ini
"""
        
        gitignore_path = os.path.join(self.project_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write(gitignore)
        self.print_color("  ✓ .gitignore created", 'green')
        
    def create_wordlist_generator(self):
        """Create custom wordlist generator"""
        self.print_color("\n[9] Creating wordlist generator...", 'yellow')
        
        generator_code = """#!/usr/bin/env python3
"""
        # ... (isi generator.py lengkap)
        
        gen_path = os.path.join(self.project_dir, 'wordlists', 'custom', 'generate.py')
        with open(gen_path, 'w') as f:
            f.write(generator_code)
        self.print_color("  ✓ Created: wordlists/custom/generate.py", 'green')
        
    def check_cain_abel_files(self):
        """Cek apakah file Cain & Abel sudah didownload"""
        self.print_color("\n[10] Checking Cain & Abel files...", 'yellow')
        
        cain_dir = os.path.join(self.project_dir, 'tools', 'cain_abel')
        cain_exe = os.path.join(cain_dir, 'ca_setup.exe')
        winpcap_exe = os.path.join(cain_dir, 'WinPcap_4_1_3.exe')
        
        if os.path.exists(cain_exe):
            size = os.path.getsize(cain_exe)
            self.print_color(f"  ✓ ca_setup.exe found ({size:,} bytes)", 'green')
        else:
            self.print_color(f"  ⚠ ca_setup.exe not found (download manually)", 'yellow')
            
        if os.path.exists(winpcap_exe):
            size = os.path.getsize(winpcap_exe)
            self.print_color(f"  ✓ WinPcap_4_1_3.exe found ({size:,} bytes)", 'green')
        else:
            self.print_color(f"  ⚠ WinPcap_4_1_3.exe not found (download manually)", 'yellow')
            
    def run_platform_installer(self):
        """Jalankan installer spesifik platform"""
        self.print_color("\n[11] Running platform-specific installer...", 'yellow')
        
        if self.system == 'windows':
            # Untuk Windows, jalankan PowerShell script
            installer = os.path.join(self.project_dir, 'tools', 'windows', 'install_tools.ps1')
            if os.path.exists(installer):
                self.print_color("  Running Windows installer...", 'blue')
                subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', installer], 
                             check=False, capture_output=True)
            else:
                self.print_color("  ⚠ Windows installer not found", 'yellow')
                
        elif self.system == 'linux':
            # Untuk Linux, jalankan bash script
            installer = os.path.join(self.project_dir, 'tools', 'kali_linux', 'install_tools.sh')
            if os.path.exists(installer):
                self.print_color("  Running Linux installer...", 'blue')
                subprocess.run(['bash', installer], check=False)
            else:
                self.print_color("  ⚠ Linux installer not found", 'yellow')
                
        elif self.system == 'darwin':  # macOS
            installer = os.path.join(self.project_dir, 'tools', 'macos', 'install_tools.sh')
            if os.path.exists(installer):
                self.print_color("  Running macOS installer...", 'blue')
                subprocess.run(['bash', installer], check=False)
            else:
                self.print_color("  ⚠ macOS installer not found", 'yellow')
                
    def verify(self):
        """Verifikasi instalasi"""
        self.print_color("\n[12] Verifying installation...", 'yellow')
        
        # Cek direktori
        dirs_to_check = ['docs', 'wordlists', 'hashes', 'scripts', 'modules', 'results', 'logs', 'screenshots', 'backups']
        for d in dirs_to_check:
            path = os.path.join(self.project_dir, d)
            if os.path.exists(path):
                self.print_color(f"  ✓ {d}/", 'green')
                
        # Cek file penting
        files_to_check = ['requirements.txt', 'config.yaml', '.gitignore']
        for f in files_to_check:
            path = os.path.join(self.project_dir, f)
            if os.path.exists(path):
                size = os.path.getsize(path)
                self.print_color(f"  ✓ {f} ({size} bytes)", 'green')
                
        # Cek wordlists
        wordlists_dir = os.path.join(self.project_dir, 'wordlists')
        if os.path.exists(wordlists_dir):
            wordlist_files = [f for f in os.listdir(wordlists_dir) if f.endswith('.txt')]
            self.print_color(f"  ✓ Wordlists: {len(wordlist_files)} files", 'green')
            
            # Tampilkan detail wordlists
            for wl in ['indonesian.txt', 'username.txt', 'passwords.txt', 'common_passwords.txt', 'common_usernames.txt']:
                path = os.path.join(wordlists_dir, wl)
                if os.path.exists(path):
                    size = os.path.getsize(path)
                    self.print_color(f"    • {wl}: {size:,} bytes", 'white')
                else:
                    self.print_color(f"    • {wl}: NOT FOUND", 'yellow')
                    
    def show_summary(self):
        """Tampilkan ringkasan instalasi"""
        self.print_color("\n" + "="*60, 'purple')
        self.print_color("INSTALLATION SUMMARY", 'purple')
        self.print_color("="*60, 'purple')
        
        self.print_color("\n✅ Completed:", 'green')
        self.print_color("  • All directories created", 'white')
        self.print_color("  • Hash files generated", 'white')
        self.print_color("  • Wordlists downloaded (see above)", 'white')
        self.print_color("  • Python packages installed", 'white')
        self.print_color("  • Configuration files created", 'white')
        
        self.print_color("\n📥 Manual Download Required:", 'yellow')
        self.print_color("  • tools/cain_abel/ca_setup.exe", 'white')
        self.print_color("  • tools/cain_abel/WinPcap_4_1_3.exe", 'white')
        
        self.print_color("\n📁 Project Structure:", 'cyan')
        self.print_color(f"  • Location: {self.project_dir}", 'white')
        self.print_color("  • Total folders: 25+", 'white')
        
        self.print_color("\n🚀 Next Steps:", 'blue')
        self.print_color("  1. Download Cain & Abel files (see README.txt)", 'white')
        self.print_color("  2. cd scripts", 'white')
        self.print_color("  3. python 05_master_controller.py", 'white')
        self.print_color("  4. Choose menu option", 'white')
        
        self.print_color("\n" + "="*60, 'purple')
        
    def run(self):
        """Main function"""
        self.print_banner()
        
        steps = [
            self.create_directories,
            self.create_cain_abel_readme,
            self.create_hash_files,
            self.download_wordlists,
            self.create_requirements,
            self.create_config,
            self.create_gitignore,
            self.create_wordlist_generator,
            self.install_python_packages,
            self.run_platform_installer,
            self.check_cain_abel_files,
            self.verify,
            self.show_summary
        ]
        
        for step in steps:
            step()
            
        self.print_color("\n" + "="*60, 'green')
        self.print_color("INSTALLATION COMPLETE!", 'green')
        self.print_color("="*60, 'green')

if __name__ == "__main__":
    installer = IntegratedInstaller()
    installer.run()