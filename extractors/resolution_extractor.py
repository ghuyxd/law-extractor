"""
Extractor chuyên biệt cho Nghị quyết
"""
from typing import Dict, Any
from .base_extractor import BaseExtractor

class ResolutionExtractor(BaseExtractor):
    """Extractor cho Nghị quyết"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất cấu trúc đặc thù của Nghị quyết"""
        raw_text = document.get('raw_text', '')
        
        # Bắt đầu với cấu trúc chung
        structure = self.extract_common_structure(raw_text)
        
        # Thêm các thành phần đặc thù của Nghị quyết
        structure.update({
            "MucTieu": self.extract_objectives(raw_text),
            "NhiemVuChinh": self.extract_main_tasks(raw_text),
            "GiaiPhap": self.extract_solutions(raw_text),
            "ToChucThucHien": self.extract_organization_implementation(raw_text),
            "TamNhin": self.extract_vision(raw_text),
            "DinhHuong": self.extract_orientations(raw_text)
        })
        
        return structure
    
    def extract_vision(self, text: str) -> list[str]:
        """Trích xuất tầm nhìn"""
        keywords = [
            'tầm\\s+nhìn',
            'viễn\\s+cảnh',
            'định\\s+hướng\\s+phát\\s+triển',
            'chiến\\s+lược'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 3)
    
    def extract_orientations(self, text: str) -> list[str]:
        """Trích xuất định hướng"""
        keywords = [
            'định\\s+hướng',
            'phương\\s+hướng',
            'hướng\\s+phát\\s+triển',
            'quan\\s+điểm'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 5)