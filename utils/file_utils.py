"""
Utilities cho xử lý file JSON
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


def read_json_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Đọc nội dung file JSON
    
    Args:
        file_path: Đường dẫn đến file JSON
        
    Returns:
        Dictionary chứa nội dung file hoặc None nếu có lỗi
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Lỗi đọc file {file_path}: {str(e)}")
        return None


def write_json_file(data: Any, file_path: str, indent: int = 2) -> bool:
    """
    Ghi dữ liệu ra file JSON
    
    Args:
        data: Dữ liệu cần ghi
        file_path: Đường dẫn file đầu ra
        indent: Số space để indent JSON
        
    Returns:
        True nếu thành công, False nếu có lỗi
    """
    try:
        # Tạo thư mục nếu chưa tồn tại
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception as e:
        print(f"Lỗi ghi file {file_path}: {str(e)}")
        return False


def get_all_json_files(directory: Path) -> List[Path]:
    """
    Lấy tất cả file JSON trong thư mục
    
    Args:
        directory: Thư mục cần quét
        
    Returns:
        Danh sách đường dẫn các file JSON
    """
    json_files = []
    
    if not directory.exists() or not directory.is_dir():
        return json_files
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.json':
            json_files.append(file_path)
    
    return sorted(json_files)


def create_output_directory(base_dir: str, sub_dir: str = "") -> Path:
    """
    Tạo thư mục đầu ra
    
    Args:
        base_dir: Thư mục gốc
        sub_dir: Thư mục con (tùy chọn)
        
    Returns:
        Path của thư mục đã tạo
    """
    if sub_dir:
        output_dir = Path(base_dir) / sub_dir
    else:
        output_dir = Path(base_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def backup_file(file_path: str, backup_suffix: str = ".bak") -> bool:
    """
    Tạo backup của file
    
    Args:
        file_path: Đường dẫn file gốc
        backup_suffix: Hậu tố cho file backup
        
    Returns:
        True nếu backup thành công
    """
    try:
        original_path = Path(file_path)
        if original_path.exists():
            backup_path = original_path.with_suffix(original_path.suffix + backup_suffix)
            original_path.rename(backup_path)
            return True
    except Exception as e:
        print(f"Lỗi backup file {file_path}: {str(e)}")
    
    return False