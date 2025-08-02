"""
Entry point chính cho hệ thống xử lý văn bản pháp luật
"""
import argparse
import sys
from pathlib import Path

from core.processor import LegalDocumentProcessor
from core.config import setup_logging, DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Xử lý và trích xuất thông tin từ văn bản pháp luật"
    )
    
    parser.add_argument(
        "--input-dir", "-i",
        type=str,
        default=DEFAULT_INPUT_DIR,
        help=f"Thư mục chứa file JSON đầu vào (mặc định: {DEFAULT_INPUT_DIR})"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Thư mục lưu kết quả đầu ra (mặc định: {DEFAULT_OUTPUT_DIR})"
    )
    
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Xử lý một file cụ thể thay vì toàn bộ thư mục"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Hiển thị thông tin chi tiết"
    )
    
    return parser.parse_args()

def main():
    """Hàm chính"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging()
    
    if args.verbose:
        logger.setLevel("DEBUG")
    
    try:
        # Kiểm tra thư mục đầu vào
        input_path = Path(args.input_dir)
        if not input_path.exists():
            logger.error(f"Thư mục đầu vào không tồn tại: {input_path}")
            sys.exit(1)
        
        # Tạo processor
        processor = LegalDocumentProcessor(
            input_dir=args.input_dir,
            output_dir=args.output_dir
        )
        
        # Xử lý file
        if args.file:
            # Xử lý một file cụ thể
            file_path = Path(args.file)
            if not file_path.exists():
                logger.error(f"File không tồn tại: {file_path}")
                sys.exit(1)
            
            success = processor.process_json_file(file_path)
            if success:
                logger.info("Xử lý file thành công!")
            else:
                logger.error("Xử lý file thất bại!")
                sys.exit(1)
        else:
            # Xử lý toàn bộ thư mục
            processor.process_all_files()
        
        logger.info("Hoàn thành xử lý!")
        
    except KeyboardInterrupt:
        logger.info("Dừng xử lý theo yêu cầu người dùng")
    except Exception as e:
        logger.error(f"Lỗi không mong muốn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()