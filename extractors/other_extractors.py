"""
Các extractor cho các loại văn bản khác
"""
from typing import Dict, Any
from .base_extractor import BaseExtractor

class DecisionExtractor(BaseExtractor):
    """Extractor cho Quyết định"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "QuyetDinhVe": self.extract_decision_subject(raw_text),
            "ToChucThucHien": self.extract_organization_implementation(raw_text),
            "HieuLuc": self.extract_effectiveness(raw_text)
        })
        return structure
    
    def extract_decision_subject(self, text: str) -> list[str]:
        keywords = ['quyết\\s+định\\s+về', 'về\\s+việc', 'quyết\\s+định']
        return self.text_processor.extract_by_keywords(text, keywords, 3)

class CircularExtractor(BaseExtractor):
    """Extractor cho Thông tư"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "HuongDanThiHanh": self.extract_implementation_guidance(raw_text),
            "HieuLuc": self.extract_effectiveness(raw_text),
            "QuyTrinhThucHien": self.extract_procedures(raw_text)
        })
        return structure
    
    def extract_implementation_guidance(self, text: str) -> list[str]:
        keywords = ['hướng\\s+dẫn\\s+thi\\s+hành', 'hướng\\s+dẫn', 'thực\\s+hiện']
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_procedures(self, text: str) -> list[str]:
        keywords = ['quy\\s+trình', 'thủ\\s+tục', 'các\\s+bước', 'trình\\s+tự']
        return self.text_processor.extract_by_keywords(text, keywords, 6)

class DirectiveExtractor(BaseExtractor):
    """Extractor cho Chỉ thị"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "MucTieuChiDao": self.extract_directive_objectives(raw_text),
            "YeuCauChiDao": self.extract_directive_requirements(raw_text),
            "NhiemVu": self.extract_main_tasks(raw_text),
            "ToChucThucHien": self.extract_organization_implementation(raw_text)
        })
        return structure
    
    def extract_directive_objectives(self, text: str) -> list[str]:
        keywords = ['mục\\s+tiêu\\s+chỉ\\s+đạo', 'chỉ\\s+đạo', 'định\\s+hướng']
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_directive_requirements(self, text: str) -> list[str]:
        keywords = ['yêu\\s+cầu', 'đề\\s+nghị', 'cần']
        return self.text_processor.extract_by_keywords(text, keywords, 8)

class ConclusionExtractor(BaseExtractor):
    """Extractor cho Kết luận"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "KetLuanChinh": self.extract_main_conclusions(raw_text),
            "YeuCau": self.extract_requirements(raw_text),
            "GiaoNhiemVu": self.extract_task_assignments(raw_text)
        })
        return structure
    
    def extract_main_conclusions(self, text: str) -> list[str]:
        return self.text_processor.extract_sections(text)
    
    def extract_requirements(self, text: str) -> list[str]:
        keywords = ['yêu\\s+cầu', 'đề\\s+nghị', 'cần']
        return self.text_processor.extract_by_keywords(text, keywords, 8)
    
    def extract_task_assignments(self, text: str) -> list[str]:
        keywords = ['giao', 'phân\\s+công', 'uỷ\\s+quyền', 'chỉ\\s+định']
        return self.text_processor.extract_by_keywords(text, keywords, 6)

class GuidanceExtractor(BaseExtractor):
    """Extractor cho Hướng dẫn"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "NoiDungHuongDan": self.extract_guidance_content(raw_text),
            "QuyTrinhThucHien": self.extract_procedures(raw_text)
        })
        return structure
    
    def extract_guidance_content(self, text: str) -> list[str]:
        keywords = ['hướng\\s+dẫn', 'nội\\s+dung', 'cách\\s+thức']
        return self.text_processor.extract_by_keywords(text, keywords, 8)
    
    def extract_procedures(self, text: str) -> list[str]:
        keywords = ['quy\\s+trình', 'thủ\\s+tục', 'các\\s+bước', 'trình\\s+tự']
        return self.text_processor.extract_by_keywords(text, keywords, 6)

class OfficialLetterExtractor(BaseExtractor):
    """Extractor cho Công văn"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "NoiDungChinh": self.extract_main_content_sections(raw_text),
            "DeNghi": self.extract_requests_proposals(raw_text),
            "YeuCauPhapHop": self.extract_coordination_requirements(raw_text)
        })
        return structure
    
    def extract_main_content_sections(self, text: str) -> list[str]:
        return self.text_processor.extract_sections(text)
    
    def extract_requests_proposals(self, text: str) -> list[str]:
        keywords = ['đề\\s+nghị', 'kiến\\s+nghị', 'đề\\s+xuất']
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_coordination_requirements(self, text: str) -> list[str]:
        keywords = ['phối\\s+hợp', 'kết\\s+hợp', 'cộng\\s+tác']
        return self.text_processor.extract_by_keywords(text, keywords, 5)

class ReportExtractor(BaseExtractor):
    """Extractor cho Báo cáo"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "CacPhan": self.extract_report_sections(raw_text),
            "KetQuaDatDuoc": self.extract_achievements(raw_text),
            "TonTaiKhoKhan": self.extract_difficulties(raw_text),
            "KienNghiDeXuat": self.extract_recommendations(raw_text)
        })
        return structure
    
    def extract_report_sections(self, text: str) -> list[str]:
        return self.text_processor.extract_numbered_items(text, "phần", 8)
    
    def extract_achievements(self, text: str) -> list[str]:
        keywords = ['kết\\s+quả\\s+đạt\\s+được', 'thành\\s+tựu', 'đã\\s+thực\\s+hiện']
        return self.text_processor.extract_by_keywords(text, keywords, 6)
    
    def extract_difficulties(self, text: str) -> list[str]:
        keywords = ['tồn\\s+tại', 'khó\\s+khăn', 'hạn\\s+chế', 'vướng\\s+mắc']
        return self.text_processor.extract_by_keywords(text, keywords, 6)
    
    def extract_recommendations(self, text: str) -> list[str]:
        keywords = ['kiến\\s+nghị', 'đề\\s+xuất', 'đề\\s+nghị']
        return self.text_processor.extract_by_keywords(text, keywords, 5)

class PlanExtractor(BaseExtractor):
    """Extractor cho Kế hoạch/Phương án/Đề án"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "MucTieu": self.extract_objectives(raw_text),
            "NhiemVu": self.extract_main_tasks(raw_text),
            "GiaiPhap": self.extract_solutions(raw_text),
            "TienDoThucHien": self.extract_schedule(raw_text),
            "ToChucThucHien": self.extract_organization_implementation(raw_text),
            "NguonLuc": self.extract_resources(raw_text)
        })
        return structure
    
    def extract_schedule(self, text: str) -> list[str]:
        keywords = ['tiến\\s+độ', 'lộ\\s+trình', 'thời\\s+gian', 'giai\\s+đoạn']
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_resources(self, text: str) -> list[str]:
        keywords = ['nguồn\\s+lực', 'kinh\\s+phí', 'ngân\\s+sách', 'tài\\s+chính']
        return self.text_processor.extract_by_keywords(text, keywords, 5)

class RegulationExtractor(BaseExtractor):
    """Extractor cho Quy định/Quy chế"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "QuyDinhChung": self.extract_general_provisions(raw_text),
            "QuyDinhCuThe": self.extract_specific_provisions(raw_text),
            "HieuLuc": self.extract_effectiveness(raw_text),
            "TrachNhiemThiHanh": self.extract_implementation_responsibility(raw_text)
        })
        return structure
    
    def extract_specific_provisions(self, text: str) -> list[str]:
        keywords = [
            'quy\\s+định\\s+cụ\\s+thể',
            'quy\\s+định\\s+chi\\s+tiết',
            'điều\\s+kiện'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 6)

class NotificationExtractor(BaseExtractor):
    """Extractor cho Thông báo"""
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        structure.update({
            "NoiDungThongBao": self.extract_notification_content(raw_text),
            "YeuCauThucHien": self.extract_implementation_requirements(raw_text)
        })
        return structure
    
    def extract_notification_content(self, text: str) -> list[str]:
        keywords = ['thông\\s+báo', 'nội\\s+dung', 'thông\\s+tin']
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_implementation_requirements(self, text: str) -> list[str]:
        keywords = ['yêu\\s+cầu\\s+thực\\s+hiện', 'yêu\\s+cầu', 'thực\\s+hiện']
        return self.text_processor.extract_by_keywords(text, keywords, 5)