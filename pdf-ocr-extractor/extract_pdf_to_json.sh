#!/bin/bash

# Tự động xác định đường dẫn script và thư mục làm việc
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/pdf_files"
DEST_DIR="$SCRIPT_DIR/raw_json_output"

# Kiểm tra xem thư mục pdf_files có tồn tại không
if [ ! -d "$SRC_DIR" ]; then
    echo "❌ Lỗi: Không tìm thấy thư mục $SRC_DIR"
    echo "📁 Script hiện tại đang ở: $SCRIPT_DIR"
    echo "🔍 Đang tìm kiếm thư mục pdf_files..."
    
    # Thử tìm thư mục pdf_files trong thư mục hiện tại và thư mục cha
    if [ -d "pdf_files" ]; then
        SRC_DIR="$(pwd)/pdf_files"
        DEST_DIR="$(pwd)/raw_json_output"
        echo "✓ Tìm thấy pdf_files tại: $SRC_DIR"
    elif [ -d "../pdf_files" ]; then
        SRC_DIR="$(cd .. && pwd)/pdf_files"
        DEST_DIR="$(cd .. && pwd)/raw_json_output"
        echo "✓ Tìm thấy pdf_files tại: $SRC_DIR"
    else
        echo "❌ Không thể tìm thấy thư mục pdf_files"
        echo "💡 Hãy chạy script từ thư mục chứa pdf_files hoặc từ thư mục pdf-ocr-extractor"
        exit 1
    fi
fi

mkdir -p "$DEST_DIR"
echo "📂 Thư mục nguồn: $SRC_DIR"
echo "📂 Thư mục đích: $DEST_DIR"

# Hàm kiểm tra xem văn bản có đủ nhiều không (tối thiểu 50 ký tự không phải khoảng trắng)
is_text_sufficient() {
    local text="$1"
    local non_space_chars=$(echo "$text" | tr -d '[:space:]' | wc -c)
    [ "$non_space_chars" -ge 50 ]
}

# Hàm trích xuất văn bản trực tiếp từ PDF
extract_direct_text() {
    local filepath="$1"
    local page_count=$(pdfinfo "$filepath" 2>/dev/null | grep "Pages:" | awk '{print $2}')
    
    if [ -z "$page_count" ]; then
        echo ""
        return 1
    fi
    
    local full_text=""
    for ((page=1; page<=page_count; page++)); do
        local page_text=$(pdftotext -f "$page" -l "$page" "$filepath" - 2>/dev/null)
        full_text+="$page_text"$'\n\n'
    done
    
    echo "$full_text"
}

# Hàm OCR toàn bộ PDF
ocr_pdf() {
    local filepath="$1"
    echo "🔍 Sử dụng OCR cho: $filepath" >&2
    
    # Chuyển tất cả các trang thành ảnh PNG
    local tmp_dir=$(mktemp -d)
    pdftoppm -png "$filepath" "$tmp_dir/page" 2>/dev/null
    
    local full_text=""
    for img in "$tmp_dir"/page-*.png; do
        if [ -f "$img" ]; then
            local text=$(tesseract "$img" stdout -l vie+eng 2>/dev/null)
            full_text+="$text"$'\n\n'
        fi
    done
    
    # Dọn dẹp
    rm -rf "$tmp_dir"
    
    echo "$full_text"
}

find "$SRC_DIR" -type f -name '*.pdf' | while read -r filepath; do
    relpath="${filepath#$SRC_DIR/}"
    jsonname="$(basename "$relpath" .pdf).json"
    jsondir="$DEST_DIR/$(dirname "$relpath")"
    jsonpath="$jsondir/$jsonname"

    mkdir -p "$jsondir"
    echo "📄 Đang xử lý: $filepath"

    # Bước 1: Thử trích xuất văn bản trực tiếp
    echo "   → Thử trích xuất văn bản trực tiếp..."
    extracted_text=$(extract_direct_text "$filepath")
    
    # Bước 2: Kiểm tra xem văn bản có đủ không
    if is_text_sufficient "$extracted_text"; then
        echo "   ✓ Đã trích xuất văn bản trực tiếp thành công"
        final_text="$extracted_text"
    else
        echo "   ⚠ Văn bản trích xuất không đủ, chuyển sang OCR..."
        final_text=$(ocr_pdf "$filepath")
        
        if is_text_sufficient "$final_text"; then
            echo "   ✓ OCR hoàn thành"
        else
            echo "   ⚠ OCR không trích xuất được nhiều văn bản"
        fi
    fi

    # Bước 3: Ghi JSON với thông tin về phương thức trích xuất
    if is_text_sufficient "$extracted_text"; then
        method="direct_text"
    else
        method="ocr"
    fi

    # Tạo JSON với thông tin bổ sung
    json_content=$(jq -n \
        --arg filename "$(basename "$filepath")" \
        --arg method "$method" \
        --arg text "$final_text" \
        --arg processed_at "$(date -Iseconds)" \
        '{
            filename: $filename,
            extraction_method: $method,
            text: $text,
            processed_at: $processed_at,
            text_length: ($text | length)
        }')
    
    echo "$json_content" > "$jsonpath"
    
    # Hiển thị thống kê
    char_count=$(echo "$final_text" | wc -c)
    line_count=$(echo "$final_text" | wc -l)
    echo "   📊 Đã trích xuất: $char_count ký tự, $line_count dòng"
done

echo "✅ Đã trích xuất toàn bộ sang: $DEST_DIR/"