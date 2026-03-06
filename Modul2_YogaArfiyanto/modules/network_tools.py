#!/usr/bin/env python3
"""
Network Tools - Tools untuk analisis jaringan
Author: Yoga Arfiyanto
"""

import socket
import requests
import subprocess
from typing import Dict, List, Optional
from urllib.parse import urlparse

class NetworkTools:
    """Kelas untuk tools jaringan"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_ip_info(self, domain: str) -> Dict:
        """
        Dapatkan informasi IP dari domain
        
        Args:
            domain: Domain target
            
        Returns:
            Dict: Informasi IP
        """
        try:
            ip = socket.gethostbyname(domain)
            
            # Reverse DNS
            try:
                hostname, _, _ = socket.gethostbyaddr(ip)
            except:
                hostname = None
                
            return {
                'domain': domain,
                'ip': ip,
                'hostname': hostname,
                'port_scan': self.scan_common_ports(ip)
            }
        except Exception as e:
            return {'error': str(e)}
            
    def scan_common_ports(self, target: str, ports: List[int] = None) -> Dict:
        """
        Scan port umum
        
        Args:
            target: IP atau domain target
            ports: List port yang akan discan
        """
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 
                    993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
                    
        results = {}
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = 'unknown'
                    
                results[port] = {
                    'status': 'open',
                    'service': service
                }
            sock.close()
            
        return results
        
    def check_website_status(self, url: str) -> Dict:
        """
        Cek status website
        
        Args:
            url: URL website
            
        Returns:
            Dict: Status website
        """
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            return {
                'url': url,
                'status_code': response.status_code,
                'reason': response.reason,
                'headers': dict(response.headers),
                'server': response.headers.get('Server', 'Unknown'),
                'technologies': self.detect_technologies(response.text, response.headers),
                'response_time': response.elapsed.total_seconds()
            }
        except requests.exceptions.ConnectionError:
            return {'error': 'Connection failed'}
        except requests.exceptions.Timeout:
            return {'error': 'Timeout'}
        except Exception as e:
            return {'error': str(e)}
            
    def detect_technologies(self, html: str, headers: Dict) -> List[str]:
        """Deteksi teknologi yang digunakan website"""
        tech = []
        
        # Server header
        if 'server' in headers:
            tech.append(f"Server: {headers['server']}")
            
        # Framework detection
        frameworks = {
            'laravel': 'csrf-token',
            'django': 'csrftoken',
            'wordpress': 'wp-content',
            'joomla': 'com_content',
            'php': 'php',
            'asp.net': 'asp.net',
            'rails': 'csrf-param'
        }
        
        for name, pattern in frameworks.items():
            if pattern.lower() in html.lower():
                tech.append(name)
                
        return tech
        
    def whois_lookup(self, domain: str) -> Dict:
        """
        WHOIS lookup untuk domain
        (Simplified version)
        """
        try:
            # Coba dengan whois command line
            result = subprocess.run(['whois', domain], 
                                   capture_output=True, text=True, timeout=10)
            
            lines = result.stdout.split('\n')
            info = {}
            
            important_fields = ['Domain Name', 'Registrar', 'Creation Date', 
                               'Expiry Date', 'Name Server']
                               
            for line in lines:
                for field in important_fields:
                    if line.startswith(field):
                        info[field] = line.split(':')[1].strip()
                        
            return info
        except:
            return {'error': 'WHOIS lookup failed'}
            
    def check_ssl(self, domain: str) -> Dict:
        """
        Cek SSL certificate
        """
        import ssl
        import datetime
        
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.connect((domain, 443))
                cert = s.getpeercert()
                
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (not_after - datetime.datetime.now()).days
                
                return {
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'subject': dict(x[0] for x in cert['subject']),
                    'version': cert['version'],
                    'expires': cert['notAfter'],
                    'days_left': days_left,
                    'valid': days_left > 0
                }
        except:
            return {'error': 'SSL check failed'}

# Contoh penggunaan
if __name__ == "__main__":
    tools = NetworkTools()
    
    # Cek target
    result = tools.check_website_status("https://target.rootbrain.com")
    print(f"Status: {result.get('status_code')}")
    print(f"Server: {result.get('server')}")

