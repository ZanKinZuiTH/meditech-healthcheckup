# PowerShell Profile for MediTech Project
# ===================================

# เพิ่ม Buffer Size
$bufferSize = $Host.UI.RawUI.BufferSize
$bufferSize.Height = 3000
$bufferSize.Width = 120
$Host.UI.RawUI.BufferSize = $bufferSize

# เพิ่ม Window Size
$windowSize = $Host.UI.RawUI.WindowSize
$windowSize.Height = 30
$windowSize.Width = 120
$Host.UI.RawUI.WindowSize = $windowSize

# ตั้งค่า Encoding เป็น UTF-8
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::UTF8

# ตั้งค่า Git
$env:LANG = "en_US.UTF-8"
$env:LC_ALL = "en_US.UTF-8"

# แสดงข้อความยืนยัน
Write-Host "MediTech PowerShell Profile loaded with:"
Write-Host "- Increased buffer size (120x3000)"
Write-Host "- UTF-8 encoding support"
Write-Host "- Git configuration for UTF-8" 