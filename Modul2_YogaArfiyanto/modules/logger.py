#!/usr/bin/env python3
"""
Logger - System logging untuk semua aktivitas
Author: Yoga Arfiyanto
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class Logger:
    """Kelas untuk logging system"""
    
    def __init__(self, name: str, log_dir: str = "../logs"):
        """
        Args:
            name: Nama logger
            log_dir: Direktori untuk menyimpan log
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Buat logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Format log
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler untuk semua log
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Error file handler khusus error
        error_file = self.log_dir / f"error_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        
        # Tambahkan handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)
        
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
        
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
        
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
        
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
        
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
        
    def log_attack(self, attack_type: str, target: str, result: dict):
        """
        Log informasi serangan
        
        Args:
            attack_type: Tipe serangan
            target: Target serangan
            result: Hasil serangan
        """
        self.info(f"ATTACK: {attack_type} | Target: {target} | Result: {result}")
        
    def log_success(self, message: str):
        """Log success dengan format khusus"""
        self.logger.info(f"✅ SUCCESS: {message}")
        
    def log_failure(self, message: str):
        """Log failure dengan format khusus"""
        self.logger.error(f"❌ FAILURE: {message}")
        
    def log_progress(self, message: str, current: int, total: int):
        """
        Log progress
        
        Args:
            message: Pesan progress
            current: Nilai saat ini
            total: Nilai total
        """
        percentage = (current / total) * 100 if total > 0 else 0
        self.debug(f"PROGRESS: {message} - {current}/{total} ({percentage:.1f}%)")
        
    def get_recent_logs(self, lines: int = 100) -> str:
        """
        Dapatkan log terbaru
        
        Args:
            lines: Jumlah baris yang diambil
            
        Returns:
            String berisi log terbaru
        """
        log_file = self.log_dir / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
        
        if not log_file.exists():
            return "No logs found"
            
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent = all_lines[-lines:]
                return ''.join(recent)
        except:
            return "Error reading logs"
            
    def archive_old_logs(self, days: int = 7):
        """
        Arsipkan log lama
        
        Args:
            days: Log lebih dari X hari akan diarsipkan
        """
        import shutil
        from datetime import timedelta
        
        archive_dir = self.log_dir / "archive"
        archive_dir.mkdir(exist_ok=True)
        
        cutoff = datetime.now() - timedelta(days=days)
        
        for log_file in self.log_dir.glob("*.log"):
            if log_file.name.startswith("error_"):
                continue  # Skip error logs
                
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime < cutoff:
                # Move to archive
                shutil.move(str(log_file), str(archive_dir / log_file.name))
                self.info(f"Archived: {log_file.name}")

# Singleton instance untuk global logging
_loggers = {}

def get_logger(name: str) -> Logger:
    """
    Dapatkan instance logger
    
    Args:
        name: Nama logger
        
    Returns:
        Logger instance
    """
    if name not in _loggers:
        _loggers[name] = Logger(name)
    return _loggers[name]

# Contoh penggunaan
if __name__ == "__main__":
    log = get_logger("test")
    
    log.info("Starting test...")
    log.debug("Debug message")
    log.warning("Warning message")
    log.error("Error message")
    log.log_attack("SQL Injection", "target.com", {"success": True})
    log.log_success("Attack successful")
