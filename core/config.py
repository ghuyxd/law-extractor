"""
Cấu hình và constants cho hệ thống xử lý văn bản pháp luật
"""
import logging
from pathlib import Path

# Cấu hình logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

# Đường dẫn mặc định
DEFAULT_INPUT_DIR = "pdf-extractor/spelling_fixed_json"
DEFAULT_OUTPUT_DIR = "result"

# Mapping loại văn bản với extractor tương ứng
DOCUMENT_TYPE_MAPPING = {
    'luật': 'law',
    'nghị_định': 'decree',
    'nghị_quyết': 'resolution',
    'quyết_định': 'decision',
    'thông_tư': 'circular',
    'chỉ_thị': 'directive',
    'kết_luận': 'conclusion',
    'hướng_dẫn': 'guidance',
    'công_văn': 'official_letter',
    'báo_cáo': 'report',
    'kế_hoạch': 'plan',
    'phương_án': 'scheme',
    'quy_định': 'regulation',
    'quy_chế': 'statute',
    'pháp_lệnh': 'ordinance',
    'thông_báo': 'notification',
    'đề_án': 'proposal',
    'văn_bản_hợp_nhất': 'consolidated',
    'quy_chuẩn_việt_nam': 'vietnam_standard',
    'thông_tư_liên_tịch': 'joint_circular',
    'công_điện': 'cable',
    'lệnh': 'order'
}

# Regex patterns dùng chung
COMMON_PATTERNS = {
    'article': r'Điều\s+(\d+)[.\s]*([^Điều]*?)(?=Điều\s+\d+|$)',
    'chapter': r'CHƯƠNG\s+([IVXLC]+|\d+)[.\s]*([^\n]*)',
    'legal_basis': r'Căn\s+cứ\s+([^;]+(?:;|\.|\n))',
    'section': r'(\d+)\.\s+([^0-9]+?)(?=\d+\.|$)',
    'clause': r'([a-z])\)\s+([^a-z\)]+?)(?=[a-z]\)|$)',
    'date': [
        r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})',
        r'(\d{1,2})/(\d{1,2})/(\d{4})',
        r'(\d{1,2})-(\d{1,2})-(\d{4})'
    ],
    'document_number': [
        r'Số[:\s]*(\d+[^,\s\n]*)',
        r'số[:\s]*(\d+[^,\s\n]*)'
    ],
    'agency': [
        r'(CHÍNH\s+PHỦ)',
        r'(QUỐC\s+HỘI)',
        r'(CHỦ\s+TỊCH\s+NƯỚC)',
        r'(THỦ\s+TƯỚNG\s+CHÍNH\s+PHỦ)',
        r'(BỘ\s+[A-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÊẾỀỂỄỆÔỐỒỔỖỘƠỚỜỞỠỢƯỨỪỬỮỰ\s]+)',
        r'(BAN\s+CHẤP\s+HÀNH\s+TRUNG\s+ƯƠNG)',
        r'(BỘ\s+CHÍNH\s+TRỊ)',
        r'(BAN\s+BÍ\s+THƯ)',
        r'(UỶ\s+BAN\s+NHÂN\s+DÂN\s+[^.\n]+)',
        r'(HỘI\s+ĐỒNG\s+NHÂN\s+DÂN\s+[^.\n]+)'
    ]
}

# Giới hạn số lượng kết quả trích xuất
EXTRACTION_LIMITS = {
    'objectives': 5,
    'tasks': 10,
    'solutions': 8,
    'implementation': 5,
    'articles': 50,
    'chapters': 20,
    'sections': 8,
    'clauses': 15,
    'legal_basis': 10
}

# Độ dài tối thiểu cho nội dung hợp lệ
MIN_CONTENT_LENGTH = {
    'default': 10,
    'objective': 15,
    'solution': 15,
    'section': 20,
    'clause': 15,
    'legal_basis': 5
}