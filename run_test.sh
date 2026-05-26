#!/bin/bash
# PDF Toolbox comprehensive test script
# Usage: bash run_test.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

OUT_DIR="test_out"
SUMMARY="$OUT_DIR/summary.log"
PASS=0
FAIL=0
FAIL_LIST=()

mkdir -p "$OUT_DIR"

log()   { echo "[$(date +%H:%M:%S)] $*"; }
pass()  { echo "  PASS: $1"; ((PASS++)); }
fail()  { echo "  FAIL: $1"; ((FAIL++)); FAIL_LIST+=("$1"); }

# Pre-check: test input PDF
INPUT_PDF="04.pdf"
if [ ! -f "$INPUT_PDF" ]; then
    echo "ERROR: $INPUT_PDF not found"; exit 1
fi

log "=== PDF Toolbox Comprehensive Test ==="
echo ""

# ── 1. rotate ──
log "1. rotate"
python pdf_toolbox.py rotate -i "$INPUT_PDF" -r 90 -o "$OUT_DIR/test_rotate.pdf" > "$OUT_DIR/rotate.log" 2>&1
if [ -f "$OUT_DIR/test_rotate.pdf" ]; then pass "rotate"; else fail "rotate"; fi

# ── 2. split ──
log "2. split"
python pdf_toolbox.py split -i "$INPUT_PDF" -o "$OUT_DIR/test_split" -g 2 > "$OUT_DIR/split.log" 2>&1
if [ -f "$OUT_DIR/test_split/04_part01_1_2.pdf" ]; then pass "split"; else fail "split"; fi

# ── 3. merge ──
log "3. merge"
python pdf_toolbox.py merge \
    -i "$OUT_DIR/test_rotate.pdf" "$OUT_DIR/test_rotate.pdf" \
    -o "$OUT_DIR/test_merge.pdf" > "$OUT_DIR/merge.log" 2>&1
if [ -f "$OUT_DIR/test_merge.pdf" ]; then pass "merge"; else fail "merge"; fi

# ── 4. cut ──
log "4. cut"
python pdf_toolbox.py cut -i "$INPUT_PDF" -o "$OUT_DIR/test_cut.pdf" > "$OUT_DIR/cut.log" 2>&1
if [ -f "$OUT_DIR/test_cut.pdf" ]; then pass "cut"; else fail "cut"; fi

# ── 5. png ──
log "5. png"
python pdf_toolbox.py png -i "$INPUT_PDF" -o "$OUT_DIR/test_png" -z 0.3 > "$OUT_DIR/png.log" 2>&1
if [ -d "$OUT_DIR/test_png" ] && [ "$(ls -A "$OUT_DIR/test_png")" ]; then pass "png"; else fail "png"; fi

# ── 6. txt ──
log "6. txt"
python pdf_toolbox.py txt -i "$INPUT_PDF" -o "$OUT_DIR/test_txt.txt" > "$OUT_DIR/txt.log" 2>&1
if [ -f "$OUT_DIR/test_txt.txt" ]; then pass "txt"; else fail "txt"; fi

# ── 7. img2pdf ──
log "7. img2pdf"
python -c "from PIL import Image; Image.new('RGB',(100,100),'red').save('$OUT_DIR/t1.png'); Image.new('RGB',(100,100),'blue').save('$OUT_DIR/t2.png')"
python pdf_toolbox.py img2pdf -i "$OUT_DIR/t1.png" "$OUT_DIR/t2.png" -o "$OUT_DIR/test_img2pdf.pdf" > "$OUT_DIR/img2pdf.log" 2>&1
if [ -f "$OUT_DIR/test_img2pdf.pdf" ]; then pass "img2pdf"; else fail "img2pdf"; fi

# ── 8. capture ──
log "8. capture"
python pdf_toolbox.py capture -i "$INPUT_PDF" -o "$OUT_DIR/test_capture.pdf" > "$OUT_DIR/capture.log" 2>&1
if [ -f "$OUT_DIR/test_capture.pdf" ]; then pass "capture"; else fail "capture"; fi

# ── 9. receipt ──
RECEIPT_PDF="D:/01_personal/08_ZXF/00_发票/20230410/042002200411_82842056.pdf"
log "9. receipt"
if [ -f "$RECEIPT_PDF" ]; then
    python pdf_toolbox.py receipt -f "$RECEIPT_PDF" -o "$OUT_DIR/test_receipt.txt" > "$OUT_DIR/receipt.log" 2>&1
    if grep -q "Total: 246.0" "$OUT_DIR/receipt.log" 2>/dev/null; then
        pass "receipt"
    else
        fail "receipt"
    fi
else
    echo "  SKIP: receipt PDF not found"
fi

echo ""
log "=== Results ==="
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
if [ "$FAIL" -gt 0 ]; then
    echo "  Failed: ${FAIL_LIST[*]}"
fi

# Cleanup
echo ""
log "Cleaning up..."
rm -rf "$OUT_DIR"

exit $FAIL
