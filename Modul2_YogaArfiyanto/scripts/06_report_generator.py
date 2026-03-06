#!/usr/bin/env python3
"""
Report Generator - Generate laporan otomatis dari hasil serangan
Author: Yoga Arfiyanto
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.result_saver import ResultSaver
from modules.logger import get_logger

class ReportGenerator:
    """Generate laporan otomatis"""
    
    def __init__(self):
        self.log = get_logger('report')
        self.results_dir = Path("../results")
        self.docs_dir = Path("../docs")
        self.docs_dir.mkdir(exist_ok=True)
        
    def collect_results(self) -> dict:
        """Kumpulkan semua hasil dari folder results"""
        results = {
            'password_attack': [],
            'live_cracking': [],
            'sql_injection': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Collect password attack results
        pass_dir = self.results_dir / 'password_attack'
        if pass_dir.exists():
            for file in pass_dir.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        results['password_attack'].append({
                            'file': file.name,
                            'data': data
                        })
                except:
                    pass
                    
        # Collect live cracking results
        live_dir = self.results_dir / 'live_cracking'
        if live_dir.exists():
            for file in live_dir.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        results['live_cracking'].append({
                            'file': file.name,
                            'data': data
                        })
                except:
                    pass
                    
        # Collect SQL injection results
        sql_dir = self.results_dir / 'sql_injection'
        if sql_dir.exists():
            for file in sql_dir.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        results['sql_injection'].append({
                            'file': file.name,
                            'data': data
                        })
                except:
                    pass
                    
        return results
        
    def generate_markdown_report(self, results: dict) -> str:
        """Generate laporan dalam format Markdown"""
        
        report = f"""# LAPORAN TUGAS MODUL 2 - THREAT MODELLING
## Cyber Security - Yoga Arfiyanto

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 RINGKASAN HASIL

"""
        # Password Attack Summary
        report += "### 🔐 Password Attack\n\n"
        if results['password_attack']:
            for item in results['password_attack']:
                report += f"- **{item['file']}**\n"
                if 'data' in item:
                    for key, value in item['data'].items():
                        report += f"  - {key}: {value}\n"
        else:
            report += "*Belum ada hasil*\n\n"
            
        # Live Cracking Summary
        report += "\n### 🚪 Live Password Cracking\n\n"
        if results['live_cracking']:
            for item in results['live_cracking']:
                report += f"- **{item['file']}**\n"
                if 'data' in item:
                    for key, value in item['data'].items():
                        report += f"  - {key}: {value}\n"
        else:
            report += "*Belum ada hasil*\n\n"
            
        # SQL Injection Summary
        report += "\n### 💉 SQL Injection\n\n"
        if results['sql_injection']:
            for item in results['sql_injection']:
                report += f"- **{item['file']}**\n"
                if 'data' in item:
                    for key, value in item['data'].items():
                        report += f"  - {key}: {value}\n"
        else:
            report += "*Belum ada hasil*\n\n"
            
        return report
        
    def generate_pdf(self, markdown_content: str, output_file: str):
        """Generate PDF dari markdown"""
        try:
            import markdown
            from weasyprint import HTML
            
            # Convert markdown to HTML
            html = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
            
            # Add CSS
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Laporan Modul 2</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
                    h2 {{ color: #34495e; }}
                    h3 {{ color: #2980b9; }}
                    pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
                    code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #3498db; color: white; }}
                </style>
            </head>
            <body>
                {html}
            </body>
            </html>
            """
            
            # Generate PDF
            HTML(string=full_html).write_pdf(output_file)
            return True
            
        except ImportError:
            self.log.warning("Markdown/WeasyPrint not installed. Install with: pip install markdown weasyprint")
            return False
            
    def run(self):
        """Generate semua laporan"""
        self.log.info("Generating reports...")
        
        # Collect results
        results = self.collect_results()
        
        # Generate Markdown
        md_content = self.generate_markdown_report(results)
        
        # Save Markdown
        md_file = self.docs_dir / f"laporan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        self.log.info(f"Markdown report saved: {md_file}")
        
        # Generate PDF
        pdf_file = self.docs_dir / f"laporan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        if self.generate_pdf(md_content, str(pdf_file)):
            self.log.info(f"PDF report saved: {pdf_file}")
        else:
            self.log.warning("PDF generation skipped (dependencies missing)")
            
        # Generate HTML
        html_file = self.docs_dir / f"laporan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(f"""
            <html>
            <head><title>Laporan Modul 2</title>
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                pre {{ background: #f4f4f4; padding: 10px; }}
            </style>
            </head>
            <body>
            <pre>{md_content}</pre>
            </body>
            </html>
            """)
        self.log.info(f"HTML report saved: {html_file}")
        
        print(f"\n✅ Reports generated in {self.docs_dir}")
        print(f"   - Markdown: {md_file.name}")
        print(f"   - HTML: {html_file.name}")
        if pdf_file.exists():
            print(f"   - PDF: {pdf_file.name}")

if __name__ == "__main__":
    generator = ReportGenerator()
    generator.run()

