"""
Utilities cho xử lý và làm sạch text
"""

import re
from typing import List, Dict, Optional


def clean_text(text: str) -> str:
    """
    Làm sạch văn bản
    
    Args:
        text: Văn bản cần làm sạch
        
    Returns:
        Văn bản đã được làm sạch
    """
    if not text:
        return ""
    
    # Loại bỏ các ký tự không cần thiết
    text = re.sub(r'\s+', ' ', text)  # Thay nhiều space thành 1
    text = re.sub(r'\n\s*\n', '\n', text)  # Loại bỏ dòng trống thừa
    text = text.strip()
    
    return text


def normalize_whitespace(text: str) -> str:
    """
    Chuẩn hóa khoảng trắng trong text
    
    Args:
        text: Văn bản đầu vào
        
    Returns:
        Văn bản với khoảng trắng đã được chuẩn hóa
    """
    if not text:
        return ""
    
    # Thay thế nhiều space liên tiếp thành 1
    text = re.sub(r' +', ' ', text)
    
    # Thay thế nhiều newline liên tiếp thành 1
    text = re.sub(r'\n+', '\n', text)
    
    # Loại bỏ space trước/sau newline
    text = re.sub(r' *\n *', '\n', text)
    
    return text.strip()


def extract_lines_containing(text: str, keywords: List[str], case_sensitive: bool = False) -> List[str]:
    """
    Trích xuất các dòng chứa từ khóa
    
    Args:
        text: Văn bản đầu vào
        keywords: Danh sách từ khóa cần tìm
        case_sensitive: Có phân biệt hoa thường không
        
    Returns:
        Danh sách các dòng chứa từ khóa
    """
    lines = text.split('\n')
    matching_lines = []
    
    flags = 0 if case_sensitive else re.IGNORECASE
    
    for line in lines:
        for keyword in keywords:
            if re.search(re.escape(keyword), line, flags):
                matching_lines.append(line.strip())
                break
    
    return matching_lines


def remove_empty_lines(text: str) -> str:
    """
    Loại bỏ các dòng trống
    
    Args:
        text: Văn bản đầu vào
        
    Returns:
        Văn bản không có dòng trống
    """
    lines = [line for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)


def extract_text_between_patterns(text: str, start_pattern: str, end_pattern: str) -> Optional[str]:
    """
    Trích xuất text giữa 2 pattern
    
    Args:
        text: Văn bản đầu vào
        start_pattern: Pattern bắt đầu
        end_pattern: Pattern kết thúc
        
    Returns:
        Text giữa 2 pattern hoặc None nếu không tìm thấy
    """
    pattern = f'{start_pattern}(.*?){end_pattern}'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    return None


def split_into_sections(text: str, section_markers: List[str]) -> Dict[str, str]:
    """
    Chia văn bản thành các phần dựa trên markers
    
    Args:
        text: Văn bản đầu vào
        section_markers: Danh sách các marker để chia phần
        
    Returns:
        Dictionary với key là marker và value là nội dung phần đó
    """
    sections = {}
    current_section = None
    current_content = []
    
    lines = text.split('\n')
    
    for line in lines:
        line_stripped = line.strip()
        
        # Kiểm tra xem có phải marker mới không
        found_marker = None
        for marker in section_markers:
            if re.search(re.escape(marker), line_stripped, re.IGNORECASE):
                found_marker = marker
                break
        
        if found_marker:
            # Lưu section trước đó
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Bắt đầu section mới
            current_section = found_marker
            current_content = []
        else:
            # Thêm vào content của section hiện tại
            if current_section:
                current_content.append(line)
    
    # Lưu section cuối cùng
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


def format_vietnamese_date(date_str: str) -> str:
    """
    Chuẩn hóa format ngày tháng tiếng Việt
    
    Args:
        date_str: Chuỗi ngày tháng
        
    Returns:
        Ngày tháng đã được chuẩn hóa
    """
    if not date_str:
        return ""
    
    # Pattern để match "ngày X tháng Y năm Z"
    pattern = r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})'
    match = re.search(pattern, date_str, re.IGNORECASE)
    
    if match:
        day, month, year = match.groups()
        return f"{day.zfill(2)}/{month.zfill(2)}/{year}"
    
    # Pattern khác cho format DD/MM/YYYY hoặc DD-MM-YYYY
    patterns = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, date_str)
        if match:
            parts = match.groups()
            if len(parts[0]) == 4:  # Year first
                year, month, day = parts
            else:  # Day first
                day, month, year = parts
            return f"{day.zfill(2)}/{month.zfill(2)}/{year}"
    
    return date_str


def extract_person_name(text: str) -> Optional[str]:
    """
    Trích xuất tên người từ văn bản
    
    Args:
        text: Văn bản chứa tên
        
    Returns:
        Tên người hoặc None nếu không tìm thấy
    """
    # Pattern cho tên người Việt Nam
    pattern = r'^([A-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+(?:\s+[A-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+)*)$'
    
    lines = text.strip().split('\n')
    
    # Tìm từ cuối lên để lấy tên người ký
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if line and re.match(pattern, line):
            return line
    
    return None