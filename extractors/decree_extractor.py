"""
Extractor cải tiến cho Nghị định - sửa lỗi trích xuất nội dung
"""
from typing import Dict, Any, List, Optional
import re
from .base_extractor import BaseExtractor

class DecreeExtractor(BaseExtractor):
    """Extractor cải tiến cho Nghị định, khắc phục lỗi trích xuất tiêu đề"""
    
    def __init__(self):
        super().__init__()
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, str]:
        """Khởi tạo các pattern regex được cải tiến"""
        return {
            'so_nghi_dinh': r'(?:NGHỊ\s+ĐỊNH|Nghị\s+định)\s*(?:số\s*)?(\d+/\d{4}/NĐ-CP|\d+/\d{4}/ND-CP)',
            'tieu_de': r'(?:v/v|về|VỀ|Quy\s+định)\s*([^\n]+?)(?=\n|Căn\s+cứ)',
            'can_cu_section': r'Căn\s+cứ(.*?)(?=Theo\s+đề\s+nghị|NGHỊ\s+ĐỊNH|Chính\s+phủ\s+ban\s+hành)',
            'can_cu_item': r'(?:Căn\s+cứ\s+)?([^;]+?)(?:;|\n(?=Căn\s+cứ)|(?=Theo\s+đề\s+nghị))',
            # Pattern cải tiến cho điều khoản
            'dieu_pattern': r'Điều\s+(\d+)\.\s*([^\n]*?)(?:\n|$)(.*?)(?=Điều\s+\d+|CHƯƠNG|PHỤ\s+LỤC|$)',
            # Pattern để tách tiêu đề và nội dung điều
            'dieu_title_content': r'Điều\s+(\d+)\.\s*([^\n]+?)(?:\n|\r\n|\r)(.*?)(?=Điều\s+\d+|CHƯƠNG|PHỤ\s+LỤC|$)'
        }
    
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất cấu trúc với xử lý text cải tiến"""
        raw_text = document.get('raw_text', '')
        
        # Chuẩn hóa văn bản với xử lý tốt hơn
        text = self._clean_text_improved(raw_text)
        
        # Cấu trúc đầu ra
        structure = {
            "TieuDe": self._extract_title(text),
            "VanBanCanCu": self._extract_legal_basis_simple(text),
            "CacDieu": self._extract_articles_improved(text)
        }
        
        return structure
    
    def _clean_text_improved(self, text: str) -> str:
        """Làm sạch văn bản với xử lý cải tiến"""
        # Chuẩn hóa line breaks
        text = re.sub(r'\r\n|\r', '\n', text)
        
        # Loại bỏ khoảng trắng thừa nhưng giữ lại cấu trúc
        text = re.sub(r'[ \t]+', ' ', text)  # Chỉ chuẩn hóa space và tab
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Chuẩn hóa line breaks
        
        # Chuẩn hóa số điều nhưng giữ nguyên tiêu đề
        text = re.sub(r'Điều\s+(\d+)\s*\.', r'Điều \1.', text)
        
        return text.strip()
    
    def _extract_title(self, text: str) -> str:
        """Trích xuất tiêu đề với xử lý cải tiến"""
        # Lấy số nghị định
        so_match = re.search(self.patterns['so_nghi_dinh'], text, re.IGNORECASE)
        so_nghi_dinh = so_match.group(1) if so_match else ""
        
        # Lấy tiêu đề với pattern cải tiến
        title_patterns = [
            r'(?:v/v|về|VỀ)\s*([^\n]+?)(?=\n|Căn\s+cứ)',
            r'Quy\s+định\s*([^\n]+?)(?=\n|Căn\s+cứ)',
            r'NGHỊ\s+ĐỊNH.*?\n([^\n]+?)(?=\n|Căn\s+cứ)'
        ]
        
        title = ""
        for pattern in title_patterns:
            title_match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                break
        
        if so_nghi_dinh and title:
            return f"Nghị định {so_nghi_dinh} {title}"
        elif so_nghi_dinh:
            return f"Nghị định {so_nghi_dinh}"
        else:
            return "Nghị định"
    
    def _extract_legal_basis_simple(self, text: str) -> List[str]:
        """Trích xuất căn cứ pháp lý với xử lý cải tiến"""
        basis_list = []
        
        # Tìm phần căn cứ với pattern cải tiến
        can_cu_pattern = r'Căn\s+cứ(.*?)(?=Theo\s+đề\s+nghị|NGHỊ\s+ĐỊNH|Chính\s+phủ\s+ban\s+hành|Điều\s+1)'
        can_cu_match = re.search(can_cu_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if can_cu_match:
            can_cu_text = can_cu_match.group(1)
            
            # Tách từng item căn cứ với pattern cải tiến
            # Tách theo dấu chấm phẩy hoặc xuống dòng có "Căn cứ"
            items = re.split(r';(?=\s*(?:Căn\s+cứ|\n))|(?=\n\s*Căn\s+cứ)', can_cu_text)
            
            for item in items:
                # Làm sạch item
                cleaned_item = re.sub(r'^\s*Căn\s+cứ\s*', '', item.strip(), flags=re.IGNORECASE)
                cleaned_item = cleaned_item.strip().strip(';').strip()
                
                # Chỉ giữ lại các item có ý nghĩa
                if (len(cleaned_item) > 15 and 
                    any(keyword in cleaned_item.lower() 
                        for keyword in ['luật', 'nghị định', 'hiến pháp', 'quyết định', 'thông tư', 'bộ luật'])):
                    basis_list.append(cleaned_item)
        
        return basis_list
    
    def _extract_articles_improved(self, text: str) -> List[Dict[str, Any]]:
        """Trích xuất các điều với xử lý cải tiến"""
        articles = []
        
        # Pattern cải tiến để tách điều khoản
        dieu_pattern = r'Điều\s+(\d+)\.\s*([^\n]*?)(?:\n|\r\n|\r)(.*?)(?=Điều\s+\d+|CHƯƠNG|PHỤ\s+LỤC|$)'
        dieu_matches = re.finditer(dieu_pattern, text, re.DOTALL | re.IGNORECASE)
        
        for match in dieu_matches:
            so_dieu = match.group(1)
            ten_dieu_raw = match.group(2).strip()
            noi_dung_raw = match.group(3).strip() if match.group(3) else ""
            
            # Xử lý tiêu đề điều
            ten_dieu = self._clean_article_title(ten_dieu_raw)
            
            # Xử lý nội dung điều
            noi_dung = self._clean_article_content_improved(noi_dung_raw)
            
            # Nếu tiêu đề trống, lấy từ nội dung
            if not ten_dieu and noi_dung:
                # Lấy câu đầu tiên làm tiêu đề
                first_sentence = noi_dung.split('.')[0].strip()
                if len(first_sentence) < 100:  # Đảm bảo không quá dài
                    ten_dieu = first_sentence
                    # Loại bỏ câu đầu khỏi nội dung
                    remaining = '.'.join(noi_dung.split('.')[1:]).strip()
                    if remaining:
                        noi_dung = remaining
            
            # Chỉ thêm nếu có nội dung hoặc tiêu đề
            if ten_dieu or noi_dung:
                articles.append({
                    f"Dieu {so_dieu}": {
                        "ten": ten_dieu if ten_dieu else f"Điều {so_dieu}",
                        "noi_dung": noi_dung
                    }
                })
        
        return articles
    
    def _clean_article_title(self, title: str) -> str:
        """Làm sạch tiêu đề điều khoản"""
        if not title:
            return ""
        
        # Loại bỏ khoảng trắng thừa
        title = re.sub(r'\s+', ' ', title.strip())
        
        # Loại bỏ các ký tự đặc biệt ở đầu và cuối
        title = re.sub(r'^[^\w\sÀ-ỹ]+|[^\w\sÀ-ỹ]+$', '', title)
        
        return title.strip()
    
    def _clean_article_content_improved(self, content: str) -> str:
        """Làm sạch nội dung điều khoản với xử lý cải tiến"""
        if not content:
            return ""
        
        # Loại bỏ khoảng trắng thừa nhưng giữ cấu trúc
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Loại bỏ các ký tự đặc biệt không cần thiết nhưng giữ dấu câu tiếng Việt
        unwanted_chars = r'[^\w\s.,;:()\/\-àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđĐ%\[\]"]'
        content = re.sub(unwanted_chars, '', content)
        
        # Chuẩn hóa dấu câu
        content = re.sub(r'\s+([.,;:])', r'\1', content)  # Loại bỏ space trước dấu câu
        content = re.sub(r'([.,;:])\s*', r'\1 ', content)  # Thêm space sau dấu câu
        
        # Chỉ giữ lại nếu đủ dài và có ý nghĩa
        if len(content) > 10:  # Giảm threshold
            return content.strip()
        
        return ""
    
    def validate_extraction(self, structure: Dict[str, Any]) -> bool:
        """Kiểm tra với tiêu chí cải tiến"""
        # Kiểm tra có tiêu đề
        if not structure.get("TieuDe") or structure["TieuDe"] == "Nghị định":
            return False
        
        # Kiểm tra có điều khoản
        if not structure.get("CacDieu") or len(structure["CacDieu"]) == 0:
            return False
        
        # Kiểm tra chất lượng điều khoản
        valid_articles = 0
        for article in structure["CacDieu"]:
            for key, value in article.items():
                if isinstance(value, dict):
                    if value.get("ten") and len(value.get("ten", "")) > 5:
                        valid_articles += 1
                    elif value.get("noi_dung") and len(value.get("noi_dung", "")) > 20:
                        valid_articles += 1
        
        return valid_articles > 0

# Class mở rộng với debugging
class DebugDecreeExtractor(DecreeExtractor):
    """Version có debug để kiểm tra quá trình trích xuất"""
    
    def extract_with_debug(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất với thông tin debug"""
        raw_text = document.get('raw_text', '')
        print(f"Raw text length: {len(raw_text)}")
        
        # Chuẩn hóa văn bản
        text = self._clean_text_improved(raw_text)
        print(f"Cleaned text length: {len(text)}")
        
        # Debug title extraction
        title = self._extract_title(text)
        print(f"Extracted title: {title}")
        
        # Debug articles extraction
        articles = self._extract_articles_improved(text)
        print(f"Number of articles extracted: {len(articles)}")
        
        for i, article in enumerate(articles[:3]):  # Show first 3
            for key, value in article.items():
                print(f"Article {i+1} - {key}:")
                print(f"  Title: {value.get('ten', 'N/A')}")
                print(f"  Content length: {len(value.get('noi_dung', ''))}")
        
        structure = {
            "TieuDe": title,
            "VanBanCanCu": self._extract_legal_basis_simple(text),
            "CacDieu": articles
        }
        
        return structure

# Function để format output như yêu cầu
def format_simple_output(structure: Dict[str, Any]) -> Dict[str, Any]:
    """Format đầu ra đơn giản và rõ ràng"""
    output = {
        "TieuDe": structure.get("TieuDe", ""),
        "VanBanCanCu": structure.get("VanBanCanCu", []),
        "CacDieu": []
    }
    
    # Chuyển đổi format CacDieu
    for article in structure.get("CacDieu", []):
        for key, value in article.items():
            if isinstance(value, dict):
                ten = value.get('ten', '')
                noi_dung = value.get('noi_dung', '')
                
                # Tạo entry rõ ràng
                article_entry = {
                    key: {
                        "ten": ten,
                        "noi_dung": noi_dung
                    }
                }
                output["CacDieu"].append(article_entry)
            else:
                output["CacDieu"].append({key: str(value)})
    
    return output

# Usage example
def test_extractor():
    """Test function với sample text"""
    sample_text = """
    NGHỊ ĐỊNH số 123/2024/NĐ-CP
    về Quy định về phòng không nhân dân
    
    Căn cứ Luật Tổ chức Chính phủ số 32/2001/QH10;
    Căn cứ Luật Quốc phòng số 22/2018/QH14;
    
    Điều 1. Phạm vi điều chỉnh
    Nghị định này quy định chi tiết khoản 4 Điều 15 của Luật Quốc phòng về tổ chức, hoạt động phòng không nhân dân.
    
    Điều 2. Đối tượng áp dụng  
    Nghị định này áp dụng đối với cơ quan, tổ chức, đơn vị, địa phương, doanh nghiệp và cá nhân có liên quan đến hoạt động phòng không nhân dân.
    """
    
    extractor = DecreeExtractor()
    document = {"raw_text": sample_text}
    result = extractor.extract_structure(document)
    formatted = format_simple_output(result)
    
    return formatted