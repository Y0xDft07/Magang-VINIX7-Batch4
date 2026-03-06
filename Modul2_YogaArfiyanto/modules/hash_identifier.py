#!/usr/bin/env python3
"""
Hash Identifier - Mengidentifikasi tipe hash berdasarkan panjang dan pola
Author: Yoga Arfiyanto
"""

import re
import hashlib

class HashIdentifier:
    """Kelas untuk mengidentifikasi tipe hash"""
    
    def __init__(self):
        self.hash_patterns = {
            'MD5': {
                'length': 32,
                'pattern': r'^[a-fA-F0-9]{32}$',
                'description': 'Message Digest Algorithm 5'
            },
            'SHA-1': {
                'length': 40,
                'pattern': r'^[a-fA-F0-9]{40}$',
                'description': 'Secure Hash Algorithm 1'
            },
            'SHA-224': {
                'length': 56,
                'pattern': r'^[a-fA-F0-9]{56}$',
                'description': 'SHA-224'
            },
            'SHA-256': {
                'length': 64,
                'pattern': r'^[a-fA-F0-9]{64}$',
                'description': 'SHA-256'
            },
            'SHA-384': {
                'length': 96,
                'pattern': r'^[a-fA-F0-9]{96}$',
                'description': 'SHA-384'
            },
            'SHA-512': {
                'length': 128,
                'pattern': r'^[a-fA-F0-9]{128}$',
                'description': 'SHA-512'
            },
            'MySQL': {
                'length': 41,
                'pattern': r'^\*[a-fA-F0-9]{40}$',
                'description': 'MySQL password hash'
            },
            'NTLM': {
                'length': 32,
                'pattern': r'^[a-fA-F0-9]{32}$',
                'description': 'Windows NTLM hash'
            },
            'LM': {
                'length': 32,
                'pattern': r'^[a-fA-F0-9]{32}$',
                'description': 'Windows LM hash'
            },
            'bcrypt': {
                'pattern': r'^\$2[aby]\$[0-9]{2}\$[./A-Za-z0-9]{53}$',
                'description': 'bcrypt hash'
            }
        }
        
    def identify(self, hash_string):
        """
        Identifikasi tipe hash berdasarkan string
        
        Args:
            hash_string (str): Hash yang akan diidentifikasi
            
        Returns:
            str: Tipe hash yang teridentifikasi
        """
        hash_string = hash_string.strip()
        length = len(hash_string)
        
        # Cek berdasarkan pola regex
        for hash_type, info in self.hash_patterns.items():
            if 'pattern' in info:
                if re.match(info['pattern'], hash_string):
                    return hash_type
                    
        # Cek berdasarkan panjang
        for hash_type, info in self.hash_patterns.items():
            if info.get('length') == length:
                return hash_type
                
        return 'Unknown'
        
    def get_all_info(self, hash_string):
        """
        Dapatkan semua informasi tentang hash
        
        Args:
            hash_string (str): Hash yang akan dianalisis
            
        Returns:
            dict: Informasi lengkap hash
        """
        hash_type = self.identify(hash_string)
        
        return {
            'hash': hash_string,
            'length': len(hash_string),
            'type': hash_type,
            'description': self.hash_patterns.get(hash_type, {}).get('description', 'Unknown hash type'),
            'possible_algorithms': self._get_possible_algorithms(hash_string)
        }
        
    def _get_possible_algorithms(self, hash_string):
        """Dapatkan kemungkinan algoritma untuk hash"""
        length = len(hash_string)
        
        algorithms = []
        for algo, info in self.hash_patterns.items():
            if info.get('length') == length:
                algorithms.append(algo)
                
        return algorithms
        
    def is_valid_hash(self, hash_string):
        """Cek apakah string adalah hash yang valid"""
        hash_string = hash_string.strip()
        # Cek apakah hanya mengandung karakter hex
        return bool(re.match(r'^[a-fA-F0-9]+$', hash_string))
        
    def detect_encoding(self, hash_string):
        """Deteksi encoding hash (hex, base64, dll)"""
        if re.match(r'^[a-fA-F0-9]+$', hash_string):
            return 'hex'
        elif re.match(r'^[a-zA-Z0-9+/]+=*$', hash_string):
            return 'base64'
        else:
            return 'unknown'

# Contoh penggunaan
if __name__ == "__main__":
    identifier = HashIdentifier()
    
    # Test dengan hash dari tugas
    test_hashes = [
        '9B19C083DF8E73507433F0862CCAAB803582BE52',
        '4282EBBDFCFC22D59DAB2ED46BF18F831BCD327B12A3238D8C7607D8F093565327D8754E4390F276B06B8EC4EB3931ED9',
        '5f4dcc3b5aa765d61d8327deb882cf99'
    ]
    
    for h in test_hashes:
        result = identifier.get_all_info(h)
        print(f"Hash: {result['hash'][:30]}...")
        print(f"Type: {result['type']}")
        print(f"Desc: {result['description']}")
        print("-" * 50)
