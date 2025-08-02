"""
Utilities cho xử lý file I/O
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class FileHandler:
    """Class xử lý các thao tác với file"""
    
    @staticmethod
    def load_json(file_path: Path) -> Optional[Dict[str, Any]]:
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {e}")
            return None
    
    @staticmethod
    def save_json(data: Any, file_path: Path) -> bool:
        """Save data to JSON file"""
        try:
            # Tạo thư mục nếu chưa tồn tại
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving JSON file {file_path}: {e}")
            return False
    
    @staticmethod
    def get_json_files(directory: Path, pattern: str = "*_results.json") -> List[Path]:
        """Lấy danh sách file JSON theo pattern"""
        try:
            return list(directory.glob(pattern))
        except Exception as e:
            logger.error(f"Error getting JSON files from {directory}: {e}")
            return []
    
    @staticmethod
    def ensure_directory(directory: Path) -> bool:
        """Đảm bảo thư mục tồn tại"""
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
            return False
    
    @staticmethod
    def get_document_type_from_filename(filename: str) -> str:
        """Lấy loại văn bản từ tên file"""
        # Loại bỏ phần "_results.json"
        return filename.replace('_results.json', '').replace('.json', '')