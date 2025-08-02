"""
Utilities cho xử lý văn bản và trích xuất thông tin
"""
import re
from typing import List, Dict, Any, Optional
from core.config import COMMON_PATTERNS, MIN_CONTENT_LENGTH, EXTRACTION_LIMITS

class TextProcessor:
    """Class xử lý văn bản và trích xuất thông tin cơ bản"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Làm sạch văn bản"""
        if not text:
            return ""
        
        # Thay thế nhiều newline bằng space
        text = re.sub(r'\n+', ' ', text)
        # Thay thế nhiều space bằng một space
        text = re.sub(r'\s+', ' ', text)
        # Loại bỏ space đầu cuối
        return text.strip()
    
    @staticmethod
    def extract_articles(text: str) -> List[str]:
        """Trích xuất các điều từ văn bản"""
        articles = []
        matches = re.findall(COMMON_PATTERNS['article'], text, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            article_num = match[0]
            article_content = TextProcessor.clean_text(match[1])
            if len(article_content) > MIN_CONTENT_LENGTH['default']:
                articles.append(f"Điều {article_num}. {article_content}")
        
        return articles[:EXTRACTION_LIMITS['articles']]
    
    @staticmethod
    def extract_chapters(text: str) -> List[str]:
        """Trích xuất các chương từ văn bản"""
        chapters = []
        matches = re.findall(COMMON_PATTERNS['chapter'], text, re.IGNORECASE)
        
        for match in matches:
            chapter_num = match[0]
            chapter_title = match[1].strip()
            if chapter_title:
                chapters.append(f"CHƯƠNG {chapter_num}. {chapter_title}")
        
        return chapters[:EXTRACTION_LIMITS['chapters']]
    
    @staticmethod
    def extract_legal_basis(text: str) -> List[str]:
        """Trích xuất căn cứ pháp lý"""
        basis_list = []
        matches = re.findall(COMMON_PATTERNS['legal_basis'], text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            basis = match.strip().rstrip(';.,')
            if len(basis) > MIN_CONTENT_LENGTH['legal_basis']:
                basis_list.append(f"Căn cứ {basis};")
        
        return basis_list[:EXTRACTION_LIMITS['legal_basis']]
    
    @staticmethod
    def extract_sections(text: str) -> List[str]:
        """Trích xuất các mục từ văn bản"""
        sections = []
        matches = re.findall(COMMON_PATTERNS['section'], text, re.DOTALL)
        
        for match in matches:
            section_num = match[0]
            section_content = TextProcessor.clean_text(match[1])
            if len(section_content) > MIN_CONTENT_LENGTH['section']:
                sections.append(f"{section_num}. {section_content}")
        
        return sections[:EXTRACTION_LIMITS['sections']]
    
    @staticmethod
    def extract_clauses(text: str) -> List[str]:
        """Trích xuất các khoản từ văn bản"""
        clauses = []
        matches = re.findall(COMMON_PATTERNS['clause'], text, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            clause_letter = match[0]
            clause_content = TextProcessor.clean_text(match[1])
            if len(clause_content) > MIN_CONTENT_LENGTH['clause']:
                clauses.append(f"{clause_letter}) {clause_content}")
        
        return clauses[:EXTRACTION_LIMITS['clauses']]
    
    @staticmethod
    def extract_issuing_info(text: str) -> Dict[str, str]:
        """Trích xuất thông tin cơ quan ban hành và ngày ban hành"""
        info = {}
        
        # Trích xuất cơ quan ban hành
        for pattern in COMMON_PATTERNS['agency']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['co_quan_ban_hanh'] = match.group(1).strip()
                break
        
        # Trích xuất số văn bản
        for pattern in COMMON_PATTERNS['document_number']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['so_van_ban'] = match.group(1).strip()
                break
        
        # Trích xuất ngày ban hành
        for pattern in COMMON_PATTERNS['date']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 3:
                    day, month, year = match.groups()
                    info['ngay_ban_hanh'] = f"{day.zfill(2)}/{month.zfill(2)}/{year}"
                    break
        
        return info
    
    @staticmethod
    def extract_by_keywords(text: str, keywords: List[str], max_results: int = 5) -> List[str]:
        """Trích xuất nội dung theo từ khóa"""
        results = []
        
        for keyword in keywords:
            pattern = f'{keyword}[:\\s]*([^.\\n]+)'
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                content = match.strip().rstrip('.,;')
                if len(content) > MIN_CONTENT_LENGTH['default']:
                    results.append(content)
        
        return results[:max_results]
    
    @staticmethod
    def extract_numbered_items(text: str, prefix: str = "bước", max_results: int = 6) -> List[str]:
        """Trích xuất các mục được đánh số"""
        items = []
        pattern = f'{prefix}\\s+(\\d+)[:\\s]*([^.\\n]+)'
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            item_num = match[0]
            item_content = match[1].strip()
            if len(item_content) > MIN_CONTENT_LENGTH['default']:
                items.append(f"{prefix.title()} {item_num}: {item_content}")
        
        return items[:max_results]