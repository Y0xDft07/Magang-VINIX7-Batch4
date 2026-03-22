# 🛡️ Expert Vulnerability Assessment Tool (Web Only)

Alat otomatis untuk melakukan **Vulnerability Assessment** dan **Penetration Testing** pada aplikasi web tingkat ahli.  
Dikembangkan sebagai pemenuhan Tugas Modul 3 – Project-Based Internship Vinix7.

Terdapat **dua versi skrip** yang tersedia:
- `run_assessment.py` – Versi standar dengan integrasi Arachni dan eksploitasi manual.
- `run_assessment_new.py` – Versi agresif dengan fitur **bypass 403**, **fuzzing path**, **payload modern**, dan **mode agresif**.

---

## ✨ Fitur Utama

### Versi Standar (`run_assessment.py`)
- Scanning web terfokus pada daftar URL yang disediakan (menghemat waktu).
- Eksploitasi multi-teknik: SQLi, XSS, Command Injection, LFI, File Upload.
- Payload bypass: encoding, komentar inline, case variation, null byte, wrapper PHP.
- Parallel exploitation dengan `ThreadPoolExecutor`.
- Laporan komprehensif (HTML, JSON, teks) dengan tabel dan rekomendasi.
- Menu interaktif 4 mode.

### Versi Agresif (`run_assessment_new.py`)
**Semua fitur versi standar, ditambah:**
- **Bypass 403** – Menguji 7 metode HTTP dan 12 header spoofing (X-Forwarded-For, X-Originating-IP, dll.) untuk mengakses halaman yang diblokir.
- **Fuzzing Path** – Mencari endpoint tersembunyi dengan berbagai variasi path (encoding, traversal, direktori umum) dan mencoba bypass jika mendapat 403.
- **Payload Eksploitasi Lebih Canggih**:
  - SQLi: union dengan encoding ganda, error-based, time-based, boolean blind.
  - XSS: polyglot, encoding HTML/URL ganda.
  - Command Injection: berbagai pemisah dan encoding.
  - LFI: traversal dengan encoding, wrapper PHP, null byte.
  - File Upload: bypass ekstensi dan magic bytes (GIF, JPEG).
- **Deteksi Heuristik** – Menggunakan perbedaan panjang respons dan waktu untuk mendeteksi kerentanan blind.
- **Mode Agresif (Menu 5)** – Menggabungkan bypass 403, fuzzing path, dan eksploitasi pada semua endpoint yang ditemukan.

---

## 🖥️ Persyaratan Sistem

- **Sistem Operasi**: Linux (Ubuntu/Debian direkomendasikan)
- **Python**: 3.6 atau lebih baru
- **Arachni**: Framework vulnerability scanner (versi 1.6.1.3) – [Unduh di sini](https://www.arachni-scanner.com/)
- **cURL**: Untuk pengujian manual
- **Koneksi Internet**: Untuk mengakses target

---

## ⚙️ Instalasi

### 1. Clone atau salin skrip
```bash
mkdir ~/pentest-tool
cd ~/pentest-tool
# Salin kedua skrip ke direktori ini
chmod +x run_assessment.py run_assessment_new.py
```

### 2. Instal Arachni
Unduh dan ekstrak Arachni 1.6.1.3:
```bash
cd ~/Downloads
wget https://github.com/Arachni/arachni/releases/download/v1.6.1.3/arachni-1.6.1.3-0.6.1.1-linux-x86_64.tar.gz
tar -xzf arachni-1.6.1.3-0.6.1.1-linux-x86_64.tar.gz
```
Pastikan path di dalam skrip (`ARACHNI_BASE`) sesuai dengan lokasi ekstraksi. Jika berbeda, sesuaikan di bagian konfigurasi skrip.

### 3. Pastikan `curl` terinstal
```bash
sudo apt update && sudo apt install curl -y
```

---

## 🚀 Cara Penggunaan

Jalankan salah satu skrip sesuai kebutuhan:

```bash
python3 run_assessment.py      # Versi standar
# atau
python3 run_assessment_new.py  # Versi agresif
```

Keduanya akan menampilkan **menu interaktif**. Pilih mode yang diinginkan dengan memasukkan angka.

### Menu Versi Standar (`run_assessment.py`)
```
============================================================
   VULNERABILITY ASSESSMENT TOOL (WEB ONLY)
============================================================
Pilih mode eksekusi:
1. Scan dengan Arachni saja (menghasilkan laporan)
2. Eksploitasi manual pada semua URL (tanpa scan Arachni)
3. Scan Arachni + Eksploitasi manual (jika ada kerentanan high/critical)
4. Keluar
Masukkan pilihan [1-4]:
```

### Menu Versi Agresif (`run_assessment_new.py`)
```
============================================================
   VULNERABILITY ASSESSMENT TOOL (WEB ONLY) - AGGRESSIVE
============================================================
Pilih mode eksekusi:
1. Scan dengan Arachni saja
2. Eksploitasi manual pada semua URL
3. Scan Arachni + Eksploitasi manual (jika ada high/critical)
4. Mode Agresif: Bypass 403 + Fuzzing + Eksploitasi manual
5. Keluar
Masukkan pilihan [1-5]:
```

### Penjelasan Mode

| Mode | Versi Standar | Versi Agresif | Deskripsi |
|------|---------------|---------------|-----------|
| **1** | ✅ | ✅ | Menjalankan Arachni scan pada URL yang telah ditentukan, menghasilkan laporan HTML dan JSON. Eksploitasi tidak dilakukan. |
| **2** | ✅ | ✅ | Tidak menjalankan Arachni, langsung mencoba semua payload eksploitasi ke setiap URL dalam daftar. |
| **3** | ✅ | ✅ | Kombinasi: scan Arachni terlebih dahulu, kemudian jika ditemukan kerentanan high/critical, dilakukan eksploitasi mendalam pada parameter tersebut. |
| **4** | ❌ | ✅ | **Mode Agresif** – Melakukan fuzzing path pada domain, mencoba bypass 403 pada setiap endpoint yang ditemukan, lalu mengeksploitasi semua parameter yang ada. |
| **5** | ✅ (Keluar) | ✅ (Keluar) | Keluar dari program. |

---

## 📁 Struktur Direktori Output

Kedua skrip menghasilkan folder laporan dengan nama `laporan_akhir_web/` (standar) atau `laporan_akhir_web/` (agresif – sama, tetapi konten bisa berbeda). Struktur:

```
laporan_akhir_web/
├── web/
│   ├── restrict_paths.txt      # Daftar path untuk membatasi scan
│   ├── scan.afr                 # Laporan mentah Arachni
│   ├── laporan.json             # Hasil scan Arachni (format JSON)
│   └── laporan.html.zip         # Laporan HTML Arachni (perlu diekstrak)
├── log_eksploitasi.txt          # Log detail eksploitasi
├── eksekusi.log                 # Log umum eksekusi
├── laporan_akhir.txt            # Laporan teks gabungan
├── laporan_akhir.json           # Laporan JSON gabungan
└── laporan.html                 # Laporan HTML utama (gabungan)
```

---

## 📊 Contoh Hasil Laporan

### Ringkasan di Terminal
```
============================================================
RINGKASAN LAPORAN (WEB ONLY):
  Semua temuan web: 25
  Kerentanan Web High/Critical: 0
  Eksploitasi Berhasil: 3
  Laporan HTML: laporan_akhir_web/laporan.html
============================================================
```

### Tampilan HTML
Laporan HTML menampilkan:
- Ringkasan statistik
- Tabel semua temuan (termasuk informational)
- Tabel kerentanan high/critical (jika ada)
- Bukti konsep eksploitasi (dengan payload, URL, data terekstrak)
- Rekomendasi perbaikan

---

## ⚠️ Catatan Penting

- **Target Default**: Kedua skrip dikonfigurasi untuk `http://vulnweb.rootbrain.com`. Ubah variabel `BASE_URL` dan `URL_LIST` jika ingin menargetkan domain lain.
- **Waktu Scan**: Arachni membutuhkan waktu sekitar 1 jam untuk menyelesaikan scan pada target contoh.
- **Hak Akses**: Tidak diperlukan `sudo` untuk menjalankan skrip.
- **Legalitas**: Gunakan hanya pada sistem yang Anda miliki atau telah mendapatkan izin tertulis. Penyalahgunaan dapat melanggar hukum.
- **Perbedaan Skrip**: 
  - `run_assessment.py` cocok untuk pengujian standar.
  - `run_assessment_new.py` direkomendasikan untuk pengujian mendalam, terutama jika target menerapkan proteksi 403 atau memiliki endpoint tersembunyi.

---

## 📝 Lisensi

Skrip ini dibuat untuk tujuan edukasi dan tidak dilisensikan secara komersial. Gunakan dengan bijak.
