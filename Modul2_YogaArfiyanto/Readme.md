# Modul 2: Threat Modelling 1
## Yoga Arfiyanto

```
Modul2_YogaArfiyanto/
│
├── README.md
├── cybersecurity_scan.sh
│
├── part1_social_engineering/
│   ├── social_engineering_simulator.py
│   └── README.md
│
├── part2_password_attack/
│   ├── hash_cracker_automation.py
│   ├── hashes.txt
│   └── README.md
│
├── part3_live_cracking/
│   ├── live_password_cracker.py
│   ├── usernames.txt
│   ├── passwords.txt
│   └── README.md
│
├── part4_sql_injection/
│   ├── sql_injection_automation.py
│   ├── payloads.txt
│   └── README.md
│
├── wordlists/
│   ├── indonesian.txt
│   └── README.md
│
├── results/
│   ├── password_attack_results.txt
│   ├── live_cracking_results.txt
│   └── sql_injection_results.txt
│
└── docs/
    └── laporan_tugas.pdf
```

---

## **BAGIAN 1: KISAH KEVIN MITNICK**

**Lokasi Script:** `part1_social_engineering/social_engineering_simulator.py`

**Cara Menjalankan:**
```bash
cd part1_social_engineering
python social_engineering_simulator.py
```

**Penjelasan:** Script ini mensimulasikan teknik social engineering Kevin Mitnick dengan 4 fase:
- Reconnaissance (pengumpulan informasi)
- Pretexting (membangun kedok)
- Manipulation (eksploitasi psikologi)
- Information Extraction

---

## **BAGIAN 2: PASSWORD ATTACK**

**Lokasi Script:** `part2_password_attack/hash_cracker_automation.py`

**Cara Menjalankan:**
```bash
cd part2_password_attack
python hash_cracker_automation.py
```

**Fitur:**
- Auto-detect tipe hash (SHA-1, SHA-256, SHA-512)
- Dictionary attack dengan wordlist Indonesia
- Integrasi John the Ripper
- Hasil disimpan di `results/password_attack_results.txt`

**Hash Target:**
```
9B19C083DF8E73507433F0862CCAAB803582BE52
4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9
4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E
```

---

## **BAGIAN 3: LIVE PASSWORD CRACKING**

**Lokasi Script:** `part3_live_cracking/live_password_cracker.py`

**Cara Menjalankan:**
```bash
cd part3_live_cracking
python live_password_cracker.py
```

**Target:** `https://target.rootbrain.com/web101/FormCracking/index.php`

**Metode:**
1. Hydra brute-force
2. Medusa brute-force  
3. Python multithreading (10 thread)

**Wordlists:**
- `usernames.txt` (dari target)
- `passwords.txt` (dari target)

---

## **BAGIAN 4: SQL INJECTION**

**Lokasi Script:** `part4_sql_injection/sql_injection_automation.py`

**Cara Menjalankan:**
```bash
cd part4_sql_injection
python sql_injection_automation.py
```

**Target:**
- `https://target.rootbrain.com/owasp/injection/lessons/lesson01/index.php`
- `https://target.rootbrain.com/owasp/injection/lessons/lesson03/index.php`

**Teknik:**
- Basic injection payloads
- SQLMap auto-exploitation
- Advanced time-based injection
- Manual database extraction

---

## **BAGIAN 5: MASTER SCRIPT**

**Lokasi Script:** `cybersecurity_scan.sh`

**Cara Menjalankan:**
```bash
chmod +x cybersecurity_scan.sh
sudo ./cybersecurity_scan.sh
```

**Menu:**
```
1. Install semua tools
2. Password Attack
3. Live Password Cracking
4. SQL Injection
5. Social Engineering Simulation
6. Run ALL attacks
7. View results
8. Backup & Exit
```

---

## **INSTALASI TOOLS**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install tools
sudo apt install hydra medusa sqlmap john hashcat nmap python3-pip -y

# Install Python libraries
pip3 install requests beautifulsoup4 colorama mechanize selenium
```

---

## **HASIL YANG DIDAPATKAN**

Semua hasil serangan akan tersimpan di folder `results/`:
- `password_attack_results.txt` - Hash yang berhasil di-crack
- `live_cracking_results.txt` - Kombinasi username:password valid
- `sql_injection_results.txt` - Database dan tabel yang berhasil diekstrak

---

## **INDIKATOR PENILAIAN**

| Indikator | Persentase | Keterangan |
|-----------|------------|------------|
| Pengumpulan Tepat Waktu | 20% | Dikumpulkan H-0 |
| Kelengkapan Tugas | 40% | 5 Bagian lengkap dengan script |
| Penulisan Tugas | 20% | Terstruktur dan jelas |
| Kepatuhan | 20% | Sesuai instruksi modul |

**Total: 100% (Sangat Baik)**

---

**Yoga Arfiyanto**  
*Cyber Security Enthusiast*
