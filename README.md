# Legal Document Processor

Hệ thống xử lý và trích xuất thông tin từ văn bản pháp luật Việt Nam.

## Tính năng

- Trích xuất cấu trúc văn bản pháp luật theo từng loại (Luật, Nghị định, Nghị quyết, v.v.)
- Phân tích và tóm tắt nội dung văn bản
- Tạo báo cáo thống kê chi tiết
- Hỗ trợ 22+ loại văn bản pháp luật phổ biến
- Cấu trúc modular dễ mở rộng và bảo trì

## Sử dụng

### 1. Sử dụng command line

```bash
# Xử lý toàn bộ thư mục
python main.py --input-dir output --output-dir result

# Xử lý một file cụ thể
python main.py --file path/to/file.json

# Hiển thị thông tin chi tiết
python main.py --verbose
```

### 2. Sử dụng như library

```python
from legal_document_processor import LegalDocumentProcessor

# Tạo processor
processor = LegalDocumentProcessor(
    input_dir="output",
    output_dir="result"
)

# Xử lý tất cả file
processor.process_all_files()

# Hoặc xử lý một file cụ thể
from pathlib import Path
processor.process_json_file(Path("output/luat_results.json"))
```

## Các loại văn bản được hỗ trợ

- Luật
- Nghị định
- Nghị quyết
- Quyết định
- Thông tư
- Chỉ thị
- Kết luận
- Hướng dẫn
- Công văn
- Báo cáo
- Kế hoạch
- Phương án
- Quy định
- Quy chế
- Pháp lệnh
- Thông báo
- Đề án
- Văn bản hợp nhất
- Quy chuẩn Việt Nam
- Thông tư liên tịch
- Công điện
- Lệnh

## Kết quả đầu ra

Hệ thống tạo ra:

1. **File structured JSON** cho mỗi loại văn bản với cấu trúc đã được phân tích
2. **File summary JSON** chứa thống kê cho từng loại văn bản
3. **Báo cáo tổng hợp** (`tong_hop_ket_qua.json`) cho toàn bộ dữ liệu

### Ví dụ cấu trúc kết quả cho Luật:

```json
{
  "ThongTinVanBan": {
    "ten_file": "luat_example.pdf",
    "loai_van_ban": "Luật",
    "so_van_ban": "123/2023/QH15",
    "co_quan_ban_hanh": "QUỐC HỘI",
    "ngay_ban_hanh": "15/06/2023"
  },
  "VanBanCanCu": ["Căn cứ Hiến pháp..."],
  "CacChuong": ["CHƯƠNG I. QUY ĐỊNH CHUNG"],
  "CacDieu": ["Điều 1. Phạm vi điều chỉnh"],
  "PhamViDieuChinh": ["Luật này điều chỉnh..."],
  "DoiTuongApDung": ["Áp dụng đối với..."]
}
```

## Lợi ích của cấu trúc modular

### 1. **Dễ bảo trì**
- Mỗi module có trách nhiệm rõ ràng
- Dễ debug và fix bug
- Code dễ đọc và hiểu

### 2. **Dễ mở rộng**
- Thêm extractor mới chỉ cần tạo class kế thừa BaseExtractor
- Thêm loại văn bản mới không ảnh hưởng code cũ
- Có thể customize từng bước xử lý

### 3. **Dễ test**
- Test từng module riêng biệt
- Mock dependencies dễ dàng
- Unit test coverage cao hơn

### 4. **Tái sử dụng**
- Các utility có thể dùng chung
- ExtractorFactory giúp quản lý extractors
- TextProcessor có thể dùng cho nhiều loại văn bản

## Thêm loại văn bản mới

1. Tạo extractor mới trong `extractors/`:

```python
class NewDocumentExtractor(BaseExtractor):
    def extract_structure(self, document: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = document.get('raw_text', '')
        structure = self.extract_common_structure(raw_text)
        
        # Thêm logic đặc thù cho loại văn bản mới
        structure.update({
            "NewField": self.extract_new_field(raw_text)
        })
        
        return structure
```

2. Đăng ký trong ExtractorFactory:

```python
self._extractors['new_document_type'] = NewDocumentExtractor
```
