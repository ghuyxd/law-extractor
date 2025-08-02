"""
Base extractor class cho các loại văn bản pháp luật
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from utils.text_processor import TextProcessor

class BaseExtractor(ABC):
    """Base class cho tất cả các extractor"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
    
    @abstractmethod
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất cấu trúc chuyên biệt cho loại văn bản"""
        pass
    
    def extract_common_structure(self, raw_text: str) -> Dict[str, Any]:
        """Trích xuất cấu trúc chung cho tất cả văn bản"""
        return {
            "VanBanCanCu": self.text_processor.extract_legal_basis(raw_text),
            "CacDieu": self.text_processor.extract_articles(raw_text),
            "CacChuong": self.text_processor.extract_chapters(raw_text)
        }
    
    def extract_objectives(self, text: str) -> List[str]:
        """Trích xuất mục tiêu"""
        keywords = ['mục\\s+tiêu', 'nhằm', 'để']
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_main_tasks(self, text: str) -> List[str]:
        """Trích xuất nhiệm vụ chính"""
        return self.text_processor.extract_sections(text)
    
    def extract_solutions(self, text: str) -> List[str]:
        """Trích xuất giải pháp"""
        keywords = ['giải\\s+pháp', 'biện\\s+pháp', 'cách\\s+thức']
        return self.text_processor.extract_by_keywords(text, keywords, 8)
    
    def extract_organization_implementation(self, text: str) -> List[str]:
        """Trích xuất tổ chức thực hiện"""
        keywords = [
            'tổ\\s+chức\\s+thực\\s+hiện',
            'giao\\s+([^.\\n]+)\\s+chịu\\s+trách\\s+nhiệm',
            'uỷ\\s+ban',
            'bộ'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_effectiveness(self, text: str) -> List[str]:
        """Trích xuất hiệu lực"""
        keywords = [
            'có\\s+hiệu\\s+lực',
            'hiệu\\s+lực\\s+thi\\s+hành',
            'thời\\s+điểm\\s+có\\s+hiệu\\s+lực'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 3)
    
    def extract_implementation_responsibility(self, text: str) -> List[str]:
        """Trích xuất trách nhiệm thi hành"""
        keywords = [
            'trách\\s+nhiệm\\s+thi\\s+hành',
            'chịu\\s+trách\\s+nhiệm',
            'có\\s+trách\\s+nhiệm'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_general_provisions(self, text: str) -> List[str]:
        """Trích xuất quy định chung"""
        keywords = [
            'quy\\s+định\\s+chung',
            'nguyên\\s+tắc',
            'quy\\s+định\\s+cơ\\s+bản'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 5)
    
    def extract_scope_of_regulation(self, text: str) -> List[str]:
        """Trích xuất phạm vi điều chỉnh"""
        keywords = [
            'phạm\\s+vi\\s+điều\\s+chỉnh',
            'luật\\s+này\\s+điều\\s+chỉnh',
            'áp\\s+dụng\\s+đối\\s+với'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 3)
    
    def extract_subjects_of_application(self, text: str) -> List[str]:
        """Trích xuất đối tượng áp dụng"""
        keywords = [
            'đối\\s+tượng\\s+áp\\s+dụng',
            'áp\\s+dụng\\s+đối\\s+với',
            'có\\s+hiệu\\s+lực\\s+đối\\s+với'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 3)
    
    def extract_transitional_final_provisions(self, text: str) -> List[str]:
        """Trích xuất điều khoản tạm thời và cuối"""
        keywords = [
            'điều\\s+khoản\\s+tạm\\s+thời',
            'điều\\s+khoản\\s+cuối',
            'có\\s+hiệu\\s+lực',
            'thay\\s+thế'
        ]
        return self.text_processor.extract_by_keywords(text, keywords, 5)