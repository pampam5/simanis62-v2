<#
.SYNOPSIS
    Build SIMANIS62 Complete Installer
    
.DESCRIPTION
    Script untuk membuat installer lengkap SIMANIS62:
    1. Build backend dengan PyInstaller
    2. Build frontend dengan .NET publish
    3. Create installer dengan Inno Setup
    
.PARAMETER SkipBackend
    Skip build backend (gunakan build yang sudah ada)
    
.PARAMETER SkipFrontend
    Skip build frontend (gunakan build yang sudah ada)
    
.PARAMETER Version
    Versi aplikasi untuk installer. Default: 2.0.0
    
.EXAMPLE
    .\build_installer.ps1
    
.EXAMPLE
    .\build_installer.ps1 -SkipBackend -Version "2.1.0"
    
.NOTES
    Author: SIMANIS62 Team
    Version: 1.0
    Date: 2026-01-12
    
    REQUIREMENTS:
    - Python 3.12 + PyInstaller
    - .NET 8 SDK
    - Inno Setup 6.x (iscc.exe in PATH or default location)
#>

param(
    [switch]$SkipBackend,
    [switch]$SkipFrontend,
    [string]$Version = "2.0.0"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=========================================="
Write-Host "SIMANIS62 Installer Build"
Write-Host "Version: $Version"
Write-Host "=========================================="

# Find Inno Setup compiler
$IsccPaths = @(
    "iscc.exe",
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
)

$IsccExe = $null
foreach ($path in $IsccPaths) {
    if (Test-Path $path -ErrorAction SilentlyContinue) {
        $IsccExe = $path
        break
    }
    if (Get-Command $path -ErrorAction SilentlyContinue) {
        $IsccExe = $path
        break
    }
}

if (-not $IsccExe) {
    Write-Host "ERROR: Inno Setup not found!" -ForegroundColor Red
    Write-Host "Please install Inno Setup 6 from https://jrsoftware.org/isdl.php"
    exit 1
}
Write-Host "Inno Setup: $IsccExe"

# Step 1: Build Backend
if (-not $SkipBackend) {
    Write-Host "`n[Step 1/3] Building Backend..."
    & "$ScriptDir\build_backend.ps1" -Clean
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Backend build failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n[Step 1/3] Skipping Backend build"
}

# Step 2: Build Frontend
if (-not $SkipFrontend) {
    Write-Host "`n[Step 2/3] Building Frontend..."
    & "$ScriptDir\build_frontend.ps1" -Clean
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Frontend build failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "`n[Step 2/3] Skipping Frontend build"
}

# Verify build outputs exist
$BackendDist = Join-Path $ProjectRoot "dist\Simanis62.API"
$FrontendDist = Join-Path $ProjectRoot "dist\Simanis62.WPF"

if (-not (Test-Path $BackendDist)) {
    Write-Host "ERROR: Backend build not found at $BackendDist" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $FrontendDist)) {
    Write-Host "ERROR: Frontend build not found at $FrontendDist" -ForegroundColor Red
    exit 1
}

# Step 3: Run Inno Setup
Write-Host "`n[Step 3/3] Creating Installer..."

$IssFile = Join-Path $ProjectRoot "installer\simanis62.iss"
if (-not (Test-Path $IssFile)) {
    Write-Host "ERROR: Inno Setup script not found: $IssFile" -ForegroundColor Red
    exit 1
}

# Run Inno Setup with version parameter
& $IsccExe "/DAppVersion=$Version" $IssFile

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Installer creation failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n=========================================="
Write-Host "Installer build completed!" -ForegroundColor Green
Write-Host "=========================================="

# Show output
$OutputDir = Join-Path $ProjectRoot "installer\Output"
if (Test-Path $OutputDir) {
    Write-Host "`nInstaller files:"
    Get-ChildItem $OutputDir -Filter "*.exe" | ForEach-Object {
        $SizeMB = [math]::Round($_.Length / 1MB, 2)
        Write-Host "  $($_.Name) - $SizeMB MB"
    }
}