#!/usr/bin/env python3
"""
Wordlist Manager - Mengelola wordlist untuk cracking
Author: Yoga Arfiyanto
"""

import os
import requests
import gzip
import shutil
from pathlib import Path
from typing import List, Optional

class WordlistManager:
    """Kelas untuk mengelola wordlist"""
    
    def __init__(self, wordlist_dir: str = "../wordlists"):
        self.wordlist_dir = Path(wordlist_dir)
        self.wordlist_dir.mkdir(parents=True, exist_ok=True)
        
        self.default_wordlists = {
            'indonesian': {
                'url': 'https://raw.githubusercontent.com/mychaelgo/indonesia-wordlist/master/indonesian.txt',
                'filename': 'indonesian.txt',
                'description': 'Wordlist Bahasa Indonesia'
            },
            'rockyou': {
                'url': 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt',
                'filename': 'rockyou.txt',
                'description': 'RockYou wordlist (popular)'
            },
            'common_passwords': {
                'url': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt',
                'filename': 'common_passwords.txt',
                'description': 'Top 10000 common passwords'
            },
            'common_usernames': {
                'url': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt',
                'filename': 'common_usernames.txt',
                'description': 'Common usernames'
            }
        }
        
    def download_wordlist(self, wordlist_key: str) -> bool:
        """
        Download wordlist dari sumber
        
        Args:
            wordlist_key: Key dari self.default_wordlists
            
        Returns:
            bool: True jika berhasil
        """
        if wordlist_key not in self.default_wordlists:
            print(f"Wordlist {wordlist_key} tidak ditemukan")
            return False
            
        info = self.default_wordlists[wordlist_key]
        url = info['url']
        filename = self.wordlist_dir / info['filename']
        
        print(f"Downloading {info['description']}...")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Progress bar sederhana
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\rProgress: {progress:.1f}%", end='')
                            
            print(f"\n✅ Downloaded to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error downloading: {e}")
            return False
            
    def download_all_defaults(self):
        """Download semua wordlist default"""
        for key in self.default_wordlists:
            self.download_wordlist(key)
            
    def get_wordlist_path(self, name: str) -> Optional[Path]:
        """
        Dapatkan path ke wordlist
        
        Args:
            name: Nama file wordlist
            
        Returns:
            Path ke file atau None jika tidak ada
        """
        path = self.wordlist_dir / name
        return path if path.exists() else None
        
    def list_wordlists(self) -> List[dict]:
        """List semua wordlist yang tersedia"""
        wordlists = []
        
        for file in self.wordlist_dir.glob("*.txt"):
            stats = file.stat()
            wordlists.append({
                'name': file.name,
                'size': stats.st_size,
                'lines': self._count_lines(file),
                'modified': stats.st_mtime
            })
            
        return wordlists
        
    def _count_lines(self, filepath: Path) -> int:
        """Hitung jumlah baris dalam file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except:
            return 0
            
    def create_custom_wordlist(self, base_words: List[str], output: str, 
                              rules: List[str] = None) -> bool:
        """
        Buat wordlist kustom dari kata dasar
        
        Args:
            base_words: List kata dasar
            output: Nama file output
            rules: List aturan transformasi
        """
        output_path = self.wordlist_dir / "custom" / output
        output_path.parent.mkdir(exist_ok=True)
        
        transformations = {
            'uppercase': lambda w: w.upper(),
            'lowercase': lambda w: w.lower(),
            'capitalize': lambda w: w.capitalize(),
            'reverse': lambda w: w[::-1],
            'leet': lambda w: w.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '5'),
            'append123': lambda w: w + '123',
            'append2023': lambda w: w + '2023',
            'prepend2023': lambda w: '2023' + w,
            'double': lambda w: w * 2
        }
        
        with open(output_path, 'w') as f:
            for word in base_words:
                f.write(word + '\n')
                
                if rules:
                    for rule in rules:
                        if rule in transformations:
                            transformed = transformations[rule](word)
                            f.write(transformed + '\n')
                            
        return True
        
    def merge_wordlists(self, files: List[str], output: str) -> bool:
        """
        Gabungkan beberapa wordlist menjadi satu
        
        Args:
            files: List nama file wordlist
            output: Nama file output
        """
        output_path = self.wordlist_dir / output
        seen = set()
        
        with open(output_path, 'w') as outfile:
            for filename in files:
                filepath = self.wordlist_dir / filename
                if not filepath.exists():
                    print(f"File {filename} tidak ditemukan")
                    continue
                    
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                    for line in infile:
                        word = line.strip()
                        if word and word not in seen:
                            seen.add(word)
                            outfile.write(word + '\n')
                            
        print(f"✅ Merged {len(files)} files -> {len(seen)} unique words")
        return True

# Contoh penggunaan
if __name__ == "__main__":
    manager = WordlistManager()
    
    # List wordlists yang ada
    wordlists = manager.list_wordlists()
    for wl in wordlists:
        print(f"{wl['name']}: {wl['lines']} lines, {wl['size']/1024:.1f} KB")
