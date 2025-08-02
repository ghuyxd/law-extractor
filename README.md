# Dự án xử lý văn bản pháp luật

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
venv\Scripts\activate
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
