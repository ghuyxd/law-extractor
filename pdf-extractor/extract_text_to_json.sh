#!/bin/bash

SRC_DIR="pdf_files"
DEST_DIR="raw_json_output"

mkdir -p "$DEST_DIR"

find "$SRC_DIR" -type f -name '*.pdf' | while read -r filepath; do
    relpath="${filepath#$SRC_DIR/}"
    jsonname="$(basename "$relpath" .pdf).json"
    jsondir="$DEST_DIR/$(dirname "$relpath")"
    jsonpath="$jsondir/$jsonname"

    mkdir -p "$jsondir"
    echo "📄 OCR to JSON: $filepath"

    tmp_image=$(mktemp --suffix=.png)
    pdftoppm -png -singlefile "$filepath" "${tmp_image%.png}"

    text=$(tesseract "$tmp_image" stdout -l vie+eng 2>/dev/null)
    echo "{\"filename\": \"$(basename "$filepath")\", \"text\": $(jq -Rs <<<"$text")}" > "$jsonpath"

    rm "$tmp_image"
done

echo "✅ Trích xuất xong: raw_json_output/"
