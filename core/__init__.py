# core/__init__.py
"""
Core components cho hệ thống xử lý văn bản pháp luật
"""
from .processor import LegalDocumentProcessor
from .config import setup_logging

__all__ = ['LegalDocumentProcessor', 'setup_logging']