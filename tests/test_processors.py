"""
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
