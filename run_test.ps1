# PDF Toolbox comprehensive test script
# Usage: powershell -ExecutionPolicy Bypass -File run_test.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$OutDir = "test_out"
$Pass = 0
$Fail = 0
$FailList = @()

New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

function log   { Write-Host "[$(Get-Date -Format HH:mm:ss)] $args" }
function pass  { Write-Host "  PASS: $args" -ForegroundColor Green; $script:Pass++ }
function fail  { Write-Host "  FAIL: $args" -ForegroundColor Red; $script:Fail++; $script:FailList += "$args" }

# Pre-check
$InputPdf = "04.pdf"
if (-not (Test-Path $InputPdf)) { Write-Error "$InputPdf not found"; exit 1 }

log "=== PDF Toolbox Comprehensive Test ==="
""

# -- 1. rotate --
log "1. rotate"
python pdf_toolbox.py rotate -i $InputPdf -r 90 -o "$OutDir/test_rotate.pdf" 2>&1 | Out-File "$OutDir/rotate.log"
if (Test-Path "$OutDir/test_rotate.pdf") { pass "rotate" } else { fail "rotate" }

# -- 2. split --
log "2. split"
python pdf_toolbox.py split -i $InputPdf -o "$OutDir/test_split" -g 2 2>&1 | Out-File "$OutDir/split.log"
if (Test-Path "$OutDir/test_split/04_part01_1_2.pdf") { pass "split" } else { fail "split" }

# -- 3. merge --
log "3. merge"
python pdf_toolbox.py merge -i "$OutDir/test_rotate.pdf" "$OutDir/test_rotate.pdf" -o "$OutDir/test_merge.pdf" 2>&1 | Out-File "$OutDir/merge.log"
if (Test-Path "$OutDir/test_merge.pdf") { pass "merge" } else { fail "merge" }

# -- 4. cut --
log "4. cut"
python pdf_toolbox.py cut -i $InputPdf -o "$OutDir/test_cut.pdf" 2>&1 | Out-File "$OutDir/cut.log"
if (Test-Path "$OutDir/test_cut.pdf") { pass "cut" } else { fail "cut" }

# -- 5. png --
log "5. png"
python pdf_toolbox.py png -i $InputPdf -o "$OutDir/test_png" -z 0.3 2>&1 | Out-File "$OutDir/png.log"
if ((Test-Path "$OutDir/test_png") -and (Get-ChildItem "$OutDir/test_png" | Select-Object -First 1)) { pass "png" } else { fail "png" }

# -- 6. txt --
log "6. txt"
python pdf_toolbox.py txt -i $InputPdf -o "$OutDir/test_txt.txt" 2>&1 | Out-File "$OutDir/txt.log"
if (Test-Path "$OutDir/test_txt.txt") { pass "txt" } else { fail "txt" }

# -- 7. img2pdf --
log "7. img2pdf"
python -c "from PIL import Image; Image.new('RGB',(100,100),'red').save('$OutDir/t1.png'); Image.new('RGB',(100,100),'blue').save('$OutDir/t2.png')"
python pdf_toolbox.py img2pdf -i "$OutDir/t1.png" "$OutDir/t2.png" -o "$OutDir/test_img2pdf.pdf" 2>&1 | Out-File "$OutDir/img2pdf.log"
if (Test-Path "$OutDir/test_img2pdf.pdf") { pass "img2pdf" } else { fail "img2pdf" }

# -- 8. capture --
log "8. capture"
python pdf_toolbox.py capture -i $InputPdf -o "$OutDir/test_capture.pdf" 2>&1 | Out-File "$OutDir/capture.log"
if (Test-Path "$OutDir/test_capture.pdf") { pass "capture" } else { fail "capture" }

# -- 9. receipt --
log "9. receipt"
# Use wildcard to avoid Chinese char encoding issues in .ps1 file
$ReceiptPdf = Resolve-Path "D:\01_personal\08_ZXF\00_*\20230410\042002200411_82842056.pdf"
if ($ReceiptPdf) {
    python pdf_toolbox.py receipt -f "$ReceiptPdf" -o "$OutDir/test_receipt.txt" 2>&1 | Out-File "$OutDir/receipt.log"
    $receiptOk = Select-String -Path "$OutDir/receipt.log" -Pattern "Total: 246.0" -Quiet
    if ($receiptOk) { pass "receipt" } else { fail "receipt" }
} else {
    Write-Host "  SKIP: receipt PDF not found"
}

""
log "=== Results ==="
Write-Host "  PASS: $Pass" -ForegroundColor Green
Write-Host "  FAIL: $Fail" -ForegroundColor Red
if ($Fail -gt 0) { Write-Host "  Failed: $($FailList -join ', ')" -ForegroundColor Red }

""
if ($Fail -gt 0) {
    log "Test artifacts left in $OutDir for inspection"
    log "Remove: Remove-Item -Path '$OutDir' -Recurse -Force"
} else {
    log "Cleaning up..."
    Remove-Item -Path $OutDir -Recurse -Force -ErrorAction SilentlyContinue
}

exit $Fail
