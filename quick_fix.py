#!/usr/bin/env python3
"""
Script sửa nhanh vấn đề và chạy lại
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, str(Path(__file__).parent))

from processors.lenh_processor import LenhProcessor
from utils.file_utils import read_json_file, get_all_json_files


def process_documents_simple():
    """Xử lý văn bản theo cách đơn giản"""
    
    print("🔧 Sửa nhanh và xử lý văn bản...")
    
    # Đường dẫn input
    input_dir = Path("pdf-ocr-extractor/spelling_fixed_json")
    
    if not input_dir.exists():
        print(f"❌ Không tìm thấy thư mục: {input_dir}")
        print("💡 Hãy đảm bảo bạn đang chạy script từ thư mục gốc của dự án")
        return
    
    # Tạo file output với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"processed_documents_{timestamp}.json"
    
    print(f"📁 Thư mục input: {input_dir}")
    print(f"📄 File output: {output_file}")
    
    results = []
    
    # Processors cho từng loại văn bản
    processors = {
        "Lệnh": LenhProcessor(),
        # Tạm thời chỉ có LenhProcessor, các processor khác sẽ dùng base logic
    }
    
    # Duyệt qua từng thư mục con
    for doc_type_dir in input_dir.iterdir():
        if not doc_type_dir.is_dir():
            continue
            
        doc_type = doc_type_dir.name
        print(f"\n📂 Xử lý loại văn bản: {doc_type}")
        
        # Lấy processor tương ứng
        if doc_type in processors:
            processor = processors[doc_type]
        else:
            # Sử dụng LenhProcessor làm base (tạm thời)
            processor = LenhProcessor()
        
        # Lấy tất cả file JSON trong thư mục
        json_files = get_all_json_files(doc_type_dir)
        
        for json_file in json_files:
            try:
                print(f"  📄 {json_file.name}")
                
                # Đọc file
                data = read_json_file(json_file)
                
                if data and 'text' in data:
                    # Xử lý văn bản
                    if doc_type == "Lệnh":
                        result = processor.process(data['text'], data.get('filename', ''))
                    else:
                        # Cho các loại khác, tạo kết quả cơ bản
                        result = {
                            "ten_van_ban": doc_type,
                            "so_hieu": processor.extract_so_hieu(data['text']),
                            "ngay_ban_hanh": processor.extract_ngay_ban_hanh(data['text']),
                            "co_quan_ban_hanh": processor.extract_co_quan_ban_hanh(data['text']),
                            "nguoi_ky": processor.extract_nguoi_ky(data['text']),
                            "trich_yeu": processor.extract_trich_yeu(data['text']),
                            "can_cu_phap_ly": processor.extract_can_cu_phap_ly(data['text']),
                            "van_ban_duoc_cong_bo": {},
                            "thong_tin_cong_bao": processor.extract_thong_tin_cong_bao(data['text']),
                            "thong_tin_ky_so": processor.extract_thong_tin_ky_so(data['text'])
                        }
                    
                    if result:
                        results.append(result)
                        
            except Exception as e:
                print(f"    ❌ Lỗi: {e}")
                continue
    
    # Lưu kết quả
    try:
        print(f"\n💾 Lưu {len(results)} kết quả vào {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Thành công!")
        
        # Thống kê
        doc_types = {}
        for doc in results:
            doc_type = doc.get('ten_van_ban', 'Không xác định') 
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        print(f"\n📊 Thống kê:")
        for doc_type, count in sorted(doc_types.items()):
            print(f"  {doc_type}: {count} văn bản")
            
        # Hiển thị một ví dụ
        if results:
            print(f"\n📄 Ví dụ kết quả đầu tiên:")
            example = results[0]
            for key, value in example.items():
                if isinstance(value, (dict, list)) and value:
                    print(f"  {key}: {json.dumps(value, ensure_ascii=False)}")
                elif value:
                    print(f"  {key}: {value}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu file: {e}")
        return None


if __name__ == "__main__":
    output_file = process_documents_simple()
    
    if output_file:
        print(f"\n🎉 Hoàn thành! Kiểm tra file: {output_file}")
        
        # Kiểm tra kích thước file
        file_size = os.path.getsize(output_file)
        print(f"📏 Kích thước file: {file_size:,} bytes")
        
        if file_size > 0:
            print("✅ File đã được tạo thành công!")
        else:
            print("⚠️ File rỗng - có thể có vấn đề!")
    else:
        print("❌ Không thể tạo file output!")