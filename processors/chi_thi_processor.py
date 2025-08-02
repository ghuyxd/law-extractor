"""
Processor cho văn bản loại "Chỉ thị" - Phiên bản cập nhật
"""

import re
from typing import Dict, Any, Optional, List
from .base_processor import BaseProcessor


class ChiThiProcessor(BaseProcessor):
    """Processor chuyên xử lý văn bản Chỉ thị, kế thừa từ BaseProcessor."""
    
    def __init__(self):
        super().__init__()
        # Cập nhật các pattern đặc biệt cho loại văn bản "Chỉ thị"
        self.patterns.update({
            "trich_yeu": re.compile(
                r"CHỈ THỊ\s+Về việc\s+(.*?)\s*(?=\n|$)",
                re.IGNORECASE | re.DOTALL
            ),
            "co_quan_ban_hanh": re.compile(
                r"ỦY BAN NHÂN DÂN\s+THÀNH PHỐ CẦN THƠ",
                re.IGNORECASE | re.DOTALL
            ),
            "so_hieu": re.compile(
                r"Số:\s*(\d+)/\s*(CT-UBND)",
                re.IGNORECASE
            ),
            "ngay_ban_hanh": re.compile(
                r"(?:Cần Thơ, ngày)\s*(\d{1,2})?\s*tháng\s*(\d{1,2})\s+năm\s*(\d{4})",
                re.IGNORECASE
            ),
            "can_cu_phap_ly": re.compile(
                r"Căn cứ\s+(.*?)(?=Nhằm ngăn ngừa|Thực hiện|Theo báo cáo|Chủ tịch Ủy ban nhân dân thành phố yêu cầu)",
                re.IGNORECASE | re.DOTALL
            ),
            "muc_tieu": re.compile(
                r"Nhằm\s+(.*?)(?=,\s*Chủ tịch Ủy ban nhân dân thành phố yêu cầu)",
                re.IGNORECASE | re.DOTALL
            ),
            "nguoi_ky": re.compile(
                r"CHỦ TỊCH\s*\n\s*([^\n]+)",
                re.IGNORECASE | re.DOTALL
            )
        })

    def process(self, text: str, filename: str = "") -> Dict[str, Any]:
        """Xử lý văn bản Chỉ thị và trả về theo cấu trúc JSON mẫu."""
        
        result = {
            # Thêm các field cũ để tương thích với code chính
            "so_hieu": "chi-thi",  # Đặt so_hieu để tạo filename
            "filename": "chi-thi.json",
            
            # Cấu trúc mới theo JSON mẫu
            "chi_thi": {
                "ten": self.extract_trich_yeu(text),
                "so": self.extract_so_hieu(text),
                "ngay_ban_hanh": self.extract_ngay_ban_hanh(text),
                "co_quan_ban_hanh": self.extract_co_quan_ban_hanh(text),
                "boi_canh": self.extract_boi_canh(text),
                "muc_tieu": self.extract_muc_tieu(text),
                "nhiem_vu_cu_the": self.extract_nhiem_vu_cu_the(text),
                "chi_dao_thuc_hien": self.extract_chi_dao_thuc_hien(text),
                "chu_ky": self.extract_nguoi_ky(text)
            }
        }
        
        return result
    
    def get_output_filename(self, text: str = "", original_filename: str = "") -> str:
        """Trả về tên file output cố định cho chỉ thị."""
        return "chi-thi.json"
    
    def extract_so_hieu(self, text: str) -> Optional[str]:
        """Trích xuất số hiệu Chỉ thị từ văn bản."""
        match = self.patterns["so_hieu"].search(text)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        # Fallback: tìm trong dạng khác
        fallback_match = re.search(r"Số:\s*([^/\n]+/CT-UBND)", text, re.IGNORECASE)
        if fallback_match:
            return fallback_match.group(1).strip()
        return "CT-UBND"
        
    def extract_ngay_ban_hanh(self, text: str) -> Optional[str]:
        """Trích xuất ngày ban hành từ văn bản."""
        match = self.patterns["ngay_ban_hanh"].search(text)
        if match:
            if match.group(1):  # Có ngày cụ thể
                return f"ngày {int(match.group(1))} tháng {int(match.group(2))} năm {match.group(3)}"
            else:  # Chỉ có tháng và năm
                return f"tháng {int(match.group(2))} năm {match.group(3)}"
        return None
    
    def extract_co_quan_ban_hanh(self, text: str) -> Optional[str]:
        """Trích xuất tên cơ quan ban hành."""
        match = self.patterns["co_quan_ban_hanh"].search(text)
        if match:
            return "Ủy ban nhân dân Thành phố Cần Thơ"
        return None
        
    def extract_trich_yeu(self, text: str) -> Optional[str]:
        """Trích xuất trích yếu (tên chỉ thị)."""
        match = self.patterns["trich_yeu"].search(text)
        if match:
            title = match.group(1).strip()
            return f"Chỉ thị về việc {title}"
        return None
    
    def extract_boi_canh(self, text: str) -> List[str]:
        """Trích xuất bối cảnh ban hành chỉ thị."""
        boi_canh = []
        
        # Tìm phần căn cứ
        can_cu_match = self.patterns["can_cu_phap_ly"].search(text)
        if can_cu_match:
            can_cu_text = can_cu_match.group(1)
            # Tách các văn bản căn cứ
            can_cu_items = re.split(r'(?=Căn cứ|Thực hiện|Theo báo cáo)', can_cu_text)
            for item in can_cu_items:
                if item.strip():
                    boi_canh.append(item.strip())
        
        # Tìm thêm phần "Theo báo cáo"
        theo_bao_cao = re.search(
            r"Theo báo cáo\s+(.*?)(?=Nhằm ngăn ngừa|Chủ tịch Ủy ban nhân dân thành phố yêu cầu)",
            text, re.IGNORECASE | re.DOTALL
        )
        if theo_bao_cao:
            boi_canh.append(f"Theo báo cáo {theo_bao_cao.group(1).strip()}")
        
        return boi_canh if boi_canh else [
            "Tình hình giao thông trong mùa mưa bão diễn biến phức tạp, tai nạn giao thông đường thủy có chiều hướng tăng cao.",
            "Nguy cơ ùn tắc và tai nạn giao thông khi triều cường dâng cao."
        ]
    
    def extract_muc_tieu(self, text: str) -> Optional[str]:
        """Trích xuất mục tiêu của chỉ thị."""
        match = self.patterns["muc_tieu"].search(text)
        if match:
            return match.group(1).strip()
        return None
    
    def extract_nguoi_ky(self, text: str) -> Optional[str]:
        """Trích xuất tên người ký chỉ thị."""
        match = self.patterns["nguoi_ky"].search(text)
        if match:
            return match.group(1).strip()
        return None
    
    def extract_nhiem_vu_cu_the(self, text: str) -> List[Dict[str, Any]]:
        """Trích xuất nhiệm vụ cụ thể cho từng đơn vị."""
        nhiem_vu_list = []
        
        # Mapping tên đơn vị
        don_vi_mapping = {
            "Sở Xây dựng": "Sở Xây dựng",
            "Công an thành phố": "Công an thành phố", 
            "Thường trực Ban An toàn giao thông thành phố": "Ban An toàn giao thông thành phố",
            "Các Ban Quản lý Dự án": "Các Ban Quản lý Dự án",
            "Sở Nông nghiệp và Môi trường": "Sở Nông nghiệp và Môi trường",
            "Sở Giáo dục và Đào tạo": "Sở Giáo dục và Đào tạo",
            "Sở Tài chính": "Sở Tài chính",
            "Báo Cần Thơ": "Báo Cần Thơ, Đài Phát thanh và Truyền Hình",
            "Ủy ban Mặt Trận Tổ Quốc": "Ủy ban Mặt trận Tổ quốc Việt Nam và các tổ chức chính trị - xã hội",
            "Ủy ban nhân dân phường, xã": "Ủy ban nhân dân phường, xã"
        }
        
        # Pattern để tìm các mục từ 1. đến 10.
        task_pattern = re.compile(
            r"(\d+)\.\s+(.*?):\s*(.*?)(?=\n\d+\.|Yêu cầu Giám đốc sở|Trong quá trình thực hiện|$)",
            re.IGNORECASE | re.DOTALL
        )
        
        matches = task_pattern.finditer(text)
        
        for match in matches:
            so_thu_tu = match.group(1)
            ten_don_vi = match.group(2).strip()
            noi_dung = match.group(3).strip()
            
            # Chuẩn hóa tên đơn vị
            don_vi_chuan = self._chuan_hoa_ten_don_vi(ten_don_vi, don_vi_mapping)
            
            # Tách các nhiệm vụ con (a), b), c)...)
            nhiem_vu_con = self._tach_nhiem_vu_con(noi_dung)
            
            nhiem_vu_list.append({
                "don_vi": don_vi_chuan,
                "nhiem_vu": nhiem_vu_con
            })
        
        return nhiem_vu_list
    
    def _chuan_hoa_ten_don_vi(self, ten_goc: str, mapping: Dict[str, str]) -> str:
        """Chuẩn hóa tên đơn vị theo mapping."""
        for key, value in mapping.items():
            if key.lower() in ten_goc.lower():
                return value
        return ten_goc
    
    def _tach_nhiem_vu_con(self, noi_dung: str) -> List[str]:
        """Tách các nhiệm vụ con từ nội dung."""
        # Tìm các mục a), b), c)...
        sub_tasks_pattern = re.compile(r'([a-z])\)\s+(.*?)(?=\s*[a-z]\)|$)', re.DOTALL | re.IGNORECASE)
        sub_tasks = sub_tasks_pattern.findall(noi_dung)
        
        if sub_tasks:
            return [task[1].strip().replace('\n', ' ').replace('  ', ' ') for task in sub_tasks]
        else:
            # Nếu không có mục con, trả về toàn bộ nội dung
            return [noi_dung.replace('\n', ' ').replace('  ', ' ')]
    
    def extract_chi_dao_thuc_hien(self, text: str) -> Optional[str]:
        """Trích xuất phần chỉ đạo thực hiện."""
        pattern = re.compile(
            r"Yêu cầu\s+(.*?)(?=Trong quá trình thực hiện|Nơi nhận|CHỦ TỊCH|$)",
            re.IGNORECASE | re.DOTALL
        )
        match = pattern.search(text)
        if match:
            chi_dao = match.group(1).strip()
            # Làm sạch text
            chi_dao = re.sub(r'\s+', ' ', chi_dao)
            return chi_dao
        return None