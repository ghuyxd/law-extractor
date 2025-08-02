"""
Tạo báo cáo tóm tắt và thống kê
"""
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter

class SummaryGenerator:
    """Class tạo báo cáo tóm tắt"""
    
    @staticmethod
    def create_document_summary(documents: List[Dict[str, Any]], document_type: str) -> Dict[str, Any]:
        """Tạo tóm tắt cho một loại văn bản"""
        total_docs = len(documents)
        
        if total_docs == 0:
            return {
                'loai_van_ban': document_type,
                'tong_so_van_ban': 0,
                'ngay_xu_ly': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }
        
        # Thống kê cơ bản
        total_pages = sum(doc.get('ThongTinVanBan', {}).get('so_trang', 0) for doc in documents)
        total_chars = sum(doc.get('ThongTinVanBan', {}).get('so_ky_tu', 0) for doc in documents)
        
        # Thống kê cơ quan ban hành
        agencies = [
            doc.get('ThongTinVanBan', {}).get('co_quan_ban_hanh')
            for doc in documents
            if doc.get('ThongTinVanBan', {}).get('co_quan_ban_hanh')
        ]
        agency_counts = dict(Counter(agencies))
        
        # Thống kê năm ban hành
        years = []
        for doc in documents:
            date = doc.get('ThongTinVanBan', {}).get('ngay_ban_hanh')
            if date:
                try:
                    year = date.split('/')[-1]
                    years.append(year)
                except:
                    pass
        year_counts = dict(Counter(years))
        
        # Thống kê số điều
        articles_counts = [
            len(doc.get('CacDieu', []))
            for doc in documents
            if doc.get('CacDieu')
        ]
        
        summary = {
            'loai_van_ban': document_type,
            'tong_so_van_ban': total_docs,
            'tong_so_trang': total_pages,
            'tong_so_ky_tu': total_chars,
            'trung_binh_trang_moi_van_ban': round(total_pages / total_docs, 2) if total_docs > 0 else 0,
            'trung_binh_ky_tu_moi_van_ban': round(total_chars / total_docs, 2) if total_docs > 0 else 0,
            'co_quan_ban_hanh': agency_counts,
            'phan_bo_theo_nam': year_counts,
            'ngay_xu_ly': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Thống kê chuyên biệt cho văn bản có điều
        if articles_counts:
            summary.update({
                'tong_so_dieu': sum(articles_counts),
                'trung_binh_dieu_moi_van_ban': round(sum(articles_counts) / len(articles_counts), 2),
                'van_ban_nhieu_dieu_nhat': max(articles_counts),
                'van_ban_it_dieu_nhat': min(articles_counts)
            })
        
        return summary
    
    @staticmethod
    def create_overall_summary(summary_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tạo báo cáo tổng hợp cho tất cả loại văn bản"""
        overall_summary = {
            'tong_so_loai_van_ban': len(summary_files),
            'chi_tiet_theo_loai': {},
            'tong_hop_chung': {
                'tong_van_ban': 0,
                'tong_trang': 0,
                'tong_ky_tu': 0,
                'tong_dieu': 0
            },
            'thong_ke_co_quan': {},
            'thong_ke_nam': {},
            'ngay_tao_bao_cao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        all_agencies = []
        all_years = []
        
        for summary in summary_files:
            if not isinstance(summary, dict):
                continue
                
            doc_type = summary.get('loai_van_ban', 'unknown')
            overall_summary['chi_tiet_theo_loai'][doc_type] = summary
            
            # Tính tổng
            overall_summary['tong_hop_chung']['tong_van_ban'] += summary.get('tong_so_van_ban', 0)
            overall_summary['tong_hop_chung']['tong_trang'] += summary.get('tong_so_trang', 0)
            overall_summary['tong_hop_chung']['tong_ky_tu'] += summary.get('tong_so_ky_tu', 0)
            overall_summary['tong_hop_chung']['tong_dieu'] += summary.get('tong_so_dieu', 0)
            
            # Thu thập dữ liệu cho thống kê tổng hợp
            agencies = summary.get('co_quan_ban_hanh', {})
            for agency, count in agencies.items():
                all_agencies.extend([agency] * count)
            
            years = summary.get('phan_bo_theo_nam', {})
            for year, count in years.items():
                all_years.extend([year] * count)
        
        # Thống kê tổng hợp cơ quan và năm
        overall_summary['thong_ke_co_quan'] = dict(Counter(all_agencies))
        overall_summary['thong_ke_nam'] = dict(Counter(all_years))
        
        return overall_summary