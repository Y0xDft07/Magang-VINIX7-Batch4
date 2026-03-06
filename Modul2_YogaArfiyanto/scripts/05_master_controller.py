#!/usr/bin/env python3
"""
Master Controller - Menjalankan semua script
Module 2: Threat Modelling
Author: Yoga Arfiyanto
"""

import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

# Tambahkan path module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from modules.logger import get_logger
    from modules.result_saver import ResultSaver
except ImportError:
    # Fallback if modules not available
    get_logger = None
    ResultSaver = None

# Try to import colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Define dummy colors
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    Style = Fore

class MasterController:
    """Controller untuk menjalankan semua script"""
    
    def __init__(self):
        self.scripts_dir = os.path.dirname(__file__)
        self.project_dir = os.path.dirname(self.scripts_dir)
        
        self.scripts = {
            '1': {
                'name': 'Social Engineering Simulation',
                'file': '01_social_engineering.py',
                'description': 'Simulasi teknik social engineering Kevin Mitnick'
            },
            '2': {
                'name': 'Hash Cracker',
                'file': '02_hash_cracker.py',
                'description': 'Crack hash dengan multiple methods'
            },
            '3': {
                'name': 'Live Password Cracker',
                'file': '03_live_cracker.py',  # Nama file asli
                'description': 'Live cracking dengan Hydra/Medusa/Python'
            },
            '4': {
                'name': 'SQL Injection',
                'file': '04_sql_injection.py',
                'description': 'Auto SQL injection exploitation'
            }
        }
        
        # Setup logging
        if get_logger:
            self.log = get_logger('master')
        else:
            self.log = None
            
        # Setup results directory
        self.results_dir = os.path.join(self.project_dir, 'results')
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Setup logs directory
        self.logs_dir = os.path.join(self.project_dir, 'logs')
        os.makedirs(self.logs_dir, exist_ok=True)
        
        self.log_file = os.path.join(self.logs_dir, 'master_log.txt')
        
    def print_color(self, text, color='white'):
        """Print dengan warna jika tersedia"""
        if HAS_COLOR:
            color_map = {
                'red': Fore.RED,
                'green': Fore.GREEN,
                'yellow': Fore.YELLOW,
                'blue': Fore.BLUE,
                'magenta': Fore.MAGENTA,
                'cyan': Fore.CYAN,
                'white': Fore.WHITE
            }
            print(f"{color_map.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}")
        else:
            print(text)
        
    def banner(self):
        """Tampilkan banner"""
        self.print_color("""
╔══════════════════════════════════════════════════════════╗
║              MASTER CONTROLLER - MODUL 2                 ║
║                  YOGA ARFIYANTO                           ║
╚══════════════════════════════════════════════════════════╝
        """, 'cyan')
        
    def check_environment(self):
        """Cek environment dan dependencies"""
        self.print_color("\n[CHECK] Memeriksa environment...", 'yellow')
        
        # Cek Python version
        python_version = sys.version_info
        self.print_color(f"  Python: {python_version.major}.{python_version.minor}.{python_version.micro}", 'white')
        
        # Cek direktori yang diperlukan
        dirs = [
            'wordlists',
            'hashes',
            'results',
            'results/password_attack',
            'results/live_cracking',
            'results/sql_injection',
            'logs',
            'screenshots',
            'screenshots/01_installation',
            'screenshots/02_password_attack',
            'screenshots/03_live_cracking',
            'screenshots/04_sql_injection',
            'backups'
        ]
        
        for dir_path in dirs:
            full_path = os.path.join(self.project_dir, dir_path)
            if os.path.exists(full_path):
                self.print_color(f"  ✓ {dir_path}", 'green')
            else:
                self.print_color(f"  Membuat {dir_path}", 'yellow')
                os.makedirs(full_path, exist_ok=True)
                
        # Cek wordlists
        wordlist_files = ['indonesian.txt', 'username.txt', 'passwords.txt']
        for wl in wordlist_files:
            wl_path = os.path.join(self.project_dir, 'wordlists', wl)
            if os.path.exists(wl_path):
                size = os.path.getsize(wl_path)
                self.print_color(f"  ✓ {wl} ({size} bytes)", 'green')
            else:
                self.print_color(f"  ⚠ {wl} belum ada. Jalankan: python3 tools/install_all.py", 'yellow')
                
        return True
        
    def show_menu(self):
        """Tampilkan menu utama"""
        self.print_color(f"\nWaktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 'white')
        self.print_color("\n" + "="*60, 'white')
        self.print_color("MENU UTAMA", 'white')
        self.print_color("="*60, 'white')
        
        for key, script in self.scripts.items():
            self.print_color(f"\n  {key}. {script['name']}", 'green')
            self.print_color(f"     {script['description']}", 'white')
            
        self.print_color("\n  a. Jalankan SEMUA script", 'yellow')
        self.print_color("  b. Lihat hasil serangan", 'yellow')
        self.print_color("  c. Backup hasil", 'yellow')
        self.print_color("  q. Keluar", 'red')
        self.print_color("\n" + "="*60, 'white')
        
    def run_script(self, script_key):
        """Jalankan script tertentu"""
        script = self.scripts.get(script_key)
        if not script:
            self.print_color("Pilihan tidak valid!", 'red')
            return
            
        script_path = os.path.join(self.scripts_dir, script['file'])
        
        if not os.path.exists(script_path):
            self.print_color(f"File {script['file']} tidak ditemukan!", 'red')
            return
            
        self.print_color(f"\nMenjalankan: {script['name']}", 'cyan')
        self.print_color("="*40, 'cyan')
        
        try:
            # Catat ke log
            with open(self.log_file, 'a') as f:
                f.write(f"\n[{datetime.now()}] Menjalankan {script['file']}\n")
                
            # Jalankan script
            result = subprocess.run([sys.executable, script_path], 
                                  capture_output=True, text=True)
            
            # Tampilkan output
            if result.stdout:
                print(result.stdout)
                
            if result.stderr:
                self.print_color(result.stderr, 'red')
                
            # Catat hasil
            with open(self.log_file, 'a') as f:
                f.write(f"Status: {'Success' if result.returncode == 0 else 'Failed'}\n")
                f.write("="*40 + "\n")
                
            if result.returncode == 0:
                self.print_color(f"\n✓ Script selesai!", 'green')
            else:
                self.print_color(f"\n✗ Script error dengan code {result.returncode}", 'red')
                
        except Exception as e:
            self.print_color(f"Error: {e}", 'red')
            
    def run_all(self):
        """Jalankan semua script"""
        self.print_color("\nMenjalankan SEMUA script...", 'yellow')
        self.print_color("="*40, 'yellow')
        
        for key in self.scripts:
            self.print_color(f"\n[{key}] {self.scripts[key]['name']}", 'cyan')
            self.run_script(key)
            time.sleep(2)  # Jeda antar script
            
        self.print_color("\n✓ Semua script telah dijalankan!", 'green')
        
    def view_results(self):
        """Lihat hasil serangan"""
        self.print_color("\nHASIL SERANGAN:", 'yellow')
        self.print_color("="*40, 'yellow')
        
        attack_dirs = {
            'Password Attack': os.path.join(self.results_dir, 'password_attack'),
            'Live Cracking': os.path.join(self.results_dir, 'live_cracking'),
            'SQL Injection': os.path.join(self.results_dir, 'sql_injection')
        }
        
        for attack_name, attack_path in attack_dirs.items():
            self.print_color(f"\n{attack_name}:", 'green')
            
            if os.path.exists(attack_path):
                files = os.listdir(attack_path)
                if files:
                    for file in sorted(files, reverse=True)[:5]:  # Show 5 most recent
                        file_path = os.path.join(attack_path, file)
                        size = os.path.getsize(file_path)
                        modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                        self.print_color(f"  • {file} ({size} bytes) - {modified.strftime('%H:%M:%S')}", 'white')
                        
                        # Tampilkan preview untuk file kecil
                        if size < 2000 and file.endswith('.txt'):
                            try:
                                with open(file_path, 'r') as f:
                                    content = f.read().strip()
                                    if content:
                                        preview = content[:150] + "..." if len(content) > 150 else content
                                        # Bersihkan preview untuk tampilan
                                        preview = preview.replace('\n', ' ').replace('\r', '')
                                        self.print_color(f"    Preview: {preview}", 'blue')
                            except:
                                pass
                else:
                    self.print_color("  (belum ada hasil)", 'yellow')
            else:
                self.print_color("  (folder belum ada)", 'yellow')
                
    def backup_results(self):
        """Backup semua hasil"""
        self.print_color("\nBackup hasil...", 'yellow')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.project_dir, 'backups', f'backup_{timestamp}')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy results
        import shutil
        if os.path.exists(self.results_dir):
            shutil.copytree(self.results_dir, os.path.join(backup_dir, 'results'))
            self.print_color(f"  ✓ Results backed up", 'green')
            
        # Copy logs
        if os.path.exists(self.logs_dir):
            shutil.copytree(self.logs_dir, os.path.join(backup_dir, 'logs'))
            self.print_color(f"  ✓ Logs backed up", 'green')
            
        # Create archive
        shutil.make_archive(backup_dir, 'zip', backup_dir)
        shutil.rmtree(backup_dir)  # Remove unzipped
        
        self.print_color(f"✓ Backup created: backups/backup_{timestamp}.zip", 'green')
        
    def run(self):
        """Main loop"""
        self.banner()
        self.check_environment()
        
        while True:
            self.show_menu()
            choice = input("\nPilihan Anda: ").strip().lower()
            
            if choice == 'q':
                self.print_color("\nTerima kasih! Keluar...", 'green')
                break
            elif choice == 'a':
                self.run_all()
            elif choice == 'b':
                self.view_results()
            elif choice == 'c':
                self.backup_results()
            elif choice in self.scripts:
                self.run_script(choice)
            else:
                self.print_color("Pilihan tidak valid!", 'red')
                
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    controller = MasterController()
    controller.run()