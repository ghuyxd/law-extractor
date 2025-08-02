"""
Processor cho văn bản loại "Lệnh"
"""

import re
from typing import Dict, Any, Optional
from .base_processor import BaseProcessor


class LenhProcessor(BaseProcessor):
    """Processor chuyên xử lý văn bản Lệnh"""
    
    def __init__(self):
        super().__init__()
        self.patterns.update({
            'co_quan_ban_hanh': r'(CHỦ TỊCH\s*NƯỚC[^\n]*)',
            'van_ban_cong_bo': r'(?:NAY CÔNG BỐ:|CÔNG BỐ:)\s*\n?\s*([^\n]+(?:\n[^\n]+)*?)(?=\s*Đã được)',
            'co_quan_thong_qua': r'Đã được\s+([^,]+),?\s*([^,]*),?\s*([^,]*)\s*thông qua',
            'ngay_thong_qua': r'thông qua\s+ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})',
        })
    
    def process(self, text: str, filename: str = "") -> Dict[str, Any]:
        """Xử lý văn bản Lệnh"""
        
        result = {
            "ten_van_ban": "Lệnh",
            "so_hieu": self.extract_so_hieu(text),
            "ngay_ban_hanh": self.extract_ngay_ban_hanh(text),
            "co_quan_ban_hanh": self.extract_co_quan_ban_hanh(text),
            "nguoi_ky": self.extract_nguoi_ky(text),
            "trich_yeu": self.extract_trich_yeu(text),
            "can_cu_phap_ly": self.extract_can_cu_phap_ly(text),
            "van_ban_duoc_cong_bo": self.extract_van_ban_duoc_cong_bo(text),
            "thong_tin_cong_bao": self.extract_thong_tin_cong_bao(text),
            "thong_tin_ky_so": self.extract_thong_tin_ky_so(text)
        }
        
        return result
    
    def extract_co_quan_ban_hanh(self, text: str) -> Optional[str]:
        """Trích xuất cơ quan ban hành cho Lệnh"""
        patterns = [
            r'(CHỦ TỊCH\s*NƯỚC\s*CỘNG\s*HÒA\s*XÃ\s*HỘI\s*CHỦ\s*NGHĨA\s*VIỆT\s*NAM)',
            r'(CHỦ TỊCH\s*NƯỚC[^\n]*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Chủ tịch nước Cộng hòa xã hội chủ nghĩa Việt Nam"
    
    def extract_trich_yeu(self, text: str) -> Optional[str]:
        """Trích xuất trích yếu cho Lệnh"""
        patterns = [
            r'LỆNH\s*\n\s*([^\n]+(?:\n[^\n]+)*?)(?=\s*CHỦ TỊCH)',
            r'Số:\s*[^\n]+\s*\n[^\n]*\n\s*LỆNH\s*\n\s*([^\n]+(?:\n[^\n]+)*?)(?=\s*CHỦ TỊCH)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                trich_yeu = match.group(1).strip()
                # Loại bỏ các dòng trống và chuẩn hóa
                trich_yeu = re.sub(r'\s+', ' ', trich_yeu)
                return trich_yeu
        
        return None
    
    def extract_van_ban_duoc_cong_bo(self, text: str) -> Dict[str, Any]:
        """Trích xuất thông tin văn bản được công bố trong Lệnh"""
        result = {}
        
        # Tìm tên văn bản được công bố
        van_ban_pattern = r'(?:NAY CÔNG BỐ:|CÔNG BỐ:)\s*\n?\s*([^\n]+(?:\n[^\n]+)*?)(?=\s*Đã được)'
        match = re.search(van_ban_pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            result['ten'] = match.group(1).strip()
        
        # Tìm cơ quan thông qua
        co_quan_pattern = r'Đã được\s+([^,\n]+(?:,[^,\n]+)*?)\s+(?:khóa|thông qua)'
        match = re.search(co_quan_pattern, text, re.IGNORECASE)
        if match:
            co_quan_text = match.group(1).strip()
            
            # Tách cơ quan và khóa
            if 'khóa' in co_quan_text.lower():
                parts = re.split(r'\s+khóa\s+', co_quan_text, flags=re.IGNORECASE)
                if len(parts) >= 2:
                    result['co_quan_thong_qua'] = parts[0].strip()
                    # Tìm thông tin khóa và kỳ họp
                    khoa_ky_pattern = r'khóa\s+([^,\s]+)(?:,\s*([^,\n]+))?'
                    khoa_match = re.search(khoa_ky_pattern, co_quan_text, re.IGNORECASE)
                    if khoa_match:
                        khoa = khoa_match.group(1).strip()
                        result['co_quan_thong_qua'] = f"{result['co_quan_thong_qua']} khóa {khoa}"
                        if khoa_match.group(2):
                            result['ky_hop'] = khoa_match.group(2).strip()
            else:
                result['co_quan_thong_qua'] = co_quan_text
        
        # Tìm ngày thông qua
        ngay_pattern = r'thông qua\s+ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})'
        match = re.search(ngay_pattern, text, re.IGNORECASE)
        if match:
            day, month, year = match.groups()
            result['ngay_thong_qua'] = f"{day.zfill(2)}/{month.zfill(2)}/{year}"
        
        return result