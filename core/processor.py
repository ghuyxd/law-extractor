"""
Class chính để xử lý văn bản pháp luật
"""
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from core.config import setup_logging, DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR, DOCUMENT_TYPE_MAPPING
from utils.file_handler import FileHandler
from utils.text_processor import TextProcessor
from utils.summary_generator import SummaryGenerator
from extractors.extractor_factory import ExtractorFactory


logger = setup_logging()

class LegalDocumentProcessor:
    """
    Lớp xử lý các file JSON chứa dữ liệu văn bản pháp luật và trích xuất thông tin theo cấu trúc pháp lý chuẩn
    """
    
    def __init__(self, input_dir: str = DEFAULT_INPUT_DIR, output_dir: str = DEFAULT_OUTPUT_DIR):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Đảm bảo thư mục output tồn tại
        FileHandler.ensure_directory(self.output_dir)
        
        self.file_handler = FileHandler()
        self.text_processor = TextProcessor()
        self.summary_generator = SummaryGenerator()
        self.extractor_factory = ExtractorFactory()
    
    def process_document(self, document: Dict[str, Any], document_type: str) -> Dict[str, Any]:
        """Xử lý một văn bản và trích xuất thông tin theo cấu trúc pháp lý"""
        # Trích xuất thông tin cơ bản
        file_info = document.get('file_info', {})
        raw_text = document.get('raw_text', '')
        
        # Thông tin metadata
        result = {
            "ThongTinVanBan": {
                "ten_file": file_info.get('filename', ''),
                "loai_van_ban": file_info.get('document_type', document_type.replace('_', ' ').title()),
                "so_trang": file_info.get('total_pages', 0),
                "so_ky_tu": file_info.get('extraction_summary', {}).get('total_chars', 0),
                "duong_dan": file_info.get('filepath', '')
            }
        }
        
        # Trích xuất thông tin cơ quan ban hành và ngày ban hành
        issuing_info = self.text_processor.extract_issuing_info(raw_text)
        result["ThongTinVanBan"].update(issuing_info)
        
        # Trích xuất cấu trúc chuyên biệt theo loại văn bản
        extractor = self.extractor_factory.get_extractor(document_type)
        if extractor:
            specific_structure = extractor.extract_structure(document)
            result.update(specific_structure)
        else:
            # Cấu trúc mặc định
            result.update({
                "VanBanCanCu": self.text_processor.extract_legal_basis(raw_text),
                "CacDieu": self.text_processor.extract_articles(raw_text),
                "NoiDungChinh": self.text_processor.extract_sections(raw_text)
            })
        
        return result
    
    def process_json_file(self, json_file: Path) -> bool:
        """Xử lý một file JSON"""
        logger.info(f"Processing file: {json_file.name}")
        
        # Load dữ liệu
        data = self.file_handler.load_json(json_file)
        if not data:
            return False
        
        # Lấy loại văn bản từ tên file
        document_type = self.file_handler.get_document_type_from_filename(json_file.name)
        
        processed_documents = []
        
        if isinstance(data, list):
            for doc in data:
                try:
                    processed_doc = self.process_document(doc, document_type)
                    processed_documents.append(processed_doc)
                except Exception as e:
                    logger.error(f"Error processing document in {json_file.name}: {e}")
                    continue
        else:
            logger.warning(f"Unexpected data format in {json_file.name}")
            return False
        
        # Tạo thư mục kết quả cho loại văn bản này
        output_subdir = self.output_dir / document_type
        FileHandler.ensure_directory(output_subdir)
        
        # Ghi kết quả
        output_file = output_subdir / f"{document_type}_structured.json"
        success = self.file_handler.save_json(processed_documents, output_file)
        
        if success:
            # Tạo file tóm tắt thống kê
            summary = self.summary_generator.create_document_summary(processed_documents, document_type)
            summary_file = output_subdir / f"{document_type}_summary.json"
            self.file_handler.save_json(summary, summary_file)
            
            logger.info(f"Processed {len(processed_documents)} documents from {json_file.name}")
            return True
        
        return False
    
    def process_all_files(self) -> None:
        """Xử lý tất cả file JSON trong thư mục input"""
        json_files = self.file_handler.get_json_files(self.input_dir)
        
        if not json_files:
            logger.warning(f"No JSON files found in {self.input_dir}")
            return
        
        logger.info(f"Found {len(json_files)} files to process")
        
        processed_count = 0
        for json_file in json_files:
            if self.process_json_file(json_file):
                processed_count += 1
        
        if processed_count > 0:
            # Tạo báo cáo tổng hợp
            self.create_overall_summary()
            logger.info(f"Processing completed! Processed {processed_count}/{len(json_files)} files. Results saved in '{self.output_dir}' directory")
        else:
            logger.error("No files were processed successfully")
    
    def create_overall_summary(self) -> None:
        """Tạo báo cáo tổng hợp cho tất cả loại văn bản"""
        summary_files = list(self.output_dir.glob("*/*_summary.json"))
        
        if not summary_files:
            logger.warning("No summary files found for overall summary")
            return
        
        summaries = []
        for summary_file in summary_files:
            summary_data = self.file_handler.load_json(summary_file)
            if summary_data:
                summaries.append(summary_data)
        
        if summaries:
            overall_summary = self.summary_generator.create_overall_summary(summaries)
            overall_file = self.output_dir / "tong_hop_ket_qua.json"
            
            if self.file_handler.save_json(overall_summary, overall_file):
                logger.info(f"Overall summary saved to {overall_file}")
            else:
                logger.error("Failed to save overall summary")