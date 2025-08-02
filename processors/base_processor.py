"""
Base processor cho các loại văn bản pháp luật
Chứa các phương thức chung để trích xuất thông tin từ văn bản
"""

import re
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    """Lớp cơ sở cho tất cả các processor"""
    
    def __init__(self):
        self.patterns = self._init_patterns()
    
    def _init_patterns(self) -> Dict[str, str]:
        """Khởi tạo các pattern regex chung"""
        return {
            'so_hieu': r'Số:\s*([^\n]+)',
            'ngay_ban_hanh': r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})',
            'nguoi_ky': r'([A-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ\s]+)$',
            'can_cu': r'Căn cứ\s+([^;]+(?:;[^;]+)*)',
            'cong_bao': r'CÔNG BÁO[/\s]*Số:\s*([^\n/]+)/?([^\n/]*)/Ngày\s*([^\n]+)',
            'thoi_gian_ky': r'Thời gian ký:\s*([^\n]+)',
            'co_quan_ky': r'Cơ quan:\s*([^\n]+)',
            'nguoi_ky_dien_tu': r'Người ký:\s*([^\n]+)',
        }
    
    @abstractmethod
    def process(self, text: str, filename: str = "") -> Dict[str, Any]:
        """
        Phương thức chính để xử lý văn bản
        Mỗi processor con phải implement phương thức này
        """
        pass
    
    def extract_so_hieu(self, text: str) -> Optional[str]:
        """Trích xuất số hiệu văn bản"""
        match = re.search(self.patterns['so_hieu'], text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def extract_ngay_ban_hanh(self, text: str) -> Optional[str]:
        """Trích xuất ngày ban hành"""
        match = re.search(self.patterns['ngay_ban_hanh'], text, re.IGNORECASE)
        if match:
            day, month, year = match.groups()
            return f"{day.zfill(2)}/{month.zfill(2)}/{year}"
        return None
    
    def extract_nguoi_ky(self, text: str) -> Optional[str]:
        """Trích xuất người ký"""
        lines = text.strip().split('\n')
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            if line and not re.match(r'^(CHỦ TỊCH|THỦ TƯỚNG|BỘ TRƯỞNG|GIÁM ĐỐC)', line):
                # Kiểm tra xem có phải là tên người không
                if re.match(r'^[A-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ\s]+$', line):
                    return line
        return None
    
    def extract_can_cu_phap_ly(self, text: str) -> List[str]:
        """Trích xuất các căn cứ pháp lý"""
        can_cu_list = []
        
        # Tìm tất cả "Căn cứ"
        can_cu_pattern = r'Căn cứ\s+([^;]+(?:;[^;]+)*?)(?=\s*(?:Căn cứ|NAY|QUYẾT ĐỊNH|CHÍNH PHỦ|CHỦ TỊCH))'
        matches = re.finditer(can_cu_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            can_cu_text = match.group(1).strip()
            # Loại bỏ dấu ";" cuối và split theo ";"
            can_cu_items = [item.strip() for item in can_cu_text.split(';') if item.strip()]
            can_cu_list.extend(can_cu_items)
        
        return can_cu_list
    
    def extract_thong_tin_cong_bao(self, text: str) -> Dict[str, str]:
        """Trích xuất thông tin công báo"""
        match = re.search(self.patterns['cong_bao'], text, re.IGNORECASE)
        if match:
            so = match.group(1).strip()
            so_2 = match.group(2).strip() if match.group(2) else ""
            ngay = match.group(3).strip()
            
            # Xử lý số công báo
            if so_2:
                so_full = f"{so}/{so_2}" if so_2 else so
            else:
                so_full = so
                
            return {
                "so": so_full,
                "ngay": self._format_date(ngay)
            }
        return {}
    
    def extract_thong_tin_ky_so(self, text: str) -> Dict[str, str]:
        """Trích xuất thông tin ký số"""
        result = {}
        
        # Người ký điện tử
        match = re.search(self.patterns['nguoi_ky_dien_tu'], text)
        if match:
            result['nguoi_ky'] = match.group(1).strip()
        
        # Cơ quan
        match = re.search(self.patterns['co_quan_ky'], text)
        if match:
            result['co_quan'] = match.group(1).strip()
        
        # Thời gian ký
        match = re.search(self.patterns['thoi_gian_ky'], text)
        if match:
            result['thoi_gian_ky'] = match.group(1).strip()
        
        return result
    
    def extract_co_quan_ban_hanh(self, text: str) -> Optional[str]:
        """Trích xuất cơ quan ban hành - method này sẽ được override trong các processor con"""
        # Pattern chung cho các chức vụ
        patterns = [
            r'(CHỦ TỊCH NƯỚC[^\n]*)',
            r'(THỦ TƯỚNG[^\n]*)',
            r'(BỘ TRƯỞNG[^\n]*)',
            r'(CHỦ TỊCH[^\n]*)',
            r'(GIÁM ĐỐC[^\n]*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def extract_trich_yeu(self, text: str) -> Optional[str]:
        """Trích xuất trích yếu văn bản"""
        # Pattern chung để tìm tiêu đề sau số hiệu
        patterns = [
            r'Số:\s*[^\n]+\s*\n\s*([^\n]+(?:\n[^\n]+)*?)(?=\s*(?:CHỦ TỊCH|THỦ TƯỚNG|BỘ TRƯỞNG|GIÁM ĐỐC|Căn cứ))',
            r'(?:LỆNH|LUẬT|NGHỊ ĐỊNH|QUYẾT ĐỊNH|THÔNG TƯ|CHỈ THỊ)\s*\n\s*([^\n]+(?:\n[^\n]+)*?)(?=\s*(?:CHỦ TỊCH|THỦ TƯỚNG|BỘ TRƯỞNG|GIÁM ĐỐC|Căn cứ))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _format_date(self, date_str: str) -> str:
        """Chuẩn hóa format ngày tháng"""
        # Xử lý các format khác nhau của ngày tháng
        date_str = date_str.replace('-', '/')
        
        # Pattern để match các format ngày tháng
        patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',
            r'(\d{1,2})-(\d{1,2})-(\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                day, month, year = match.groups()
                return f"{day.zfill(2)}-{month.zfill(2)}-{year}"
        
        return date_str
    
    def clean_text(self, text: str) -> str:
        """Làm sạch văn bản"""
        if not text:
            return ""
        
        # Loại bỏ các ký tự không cần thiết
        text = re.sub(r'\s+', ' ', text)  # Thay nhiều space thành 1
        text = text.strip()
        
        return text
    
    def extract_van_ban_duoc_cong_bo(self, text: str) -> Dict[str, Any]:
        """
        Trích xuất thông tin văn bản được công bố
        Method này sẽ được override trong các processor con
        """
        return {}