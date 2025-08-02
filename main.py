#!/usr/bin/env python3
"""
Chương trình xử lý văn bản pháp luật
Đọc các file JSON từ thư mục spelling_fixed_json và phân tích nội dung
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

from processors.lenh_processor import LenhProcessor
from processors.luat_processor import LuatProcessor
from processors.nghi_dinh_processor import NghiDinhProcessor
from processors.nghi_quyet_processor import NghiQuyetProcessor
from processors.quyet_dinh_processor import QuyetDinhProcessor
from processors.thong_tu_processor import ThongTuProcessor
from processors.chi_thi_processor import ChiThiProcessor
from processors.cong_van_processor import CongVanProcessor
from processors.cong_dien_processor import CongDienProcessor
from processors.ket_luan_processor import KetLuanProcessor
from processors.phap_lenh_processor import PhapLenhProcessor
from processors.thong_bao_processor import ThongBaoProcessor
from processors.huong_dan_processor import HuongDanProcessor
from processors.ke_hoach_processor import KeHoachProcessor
from processors.quy_dinh_processor import QuyDinhProcessor
from processors.quy_che_processor import QuyCheProcessor
from processors.phuong_an_processor import PhuongAnProcessor
from processors.de_an_processor import DeAnProcessor
from processors.thong_tu_lien_tich_processor import ThongTuLienTichProcessor
from processors.van_ban_hop_nhat_processor import VanBanHopNhatProcessor
from processors.quy_chuan_viet_nam_processor import QuyChuanVietNamProcessor
from utils.file_utils import read_json_file, write_json_file, get_all_json_files
from utils.text_utils import clean_text


class LawDocumentProcessor:
    """Lớp chính để xử lý các văn bản pháp luật"""
    
    def __init__(self, input_dir: str = "pdf-ocr-extractor/spelling_fixed_json"):
        self.input_dir = Path(input_dir)
        self.processors = self._init_processors()
        
    def _init_processors(self) -> Dict[str, Any]:
        """Khởi tạo các processor cho từng loại văn bản"""
        return {
            "Lệnh": LenhProcessor(),
            "Luật": LuatProcessor(),
            "Nghị định": NghiDinhProcessor(),
            "Nghị quyết": NghiQuyetProcessor(),
            "Quyết định": QuyetDinhProcessor(),
            "Thông tư": ThongTuProcessor(),
            "Chỉ thị": ChiThiProcessor(),
            "Công văn": CongVanProcessor(),
            "Công điện": CongDienProcessor(),
            "Kết luận": KetLuanProcessor(),
            "Pháp lệnh": PhapLenhProcessor(),
            "Thông báo": ThongBaoProcessor(),
            "Hướng dẫn": HuongDanProcessor(),
            "Kế hoạch": KeHoachProcessor(),
            "Quy định": QuyDinhProcessor(),
            "Quy chế": QuyCheProcessor(),
            "Phương án": PhuongAnProcessor(),
            "Đề án": DeAnProcessor(),
            "Thông tư liên tịch": ThongTuLienTichProcessor(),
            "Văn bản hợp nhất": VanBanHopNhatProcessor(),
            "Quy chuẩn việt nam": QuyChuanVietNamProcessor(),
        }
    
    def process_directory(self, doc_type: str = None, output_dir: str = "output") -> Dict[str, List[Dict[str, Any]]]:
        """
        Xử lý tất cả file trong thư mục hoặc chỉ một loại văn bản cụ thể
        
        Args:
            doc_type: Loại văn bản cần xử lý (None để xử lý tất cả)
            output_dir: Thư mục đầu ra
            
        Returns:
            Dict với key là loại văn bản và value là list các văn bản đã được phân tích
        """
        results = {}
        
        if doc_type:
            # Xử lý chỉ một loại văn bản
            doc_dir = self.input_dir / doc_type
            if doc_dir.exists() and doc_type in self.processors:
                files = get_all_json_files(doc_dir)
                processed_docs = self._process_files(files, doc_type)
                if processed_docs:
                    results[doc_type] = processed_docs
                    self._save_by_document_type(doc_type, processed_docs, output_dir)
        else:
            # Xử lý tất cả loại văn bản
            for doc_type_dir in self.input_dir.iterdir():
                if doc_type_dir.is_dir() and doc_type_dir.name in self.processors:
                    doc_type_name = doc_type_dir.name
                    files = get_all_json_files(doc_type_dir)
                    processed_docs = self._process_files(files, doc_type_name)
                    if processed_docs:
                        results[doc_type_name] = processed_docs
                        self._save_by_document_type(doc_type_name, processed_docs, output_dir)
        
        return results
    
    def _process_files(self, files: List[Path], doc_type: str) -> List[Dict[str, Any]]:
        """Xử lý danh sách file của một loại văn bản"""
        results = []
        processor = self.processors[doc_type]
        
        for file_path in files:
            try:
                print(f"Đang xử lý: {file_path}")
                data = read_json_file(file_path)
                
                if data and 'text' in data:
                    processed_doc = processor.process(data['text'], data.get('filename', ''))
                    if processed_doc:
                        results.append(processed_doc)
                        
            except Exception as e:
                print(f"Lỗi khi xử lý file {file_path}: {str(e)}")
                continue
        
        return results
    
    def _save_by_document_type(self, doc_type: str, documents: List[Dict[str, Any]], output_dir: str):
        """Lưu các văn bản theo loại vào thư mục riêng"""
        try:
            # Tạo thư mục cho loại văn bản
            type_dir = Path(output_dir) / doc_type
            type_dir.mkdir(parents=True, exist_ok=True)
            
            # Lưu từng văn bản vào file riêng
            for doc in documents:
                filename = f"{doc.get('so_hieu', 'unknown').replace('/', '-')}.json"
                # Loại bỏ ký tự không hợp lệ trong tên file
                filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', '.')).rstrip()
                if not filename.endswith('.json'):
                    filename += '.json'
                
                file_path = type_dir / filename
                write_json_file(doc, str(file_path))
                
            print(f"✅ Đã lưu {len(documents)} văn bản {doc_type} vào: {type_dir}")
            
        except Exception as e:
            print(f"❌ Lỗi khi lưu văn bản {doc_type}: {str(e)}")
    
    def _save_summary(self, results: Dict[str, List[Dict[str, Any]]], output_dir: str):
        """Lưu file tổng hợp kết quả"""
        try:
            summary = {
                "tong_quan": {
                    "tong_so_van_ban": sum(len(docs) for docs in results.values()),
                    "so_loai_van_ban": len(results),
                    "thong_ke_theo_loai": {
                        doc_type: len(docs) for doc_type, docs in results.items()
                    }
                },
                "chi_tiet_theo_loai": {}
            }
            
            # Thêm chi tiết từng loại
            for doc_type, docs in results.items():
                summary["chi_tiet_theo_loai"][doc_type] = [
                    {
                        "so_hieu": doc.get("so_hieu"),
                        "ngay_ban_hanh": doc.get("ngay_ban_hanh"),
                        "trich_yeu": doc.get("trich_yeu"),
                        "co_quan_ban_hanh": doc.get("co_quan_ban_hanh"),
                        "nguoi_ky": doc.get("nguoi_ky")
                    }
                    for doc in docs
                ]
            
            summary_file = Path(output_dir) / "summary.json"
            write_json_file(summary, str(summary_file))
            print(f"📊 Đã tạo file tổng hợp: {summary_file}")
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo file tổng hợp: {str(e)}")

    def process_single_file(self, file_path: str, output_dir: str = "output") -> Dict[str, Any]:
        """Xử lý một file cụ thể"""
        file_path = Path(file_path)
        
        # Xác định loại văn bản từ thư mục cha
        doc_type = file_path.parent.name
        
        if doc_type not in self.processors:
            raise ValueError(f"Không hỗ trợ loại văn bản: {doc_type}")
        
        data = read_json_file(file_path)
        processor = self.processors[doc_type]
        
        result = processor.process(data['text'], data.get('filename', ''))
        
        # Lưu kết quả vào thư mục output
        if result:
            self._save_by_document_type(doc_type, [result], output_dir)
        
        return result


def main():
    """Hàm main của chương trình"""
    parser = argparse.ArgumentParser(description="Xử lý văn bản pháp luật")
    parser.add_argument("--input-dir", default="pdf-ocr-extractor/spelling_fixed_json",
                       help="Thư mục chứa file JSON đầu vào")
    parser.add_argument("--output-dir", default="output",
                       help="Thư mục đầu ra")
    parser.add_argument("--doc-type", help="Loại văn bản cần xử lý (tùy chọn)")
    parser.add_argument("--single-file", help="Xử lý một file cụ thể")
    
    args = parser.parse_args()
    
    processor = LawDocumentProcessor(args.input_dir)
    
    try:
        if args.single_file:
            # Xử lý một file
            result = processor.process_single_file(args.single_file, args.output_dir)
            if result:
                print(f"\n✅ Hoàn thành! Đã xử lý 1 văn bản.")
                print(f"📁 Kết quả được lưu trong thư mục: {args.output_dir}")
            else:
                print("❌ Không thể xử lý file.")
                return 1
        else:
            # Xử lý thư mục
            results = processor.process_directory(args.doc_type, args.output_dir)
            
            # Tạo file tổng hợp
            processor._save_summary(results, args.output_dir)
            
            total_docs = sum(len(docs) for docs in results.values())
            print(f"\n🎉 Hoàn thành! Đã xử lý {total_docs} văn bản.")
            print(f"📁 Kết quả được lưu trong thư mục: {args.output_dir}")
            
            # Hiển thị thống kê
            if results:
                print(f"\n📊 Thống kê theo loại văn bản:")
                for doc_type, docs in results.items():
                    print(f"   📄 {doc_type}: {len(docs)} văn bản")
                    
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())