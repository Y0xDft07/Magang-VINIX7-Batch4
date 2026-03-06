#!/usr/bin/env python3
"""
Auto Hash Cracker - Multiple Tools Support
Module 2: Threat Modelling
Author: Yoga Arfiyanto
"""

import hashlib
import subprocess
import os
import sys
import time
from datetime import datetime
import json
from colorama import init, Fore, Style

# Tambahkan path module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from modules.hash_identifier import HashIdentifier
    from modules.wordlist_manager import WordlistManager
    from modules.result_saver import ResultSaver
    from modules.logger import get_logger
except ImportError:
    # Fallback jika module belum ada
    print("⚠️ Modules not found, using basic functionality")
    HashIdentifier = None
    WordlistManager = None
    ResultSaver = None
    get_logger = None

init(autoreset=True)

class HashCracker:
    """Auto Hash Cracker dengan multiple methods"""
    
    def __init__(self):
        self.hashes = self._load_hashes()
        self.wordlist_path = os.path.join(os.path.dirname(__file__), '..', 'wordlists', 'indonesian.txt')
        self.results = {}
        
        # Initialize modules if available
        if HashIdentifier:
            self.identifier = HashIdentifier()
        else:
            self.identifier = None
            
        if WordlistManager:
            self.wordlist_mgr = WordlistManager()
        else:
            self.wordlist_mgr = None
            
        if ResultSaver:
            self.saver = ResultSaver("password_attack")
        else:
            self.saver = None
            
        if get_logger:
            self.log = get_logger('hash_cracker')
        else:
            self.log = None
            
    def _load_hashes(self):
        """Load hash dari file"""
        hashes = {}
        hash_file = os.path.join(os.path.dirname(__file__), '..', 'hashes', 'hash_target.txt')
        
        try:
            with open(hash_file, 'r') as f:
                content = f.read()
                
            # Parse berdasarkan label
            import re
            sha1_match = re.search(r'SHA-1[:\s]+([A-F0-9]{40})', content, re.IGNORECASE)
            if sha1_match:
                hashes['sha1'] = sha1_match.group(1)
                
            long_match = re.search(r'Hash2[:\s]+([A-F0-9]{100,})', content, re.IGNORECASE)
            if long_match:
                hashes['long'] = long_match.group(1)
                
            another_match = re.search(r'Hash3[:\s]+([A-F0-9]{100,})', content, re.IGNORECASE)
            if another_match:
                hashes['another'] = another_match.group(1)
                
        except FileNotFoundError:
            # Default dari tugas
            hashes = {
                'sha1': '9B19C083DF8E73507433F0862CCAAB803582BE52',
                'long': '4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9',
                'another': '4BEE76AB9648A2DE5E77B41861FAD982980292D739E5F4CEBA4A6182BBD4199B05D2B0A6461E65288100719459B0058D8446F7840DD0FF7694FF6957BE213A2E'
            }
            
        return hashes
        
    def banner(self):
        print(Fore.CYAN + """
╔══════════════════════════════════════════════════════════╗
║                  AUTO HASH CRACKER                        ║
║     Cain & Abel | John the Ripper | Hashcat | Python     ║
╚══════════════════════════════════════════════════════════╝
        """)
        
    def identify_hashes(self):
        """Identifikasi tipe setiap hash"""
        print(Fore.YELLOW + "\n[STEP 1] Mengidentifikasi tipe hash...")
        
        for name, hash_string in self.hashes.items():
            if self.identifier:
                hash_type = self.identifier.identify(hash_string)
            else:
                # Basic identification
                length = len(hash_string)
                if length == 40:
                    hash_type = "SHA-1"
                elif length == 64:
                    hash_type = "SHA-256"
                elif length == 128:
                    hash_type = "SHA-512"
                else:
                    hash_type = "Unknown"
                    
            print(Fore.WHITE + f"  {name.upper():10}: {hash_string[:30]}... -> {hash_type}")
            self.results[name] = {
                'hash': hash_string,
                'type': hash_type,
                'status': 'pending'
            }
            
    def prepare_wordlist(self):
        """Siapkan wordlist untuk cracking"""
        print(Fore.YELLOW + "\n[STEP 2] Menyiapkan wordlist...")
        
        if not os.path.exists(self.wordlist_path):
            print(Fore.RED + f"  Wordlist tidak ditemukan di {self.wordlist_path}")
            print(Fore.CYAN + "  Jalankan python3 tools/install_all.py untuk mendownload wordlist")
            return False
            
        # Hitung jumlah kata
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                word_count = sum(1 for _ in f)
            print(Fore.GREEN + f"  ✓ Wordlist siap: {word_count} kata")
            return True
        except:
            print(Fore.RED + "  Error membaca wordlist")
            return False
            
    def method_python(self, hash_name, hash_string, hash_type):
        """Method 1: Python Dictionary Attack"""
        print(Fore.YELLOW + f"\n[Method 1] Python Dictionary Attack - {hash_name}")
        
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
                
            total = len(words)
            print(Fore.BLUE + f"  Mencoba {total} kata...")
            
            start_time = time.time()
            
            for i, word in enumerate(words):
                if i % 1000 == 0 and i > 0:
                    elapsed = time.time() - start_time
                    print(Fore.WHITE + f"    Progress: {i}/{total} ({i/total*100:.1f}%) - {elapsed:.1f}s")
                    
                # Hash sesuai tipe
                if hash_type == "SHA-1":
                    hashed = hashlib.sha1(word.encode()).hexdigest().upper()
                elif hash_type == "SHA-256":
                    hashed = hashlib.sha256(word.encode()).hexdigest().upper()
                elif hash_type == "SHA-512":
                    hashed = hashlib.sha512(word.encode()).hexdigest().upper()
                else:
                    continue
                    
                if hashed == hash_string.upper():
                    elapsed = time.time() - start_time
                    print(Fore.GREEN + f"\n  ✅ PASSWORD DITEMUKAN: '{word}'")
                    print(Fore.GREEN + f"     Waktu: {elapsed:.2f} detik")
                    return word
                    
            print(Fore.RED + "\n  ✗ Password tidak ditemukan dalam wordlist")
            return None
            
        except Exception as e:
            print(Fore.RED + f"  Error: {e}")
            return None
            
    def method_john(self, hash_name, hash_string, hash_type):
        """Method 2: John the Ripper"""
        print(Fore.YELLOW + f"\n[Method 2] John the Ripper - {hash_name}")
        
        # Mapping hash type ke format John
        john_formats = {
            "SHA-1": "raw-sha1",
            "SHA-256": "raw-sha256",
            "SHA-512": "raw-sha512",
            "MD5": "raw-md5"
        }
        
        if hash_type not in john_formats:
            print(Fore.RED + f"  Tipe hash {hash_type} tidak didukung John")
            return None
            
        # Buat file temporary
        temp_file = f"../logs/temp_{hash_name}_{int(time.time())}.txt"
        with open(temp_file, 'w') as f:
            f.write(hash_string.lower())
            
        try:
            # Jalankan John
            cmd = f"john --format={john_formats[hash_type]} --wordlist={self.wordlist_path} {temp_file}"
            print(Fore.BLUE + f"  Menjalankan: {cmd}")
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            # Lihat hasil
            show_cmd = f"john --show --format={john_formats[hash_type]} {temp_file}"
            show_result = subprocess.run(show_cmd, shell=True, capture_output=True, text=True)
            
            if ':' in show_result.stdout:
                password = show_result.stdout.split(':')[1].strip()
                print(Fore.GREEN + f"\n  ✅ PASSWORD DITEMUKAN: '{password}'")
                return password
                
        except subprocess.TimeoutExpired:
            print(Fore.RED + "  John timeout (60 detik)")
        except Exception as e:
            print(Fore.RED + f"  Error: {e}")
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
        return None
        
    def method_hashcat(self, hash_name, hash_string, hash_type):
        """Method 3: Hashcat"""
        print(Fore.YELLOW + f"\n[Method 3] Hashcat - {hash_name}")
        
        # Mapping hash type ke mode Hashcat
        hashcat_modes = {
            "SHA-1": "100",
            "SHA-256": "1400",
            "SHA-512": "1700",
            "MD5": "0"
        }
        
        if hash_type not in hashcat_modes:
            print(Fore.RED + f"  Tipe hash {hash_type} tidak didukung Hashcat")
            return None
            
        # Buat file hash
        hash_file = f"../logs/hashcat_{hash_name}.txt"
        with open(hash_file, 'w') as f:
            f.write(hash_string.lower())
            
        try:
            # Jalankan Hashcat
            mode = hashcat_modes[hash_type]
            cmd = f"hashcat -m {mode} -a 0 {hash_file} {self.wordlist_path} --force --quiet"
            print(Fore.BLUE + f"  Menjalankan: hashcat -m {mode} -a 0 [hash] [wordlist]")
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            # Cek hasil
            show_cmd = f"hashcat -m {mode} {hash_file} --show"
            show_result = subprocess.run(show_cmd, shell=True, capture_output=True, text=True)
            
            if ':' in show_result.stdout:
                password = show_result.stdout.split(':')[1].strip()
                print(Fore.GREEN + f"\n  ✅ PASSWORD DITEMUKAN: '{password}'")
                return password
                
        except Exception as e:
            print(Fore.RED + f"  Error: {e}")
        finally:
            if os.path.exists(hash_file):
                os.remove(hash_file)
                
        return None
        
    def crack_all(self):
        """Crack semua hash dengan semua metode"""
        self.banner()
        
        # Identifikasi hash
        self.identify_hashes()
        
        # Siapkan wordlist
        if not self.prepare_wordlist():
            return
            
        # Crack setiap hash
        for hash_name, hash_data in self.results.items():
            print(Fore.WHITE + f"\n{'='*60}")
            print(Fore.WHITE + f"MEMPROSES: {hash_name.upper()}")
            print(Fore.WHITE + f"Hash: {hash_data['hash'][:50]}...")
            print(Fore.WHITE + f"Tipe: {hash_data['type']}")
            print(Fore.WHITE + f"{'='*60}")
            
            # Coba method Python dulu
            password = self.method_python(hash_name, hash_data['hash'], hash_data['type'])
            
            # Jika gagal, coba John
            if not password and hash_data['type'] != "Unknown":
                password = self.method_john(hash_name, hash_data['hash'], hash_data['type'])
                
            # Jika masih gagal, coba Hashcat
            if not password and hash_data['type'] != "Unknown":
                password = self.method_hashcat(hash_name, hash_data['hash'], hash_data['type'])
                
            # Simpan hasil
            hash_data['password'] = password if password else "Not Found"
            hash_data['status'] = "Found" if password else "Not Found"
            
        # Tampilkan ringkasan
        self.show_summary()
        
        # Simpan hasil
        self.save_results()
        
    def show_summary(self):
        """Tampilkan ringkasan hasil"""
        print(Fore.GREEN + """
╔══════════════════════════════════════════════════════════╗
║                    RINGKASAN HASIL                       ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        for hash_name, hash_data in self.results.items():
            if hash_data['password'] != "Not Found":
                status = Fore.GREEN + "✓ FOUND"
                print(Fore.WHITE + f"{hash_name.upper():15}: {status}")
                print(Fore.WHITE + f"                Password: {hash_data['password']}")
            else:
                status = Fore.RED + "✗ NOT FOUND"
                print(Fore.WHITE + f"{hash_name.upper():15}: {status}")
                
    def save_results(self):
        """Simpan hasil ke file - UBAH PATH KE results/"""
        # Buat direktori results jika belum ada
        results_dir = os.path.join(os.path.dirname(__file__), '..', 'results', 'password_attack')
        os.makedirs(results_dir, exist_ok=True)
        
        output_file = os.path.join(results_dir, f'hasil_cracking_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        with open(output_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("HASIL PASSWORD CRACKING\n")
            f.write(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            
            for hash_name, hash_data in self.results.items():
                f.write(f"{hash_name.upper()}:\n")
                f.write(f"  Hash: {hash_data['hash']}\n")
                f.write(f"  Tipe: {hash_data['type']}\n")
                f.write(f"  Password: {hash_data['password']}\n")
                f.write("-"*40 + "\n")
                
        print(Fore.GREEN + f"\n✓ Hasil disimpan di {output_file}")
        
        # Juga simpan dalam format JSON untuk report generator
        json_file = os.path.join(results_dir, f'hasil_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(Fore.GREEN + f"✓ JSON saved: {json_file}")

if __name__ == "__main__":
    cracker = HashCracker()
    cracker.crack_all()