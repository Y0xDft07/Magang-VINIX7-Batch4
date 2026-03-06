#!/usr/bin/env python3
"""
Social Engineering Simulator - Kevin Mitnick Style
Module 2: Threat Modelling
Author: Yoga Arfiyanto
"""

import time
import random
import json
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class KevinMitnickSimulator:
    """Simulasi teknik social engineering Kevin Mitnick"""
    
    def __init__(self):
        self.target_info = {}
        self.stage = 0
        self.log_file = "../logs/social_engineering.log"
        
    def banner(self):
        print(Fore.RED + """
╔══════════════════════════════════════════════════════════════╗
║     KEVIN MITNICK - THE GOD OF SOCIAL ENGINEERING           ║
║                    (1963 - 2023)                             ║
║         "Human is the weakest link in security"             ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
    def phase1_osint(self):
        """Phase 1: Open Source Intelligence"""
        print(Fore.YELLOW + "\n[PHASE 1] OSINT - Open Source Intelligence")
        print(Fore.CYAN + "Mengumpulkan informasi dari sumber publik...")
        
        # Simulasi pengumpulan data
        time.sleep(2)
        self.target_info = {
            'company': 'PT Teknologi Nusantara',
            'employee': 'Budi Santoso',
            'position': 'IT Manager',
            'email': 'budi@teknologi.id',
            'phone': '021-555-1234',
            'hobbies': ['badminton', 'tech news', 'coffee'],
            'social_media': {
                'linkedin': 'linkedin.com/in/budi',
                'facebook': 'facebook.com/budi.s',
                'instagram': '@budi_tech'
            },
            'recent_activity': 'Posting tentang masalah server'
        }
        
        self._log("OSINT selesai", self.target_info)
        self._display_info()
        
    def phase2_pretext(self):
        """Phase 2: Membangun kedok/pretext"""
        print(Fore.YELLOW + "\n[PHASE 2] Pretexting - Membangun Kedok")
        
        pretexts = [
            {
                'role': 'Teknisi Server',
                'story': 'Dari tim IT, perlu reset password server',
                'urgency': 'Server akan down dalam 30 menit'
            },
            {
                'role': 'Vendor Software',
                'story': 'Update keamanan wajib untuk semua admin',
                'urgency': 'Batas akhir hari ini'
            },
            {
                'role': 'Rekan Kerja',
                'story': f"Dari {self.target_info['position']}, {self.target_info['employee']} minta bantuan",
                'urgency': 'Sekarang'
            }
        ]
        
        chosen = random.choice(pretexts)
        print(Fore.MAGENTA + f"\n📞 Skenario yang dibangun:")
        print(Fore.WHITE + f"  Role    : {chosen['role']}")
        print(Fore.WHITE + f"  Story   : {chosen['story']}")
        print(Fore.WHITE + f"  Urgensi : {chosen['urgency']}")
        
        self.target_info['pretext'] = chosen
        self._log("Pretext dibuat", chosen)
        
    def phase3_manipulation(self):
        """Phase 3: Manipulasi psikologis"""
        print(Fore.YELLOW + "\n[PHASE 3] Psychological Manipulation")
        
        techniques = [
            ("Authority", "Mengaku sebagai atasan/otoritas"),
            ("Urgency", "Menciptakan situasi darurat"),
            ("Reciprocity", "Menawarkan bantuan gratis"),
            ("Liking", "Membangun hubungan baik"),
            ("Social Proof", "Mengatakan semua sudah melakukannya"),
            ("Scarcity", "Kesempatan terbatas")
        ]
        
        print(Fore.CYAN + "\nTeknik yang digunakan:")
        for tech, desc in techniques:
            print(Fore.BLUE + f"  • {tech:12}: {desc}")
            time.sleep(0.5)
            
        # Simulasi percakapan telepon
        self._simulate_call()
        
    def _simulate_call(self):
        """Simulasi percakapan telepon"""
        print(Fore.YELLOW + "\n📞 SIMULASI PERCAKAPAN TELEPON:")
        
        conversation = [
            ("Hacker", "Halo, dengan Bapak Budi Santoso?"),
            ("Target", "Ya, benar. Ada yang bisa dibantu?"),
            ("Hacker", "Saya dari tim IT, pak. Ada masalah dengan server, perlu bantuan Bapak."),
            ("Target", "Masalah apa?"),
            ("Hacker", "Server akan restart otomatis, tapi perlu verifikasi akses admin dulu."),
            ("Target", "Oh, akses admin server ya?"),
            ("Hacker", "Iya pak, sebentar saja. Username dan password untuk login."),
            ("Target", "Username admin, passwordnya P@ssw0rd123"),
            ("Hacker", "Terima kasih pak, sudah kami proses. Nanti kami kabari.")
        ]
        
        for speaker, text in conversation:
            if speaker == "Hacker":
                print(Fore.RED + f"  🕵️ {speaker}: {text}")
            else:
                print(Fore.GREEN + f"  👤 {speaker}: {text}")
            time.sleep(1)
            
    def phase4_extraction(self):
        """Phase 4: Ekstraksi data"""
        print(Fore.YELLOW + "\n[PHASE 4] Data Extraction")
        
        extracted = {
            'username': 'administrator',
            'password': 'P@ssw0rd123',
            'server_ip': '192.168.1.100',
            'database': 'company_db',
            'access_level': 'Super Admin'
        }
        
        print(Fore.RED + """
╔══════════════════════════════════════════════════════════╗
║              DATA BERHASIL DIEKSTRAK                     ║
╠══════════════════════════════════════════════════════════╣
        """)
        
        for key, value in extracted.items():
            print(Fore.WHITE + f"║ {key.upper():15}: {value:<30} ║")
            
        print(Fore.RED + "╚══════════════════════════════════════════════════════════╝")
        
        self.target_info['extracted'] = extracted
        self._log("Data diekstrak", extracted)
        
    def _display_info(self):
        """Tampilkan informasi target"""
        print(Fore.CYAN + "\nInformasi Target Terkumpul:")
        for key, value in self.target_info.items():
            if key not in ['pretext', 'extracted']:
                print(Fore.WHITE + f"  {key.replace('_', ' ').title():15}: {value}")
                
    def _log(self, stage, data):
        """Catat ke file log"""
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n[{timestamp}] {stage}\n")
            f.write(json.dumps(data, indent=2))
            f.write("\n" + "="*50 + "\n")
            
    def run(self):
        """Jalankan semua fase"""
        self.banner()
        print(Fore.WHITE + f"\nTarget: {self.target_info.get('employee', 'Unknown')}")
        print(Fore.WHITE + f"Waktu : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.phase1_osint()
        input(Fore.YELLOW + "\nTekan Enter untuk lanjut ke Phase 2...")
        
        self.phase2_pretext()
        input(Fore.YELLOW + "\nTekan Enter untuk lanjut ke Phase 3...")
        
        self.phase3_manipulation()
        input(Fore.YELLOW + "\nTekan Enter untuk lanjut ke Phase 4...")
        
        self.phase4_extraction()
        
        print(Fore.GREEN + """
╔══════════════════════════════════════════════════════════╗
║                    SIMULASI SELESAI                       ║
║     Pelajaran: Jangan pernah percaya telepon asing!      ║
╚══════════════════════════════════════════════════════════╝
        """)

if __name__ == "__main__":
    simulator = KevinMitnickSimulator()
    simulator.run()