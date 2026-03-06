#!/usr/bin/env python3
"""
Result Saver - Menyimpan hasil serangan ke berbagai format
Author: Yoga Arfiyanto
"""

import json
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd

class ResultSaver:
    """Kelas untuk menyimpan hasil serangan"""
    
    def __init__(self, attack_type: str):
        """
        Args:
            attack_type: Tipe serangan (password_attack, live_cracking, sql_injection)
        """
        self.attack_type = attack_type
        self.base_dir = Path("../results") / attack_type
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def save_json(self, data: Dict, filename: str = None) -> str:
        """
        Simpan hasil dalam format JSON
        
        Args:
            data: Data yang akan disimpan
            filename: Nama file (opsional)
            
        Returns:
            Path ke file yang disimpan
        """
        if filename is None:
            filename = f"result_{self.timestamp}.json"
        else:
            if not filename.endswith('.json'):
                filename += '.json'
                
        filepath = self.base_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Results saved to {filepath}")
        return str(filepath)
        
    def save_csv(self, data: List[Dict], filename: str = None) -> str:
        """
        Simpan hasil dalam format CSV
        
        Args:
            data: List of dictionaries
            filename: Nama file (opsional)
        """
        if filename is None:
            filename = f"result_{self.timestamp}.csv"
        else:
            if not filename.endswith('.csv'):
                filename += '.csv'
                
        filepath = self.base_dir / filename
        
        if data:
            keys = data[0].keys()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
                
        print(f"✅ Results saved to {filepath}")
        return str(filepath)
        
    def save_txt(self, content: str, filename: str = None) -> str:
        """
        Simpan hasil dalam format teks
        
        Args:
            content: String content
            filename: Nama file (opsional)
        """
        if filename is None:
            filename = f"result_{self.timestamp}.txt"
        else:
            if not filename.endswith('.txt'):
                filename += '.txt'
                
        filepath = self.base_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Results saved to {filepath}")
        return str(filepath)
        
    def save_markdown(self, data: Dict, title: str, filename: str = None) -> str:
        """
        Simpan hasil dalam format Markdown
        
        Args:
            data: Data yang akan disimpan
            title: Judul laporan
            filename: Nama file (opsional)
        """
        if filename is None:
            filename = f"report_{self.timestamp}.md"
        else:
            if not filename.endswith('.md'):
                filename += '.md'
                
        filepath = self.base_dir / filename
        
        # Generate markdown
        md_content = f"# {title}\n\n"
        md_content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**Attack Type:** {self.attack_type}\n\n"
        md_content += "---\n\n"
        
        # Add content
        md_content += self._dict_to_markdown(data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(f"✅ Markdown report saved to {filepath}")
        return str(filepath)
        
    def save_html(self, data: Dict, title: str, filename: str = None) -> str:
        """
        Simpan hasil dalam format HTML
        
        Args:
            data: Data yang akan disimpan
            title: Judul laporan
            filename: Nama file (opsional)
        """
        if filename is None:
            filename = f"report_{self.timestamp}.html"
        else:
            if not filename.endswith('.html'):
                filename += '.html'
                
        filepath = self.base_dir / filename
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .header {{ background: #f0f0f0; padding: 10px; border-radius: 5px; }}
        .success {{ color: green; }}
        .error {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Attack Type:</strong> {self.attack_type}</p>
    </div>
    
    <hr>
    
    <div class="content">
        {self._dict_to_html(data)}
    </div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ HTML report saved to {filepath}")
        return str(filepath)
        
    def save_excel(self, data: List[Dict], filename: str = None) -> str:
        """
        Simpan hasil dalam format Excel
        
        Args:
            data: List of dictionaries
            filename: Nama file (opsional)
        """
        try:
            import pandas as pd
            
            if filename is None:
                filename = f"result_{self.timestamp}.xlsx"
            else:
                if not filename.endswith('.xlsx'):
                    filename += '.xlsx'
                    
            filepath = self.base_dir / filename
            
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
            
            print(f"✅ Excel file saved to {filepath}")
            return str(filepath)
            
        except ImportError:
            print("❌ pandas not installed. Install with: pip install pandas openpyxl")
            return None
            
    def _dict_to_markdown(self, data: Any, level: int = 0) -> str:
        """Konversi dictionary ke markdown"""
        md = ""
        
        if isinstance(data, dict):
            for key, value in data.items():
                md += f"{'  ' * level}- **{key}**: "
                if isinstance(value, (dict, list)):
                    md += "\n" + self._dict_to_markdown(value, level + 1)
                else:
                    md += f"{value}\n"
        elif isinstance(data, list):
            for item in data:
                md += f"{'  ' * level}- {self._dict_to_markdown(item, level + 1)}"
        else:
            md += f"{data}\n"
            
        return md
        
    def _dict_to_html(self, data: Any) -> str:
        """Konversi dictionary ke HTML"""
        if isinstance(data, dict):
            html = "<ul>"
            for key, value in data.items():
                html += f"<li><strong>{key}:</strong> "
                if isinstance(value, (dict, list)):
                    html += self._dict_to_html(value)
                else:
                    html += str(value)
                html += "</li>"
            html += "</ul>"
            return html
        elif isinstance(data, list):
            html = "<ul>"
            for item in data:
                html += f"<li>{self._dict_to_html(item)}</li>"
            html += "</ul>"
            return html
        else:
            return str(data)
            
    def list_results(self) -> List[Dict]:
        """List semua hasil yang tersimpan"""
        results = []
        
        for file in self.base_dir.glob("*"):
            if file.is_file():
                stats = file.stat()
                results.append({
                    'filename': file.name,
                    'size': stats.st_size,
                    'modified': datetime.fromtimestamp(stats.st_mtime),
                    'extension': file.suffix
                })
                
        return results

# Contoh penggunaan
if __name__ == "__main__":
    saver = ResultSaver("password_attack")
    
    # Simpan hasil
    data = {
        'hash1': {'status': 'found', 'password': 'admin123'},
        'hash2': {'status': 'found', 'password': 'rahasia123'}
    }
    
    saver.save_json(data, 'test_result')

