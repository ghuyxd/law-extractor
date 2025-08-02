"""
Factory để tạo các extractor phù hợp
"""
from typing import Optional
from .base_extractor import BaseExtractor
from .law_extractor import LawExtractor
from .decree_extractor import DecreeExtractor
from .resolution_extractor import ResolutionExtractor
# from .decision_extractor import DecisionExtractor
# from .circular_extractor import CircularExtractor
from .other_extractors import (
    DirectiveExtractor, ConclusionExtractor, GuidanceExtractor,
    OfficialLetterExtractor, ReportExtractor, PlanExtractor,
    RegulationExtractor, NotificationExtractor
)

class ExtractorFactory:
    """Factory class để tạo các extractor"""
    
    def __init__(self):
        self._extractors = {
            'luật': LawExtractor,
            'nghị_định': DecreeExtractor,
            'nghị_quyết': ResolutionExtractor,
            # 'quyết_định': DecisionExtractor,
            # 'thông_tư': CircularExtractor,
            'chỉ_thị': DirectiveExtractor,
            'kết_luận': ConclusionExtractor,
            'hướng_dẫn': GuidanceExtractor,
            'công_văn': OfficialLetterExtractor,
            'báo_cáo': ReportExtractor,
            'kế_hoạch': PlanExtractor,
            'phương_án': PlanExtractor,  # Sử dụng chung với kế hoạch
            'quy_định': RegulationExtractor,
            'quy_chế': RegulationExtractor,  # Sử dụng chung với quy định
            'pháp_lệnh': LawExtractor,  # Sử dụng chung với luật
            'thông_báo': NotificationExtractor,
            'đề_án': PlanExtractor,  # Sử dụng chung với kế hoạch
            'văn_bản_hợp_nhất': LawExtractor,  # Sử dụng chung với luật
            'quy_chuẩn_việt_nam': RegulationExtractor,  # Sử dụng chung với quy định
            # 'thông_tư_liên_tịch': CircularExtractor,  # Sử dụng chung với thông tư
            'công_điện': OfficialLetterExtractor,  # Sử dụng chung với công văn
            # 'lệnh': DecisionExtractor  # Sử dụng chung với quyết định
        }
    
    def get_extractor(self, document_type: str) -> Optional[BaseExtractor]:
        """Lấy extractor phù hợp với loại văn bản"""
        extractor_class = self._extractors.get(document_type.lower())
        if extractor_class:
            return extractor_class()
        return None
    
    def get_available_types(self) -> list[str]:
        """Lấy danh sách các loại văn bản được hỗ trợ"""
        return list(self._extractors.keys())