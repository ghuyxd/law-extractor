"""
Extractor chuyên biệt cho văn bản Luật
"""
from typing import Dict, Any
from .base_extractor import BaseExtractor

class LawExtractor(BaseExtractor):
    """Extractor cho văn bản Luật"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất cấu trúc đặc thù của Luật"""
        raw_text = document.get('raw_text', '')
        
        # Bắt đầu với cấu trúc chung
        structure = self.extract_common_structure(raw_text)
        
        # Thêm các thành phần đặc thù của Luật
        structure.update({
            "PhamViDieuChinh": self.extract_scope_of_regulation(raw_text),
            "DoiTuongApDung": self.extract_subjects_of_application(raw_text),
            "DieuKhoanTamThoiVaCuoi": self.extract_transitional_final_provisions(raw_text),
            "CacNguyenTac": self.extract_principles(raw_text),
            "ThuatNgu": self.extract_terms_definitions(raw_text)
        })
        
        return structure
    
    def extract_principles(self, text: str) -> list[str]:
        """Trích xuất các nguyên tắc trong Luật"""
        keywords = [
            'nguyên\\s+tắc',
            'cơ\\s+sở',
            'định\\s+hướng',
            'quan\\s+điểm'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_terms_definitions(self, text: str) -> list[str]:
        """Trích xuất thuật ngữ và định nghĩa"""
        keywords = [
            'thuật\\s+ngữ',
            'định\\s+nghĩa',
            'hiểu\\s+là',
            'có\\s+nghĩa\\s+là'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 10)