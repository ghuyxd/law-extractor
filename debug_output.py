#!/usr/bin/env python3
"""
Script debug để kiểm tra và sửa lỗi output
"""

import os
import json
from pathlib import Path
from main import LawDocumentProcessor


def debug_output():
    """Debug và kiểm tra vấn đề output"""
    
    print("🔍 Debug quá trình output...")
    
    # Kiểm tra thư mục hiện tại
    current_dir = os.getcwd()
    print(f"Thư mục hiện tại: {current_dir}")
    
    # Kiểm tra quyền ghi
    try:
        test_file = "test_write.json"
        with open(test_file, 'w') as f:
            json.dump({"test": "data"}, f)
        os.remove(test_file)
        print("✅ Có quyền ghi file trong thư mục hiện tại")
    except Exception as e:
        print(f"❌ Không có quyền ghi: {e}")
        return
    
    # Chạy processor với output file cụ thể
    processor = LawDocumentProcessor()
    
    print("\n📁 Kiểm tra thư mục input...")
    input_dir = Path("pdf-ocr-extractor/spelling_fixed_json")
    if not input_dir.exists():
        print(f"❌ Thư mục input không tồn tại: {input_dir}")
        return
    else:
        print(f"✅ Thư mục input tồn tại: {input_dir}")
    
    # Xử lý một vài file để test
    print("\n🔄 Xử lý một số file để test...")
    try:
        # Chỉ xử lý Lệnh để test nhanh
        results = processor.process_directory("Lệnh")
        
        if results:
            print(f"✅ Xử lý thành công {len(results)} văn bản")
            
            # Thử ghi file output
            output_file = "test_output.json"
            print(f"\n💾 Thử ghi file: {output_file}")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Ghi file thành công: {output_file}")
            
            # In một ví dụ kết quả
            print(f"\n📄 Ví dụ kết quả đầu tiên:")
            print(json.dumps(results[0], ensure_ascii=False, indent=2))
            
            return results
        else:
            print("❌ Không có kết quả nào được tạo")
            
    except Exception as e:
        print(f"❌ Lỗi khi xử lý: {e}")
        import traceback
        traceback.print_exc()


def run_full_process():
    """Chạy toàn bộ quá trình với output file cụ thể"""
    
    print("\n🚀 Chạy toàn bộ quá trình...")
    
    processor = LawDocumentProcessor()
    
    try:
        # Xử lý tất cả văn bản
        results = processor.process_directory()
        
        # Tạo file output với timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"processed_documents_{timestamp}.json"
        
        print(f"💾 Lưu kết quả vào: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Hoàn thành! Đã xử lý {len(results)} văn bản.")
        print(f"📁 File kết quả: {output_file}")
        
        # Thống kê
        doc_types = {}
        for doc in results:
            doc_type = doc.get('ten_van_ban', 'Không xác định')
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        print("\n📊 Thống kê theo loại văn bản:")
        for doc_type, count in sorted(doc_types.items()):
            print(f"  {doc_type}: {count} văn bản")
            
        return output_file
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("=== DEBUG OUTPUT SCRIPT ===")
    
    # Debug cơ bản
    debug_output()
    
    # Chạy toàn bộ quá trình
    output_file = run_full_process()
    
    if output_file:
        print(f"\n🎉 Thành công! Kiểm tra file: {output_file}")
    else:
        print(f"\n❌ Có lỗi xảy ra!")