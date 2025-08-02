#!/usr/bin/env python3
"""
Script để tạo cấu trúc thư mục và các file cần thiết cho dự án
"""

import os
from pathlib import Path


def create_directory_structure():
    """Tạo cấu trúc thư mục cho dự án"""
    
    # Danh sách các thư mục cần tạo
    directories = [
        "processors",
        "utils", 
        "output",
        "logs",
        "tests",
        "config",
    ]
    
    # Tạo các thư mục
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Đã tạo thư mục: {directory}")
    
    # Tạo file __init__.py cho các package
    init_files = [
        "processors/__init__.py",
        "utils/__init__.py",
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"Đã tạo file: {init_file}")


def create_processor_templates():
    """Tạo template cho các processor còn lại"""
    
    processor_types = [
        "luat_processor",
        "nghi_dinh_processor", 
        "nghi_quyet_processor",
        "quyet_dinh_processor",
        "thong_tu_processor",
        "chi_thi_processor",
        "cong_van_processor",
        "cong_dien_processor",
        "ket_luan_processor",
        "phap_lenh_processor",
        "thong_bao_processor",
        "huong_dan_processor",
        "ke_hoach_processor",
        "quy_dinh_processor",
        "quy_che_processor",
        "phuong_an_processor",
        "de_an_processor",
        "thong_tu_lien_tich_processor",
        "van_ban_hop_nhat_processor",
        "quy_chuan_viet_nam_processor",
    ]
    
    template = '''"""
Processor cho văn bản loại "{doc_type}"
"""

import re
from typing import Dict, Any, Optional
from .base_processor import BaseProcessor


class {class_name}(BaseProcessor):
    """Processor chuyên xử lý văn bản {doc_type}"""
    
    def __init__(self):
        super().__init__()
        # Thêm các pattern đặc biệt cho loại văn bản này
        self.patterns.update({{
            # TODO: Thêm các pattern regex chuyên biệt
        }})
    
    def process(self, text: str, filename: str = "") -> Dict[str, Any]:
        """Xử lý văn bản {doc_type}"""
        
        result = {{
            "ten_van_ban": "{doc_type}",
            "so_hieu": self.extract_so_hieu(text),
            "ngay_ban_hanh": self.extract_ngay_ban_hanh(text),
            "co_quan_ban_hanh": self.extract_co_quan_ban_hanh(text),
            "nguoi_ky": self.extract_nguoi_ky(text),
            "trich_yeu": self.extract_trich_yeu(text),
            "can_cu_phap_ly": self.extract_can_cu_phap_ly(text),
            "van_ban_duoc_cong_bo": self.extract_van_ban_duoc_cong_bo(text),
            "thong_tin_cong_bao": self.extract_thong_tin_cong_bao(text),
            "thong_tin_ky_so": self.extract_thong_tin_ky_so(text)
        }}
        
        return result
    
    def extract_co_quan_ban_hanh(self, text: str) -> Optional[str]:
        """Trích xuất cơ quan ban hành cho {doc_type}"""
        # TODO: Implement logic đặc biệt cho {doc_type}
        return super().extract_co_quan_ban_hanh(text)
    
    def extract_trich_yeu(self, text: str) -> Optional[str]:
        """Trích xuất trích yếu cho {doc_type}"""
        # TODO: Implement logic đặc biệt cho {doc_type}
        return super().extract_trich_yeu(text)
    
    def extract_van_ban_duoc_cong_bo(self, text: str) -> Dict[str, Any]:
        """Trích xuất thông tin văn bản được công bố trong {doc_type}"""
        # TODO: Implement logic đặc biệt cho {doc_type}
        return super().extract_van_ban_duoc_cong_bo(text)
'''
    
    # Mapping từ file name sang class name và doc type
    name_mapping = {
        "luat_processor": ("LuatProcessor", "Luật"),
        "nghi_dinh_processor": ("NghiDinhProcessor", "Nghị định"),
        "nghi_quyet_processor": ("NghiQuyetProcessor", "Nghị quyết"),
        "quyet_dinh_processor": ("QuyetDinhProcessor", "Quyết định"),
        "thong_tu_processor": ("ThongTuProcessor", "Thông tư"),
        "chi_thi_processor": ("ChiThiProcessor", "Chỉ thị"),
        "cong_van_processor": ("CongVanProcessor", "Công văn"),
        "cong_dien_processor": ("CongDienProcessor", "Công điện"),
        "ket_luan_processor": ("KetLuanProcessor", "Kết luận"),
        "phap_lenh_processor": ("PhapLenhProcessor", "Pháp lệnh"),
        "thong_bao_processor": ("ThongBaoProcessor", "Thông báo"),
        "huong_dan_processor": ("HuongDanProcessor", "Hướng dẫn"),
        "ke_hoach_processor": ("KeHoachProcessor", "Kế hoạch"),
        "quy_dinh_processor": ("QuyDinhProcessor", "Quy định"),
        "quy_che_processor": ("QuyCheProcessor", "Quy chế"),
        "phuong_an_processor": ("PhuongAnProcessor", "Phương án"),
        "de_an_processor": ("DeAnProcessor", "Đề án"),
        "thong_tu_lien_tich_processor": ("ThongTuLienTichProcessor", "Thông tư liên tịch"),
        "van_ban_hop_nhat_processor": ("VanBanHopNhatProcessor", "Văn bản hợp nhất"),
        "quy_chuan_viet_nam_processor": ("QuyChuanVietNamProcessor", "Quy chuẩn việt nam"),
    }
    
    for processor_file in processor_types:
        file_path = Path(f"processors/{processor_file}.py")
        
        if not file_path.exists():
            class_name, doc_type = name_mapping.get(processor_file, (processor_file.title().replace("_", ""), processor_file))
            
            content = template.format(
                doc_type=doc_type,
                class_name=class_name
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Đã tạo template: {file_path}")


def create_config_files():
    """Tạo các file config"""
    
    # Config chính
    config_content = '''# Cấu hình cho dự án xử lý văn bản pháp luật

# Đường dẫn thư mục
INPUT_DIR: "pdf-ocr-extractor/spelling_fixed_json"
OUTPUT_DIR: "output"
LOG_DIR: "logs"

# Cấu hình xử lý
ENCODING: "utf-8"
INDENT: 2

# Cấu hình log
LOG_LEVEL: "INFO"
LOG_FORMAT: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Pattern regex chung
COMMON_PATTERNS:
  so_hieu: "Số:\\s*([^\\n]+)"
  ngay_ban_hanh: "ngày\\s+(\\d{1,2})\\s+tháng\\s+(\\d{1,2})\\s+năm\\s+(\\d{4})"
  nguoi_ky: "([A-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ\\s]+)$"
'''
    
    with open("config/config.yaml", 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("Đã tạo file: config/config.yaml")


def create_test_files():
    """Tạo template test files"""
    
    test_content = '''"""
Test cases cho các processor
"""

import unittest
import sys
from pathlib import Path

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from processors.lenh_processor import LenhProcessor


class TestLenhProcessor(unittest.TestCase):
    """Test cases cho LenhProcessor"""
    
    def setUp(self):
        self.processor = LenhProcessor()
        
        # Sample data từ file mẫu
        self.sample_text = """
Người ký: CỔNG THÔNG TIN ĐIỆN TỬ CHÍNH PHỦ
Email: thongtinchinhphu@chinhphu.vn
Cơ quan: VĂN PHÒNG CHÍNH PHỦ
Thời gian ký: 26/06/2025 15:19:01 +07:00

CÔNG BÁO/Số: 807 + 808/Ngày 24-6-2025

VĂN BẢN QUY PHẠM PHÁP LUẬT
CHỦ TỊCH NƯỚC - QUỐC HỘI
CHỦ TỊCH NƯỚC

CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Số: 07/2025/L-CTN

Hà Nội, ngày 16 tháng 6 năm 2025

LỆNH
Về việc công bố Nghị quyết sửa đổi, bổ sung một số điều
của Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam

CHỦ TỊCH
NƯỚC CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Căn cứ Điều 88 và Điều 120 của Hiến pháp nước Cộng hòa xã hội chủ nghĩa
Việt Nam;
NAY CÔNG BỐ:
Nghị quyết sửa đổi, bổ sung một số điều của Hiến pháp nước Cộng hòa xã
hội chủ nghĩa Việt Nam
Đã được Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XV, Kỳ họp
thứ 9 thông qua ngày 16 tháng 6 năm 2025.
CHỦ TỊCH
NƯỚC CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

Lương Cường
        """
    
    def test_extract_so_hieu(self):
        """Test trích xuất số hiệu"""
        result = self.processor.extract_so_hieu(self.sample_text)
        self.assertEqual(result, "07/2025/L-CTN")
    
    def test_extract_ngay_ban_hanh(self):
        """Test trích xuất ngày ban hành"""
        result = self.processor.extract_ngay_ban_hanh(self.sample_text)
        self.assertEqual(result, "16/06/2025")
    
    def test_extract_nguoi_ky(self):
        """Test trích xuất người ký"""
        result = self.processor.extract_nguoi_ky(self.sample_text)
        self.assertEqual(result, "Lương Cường")
    
    def test_process_complete(self):
        """Test xử lý toàn bộ văn bản"""
        result = self.processor.process(self.sample_text)
        
        self.assertEqual(result["ten_van_ban"], "Lệnh")
        self.assertEqual(result["so_hieu"], "07/2025/L-CTN")
        self.assertEqual(result["ngay_ban_hanh"], "16/06/2025")
        self.assertEqual(result["nguoi_ky"], "Lương Cường")


if __name__ == '__main__':
    unittest.main()
'''
    
    with open("tests/test_processors.py", 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("Đã tạo file: tests/test_processors.py")


def create_readme():
    """Tạo file README"""
    
    readme_content = '''# Dự án xử lý văn bản pháp luật

Dự án Python để trích xuất và phân tích thông tin từ các văn bản pháp luật Việt Nam.

## Cấu trúc thư mục

```
law-document-processor/
├── main.py                    # File chính để chạy chương trình
├── requirements.txt           # Các thư viện cần thiết
├── setup_project.py          # Script tạo cấu trúc thư mục
├── README.md                 # File này
├── processors/               # Các module xử lý từng loại văn bản
│   ├── __init__.py
│   ├── base_processor.py     # Lớp cơ sở
│   ├── lenh_processor.py     # Xử lý Lệnh
│   ├── luat_processor.py     # Xử lý Luật
│   └── ...                   # Các processor khác
├── utils/                    # Các utility functions
│   ├── __init__.py
│   ├── file_utils.py         # Xử lý file
│   └── text_utils.py         # Xử lý text
├── config/                   # File cấu hình
│   └── config.yaml
├── tests/                    # Test cases
│   └── test_processors.py
├── output/                   # Thư mục chứa kết quả
└── logs/                     # Thư mục log
```

## Cách sử dụng

### 1. Cài đặt môi trường

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Thiết lập cấu trúc thư mục

```bash
python setup_project.py
```

### 3. Chạy chương trình

```bash
# Xử lý tất cả văn bản
python main.py

# Xử lý chỉ một loại văn bản
python main.py --doc-type "Lệnh"

# Xử lý một file cụ thể
python main.py --single-file "path/to/file.json"

# Chỉ định thư mục input và output
python main.py --input-dir "pdf-ocr-extractor/spelling_fixed_json" --output-file "result.json"
```

### 4. Chạy tests

```bash
python -m pytest tests/
# hoặc
python tests/test_processors.py
```

## Các loại văn bản được hỗ trợ

- Lệnh
- Luật  
- Nghị định
- Nghị quyết
- Quyết định
- Thông tư
- Chỉ thị
- Công văn
- Công điện
- Kết luận
- Pháp lệnh
- Thông báo
- Hướng dẫn
- Kế hoạch
- Quy định
- Quy chế
- Phương án
- Đề án
- Thông tư liên tịch
- Văn bản hợp nhất
- Quy chuẩn Việt Nam

## Format đầu ra

Mỗi văn bản được phân tích sẽ có cấu trúc JSON như sau:

```json
{
  "ten_van_ban": "Lệnh",
  "so_hieu": "07/2025/L-CTN",
  "ngay_ban_hanh": "16/06/2025",
  "co_quan_ban_hanh": "Chủ tịch nước Cộng hòa xã hội chủ nghĩa Việt Nam",
  "nguoi_ky": "Lương Cường",
  "trich_yeu": "Về việc công bố Nghị quyết sửa đổi, bổ sung một số điều của Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam",
  "can_cu_phap_ly": [
    "Điều 88 và Điều 120 của Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam"
  ],
  "van_ban_duoc_cong_bo": {
    "ten": "Nghị quyết sửa đổi, bổ sung một số điều của Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam",
    "co_quan_thong_qua": "Quốc hội khóa XV",
    "ky_hop": "Kỳ họp thứ 9",
    "ngay_thong_qua": "16/06/2025"
  },
  "thong_tin_cong_bao": {
    "so": "807 + 808",
    "ngay": "24-06-2025"
  },
  "thong_tin_ky_so": {
    "nguoi_ky": "CỔNG THÔNG TIN ĐIỆN TỬ CHÍNH PHỦ",
    "co_quan": "VĂN PHÒNG CHÍNH PHỦ",
    "thoi_gian_ky": "26/06/2025 15:19:01 +07:00"
  }
}
```

## Mở rộng

Để thêm xử lý cho loại văn bản mới:

1. Tạo processor mới trong thư mục `processors/`
2. Kế thừa từ `BaseProcessor`
3. Override các method cần thiết
4. Thêm vào dictionary `processors` trong `main.py`

## Ghi chú

- Dự án sử dụng regex để trích xuất thông tin từ văn bản
- Các pattern có thể cần điều chỉnh tùy theo format cụ thể của từng văn bản
- Kết quả có thể cần review và tinh chỉnh thủ công cho một số trường hợp đặc biệt
'''
    
    with open("README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("Đã tạo file: README.md")


def main():
    """Hàm main để chạy setup"""
    print("Đang thiết lập cấu trúc dự án...")
    
    create_directory_structure()
    create_processor_templates()
    create_config_files()
    create_test_files()
    create_readme()
    
    print("\n✅ Hoàn thành thiết lập dự án!")
    print("\nCác bước tiếp theo:")
    print("1. Chạy: pip install -r requirements.txt")
    print("2. Điều chỉnh các processor trong thư mục processors/")
    print("3. Chạy: python main.py để test")
    print("4. Chạy: python tests/test_processors.py để test")


if __name__ == "__main__":
    main()