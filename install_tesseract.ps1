# PowerShell script to download and install Tesseract OCR
# Run as Administrator

Write-Host "Downloading Tesseract OCR installer..." -ForegroundColor Cyan

$url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.5.1.exe"
$output = "$env:TEMP\tesseract-installer.exe"

# Download with progress
Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing

Write-Host "Download complete. Starting installation..." -ForegroundColor Green

# Run installer silently
Start-Process -FilePath $output -ArgumentList "/S" -Wait

Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "Tesseract installed to: C:\Program Files\Tesseract-OCR" -ForegroundColor Yellow

# Clean up
Remove-Item $output -Force

Write-Host "`nVerifying installation..." -ForegroundColor Cyan
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version

Write-Host "`nTesseract OCR is ready!" -ForegroundColor Green
