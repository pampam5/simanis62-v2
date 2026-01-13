<#
.SYNOPSIS
    Build SIMANIS62 Frontend (WPF .NET 8)
    
.DESCRIPTION
    Script untuk mengompilasi frontend WPF menjadi single-file executable.
    Menggunakan self-contained deployment untuk portabilitas.
    
.PARAMETER Configuration
    Build configuration: Debug atau Release. Default: Release
    
.PARAMETER Runtime
    Target runtime identifier. Default: win-x64
    
.PARAMETER OutputDir
    Direktori output untuk build. Default: dist
    
.PARAMETER Clean
    Bersihkan build sebelumnya
    
.EXAMPLE
    .\build_frontend.ps1
    
.EXAMPLE
    .\build_frontend.ps1 -Configuration Debug -Clean
    
.NOTES
    Author: SIMANIS62 Team
    Version: 1.0
    Date: 2026-01-12
    
    REQUIREMENTS:
    - .NET 8 SDK
#>

param(
    [ValidateSet("Debug", "Release")]
    [string]$Configuration = "Release",
    
    [string]$Runtime = "win-x64",
    
    [string]$OutputDir = "dist",
    
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$FrontendDir = Join-Path $ProjectRoot "frontend\Simanis62.WPF"
$ProjectFile = Join-Path $FrontendDir "Frontend.csproj"
$DistDir = Join-Path $ProjectRoot $OutputDir

Write-Host "=========================================="
Write-Host "SIMANIS62 Frontend Build"
Write-Host "=========================================="
Write-Host "Project Root: $ProjectRoot"
Write-Host "Frontend Dir: $FrontendDir"
Write-Host "Configuration: $Configuration"
Write-Host "Runtime: $Runtime"
Write-Host "Output Dir: $DistDir"

# Check .NET SDK
Write-Host "`nChecking .NET SDK..."
$DotnetVersion = dotnet --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: .NET SDK not installed!" -ForegroundColor Red
    Write-Host "Please install .NET 8 SDK from https://dotnet.microsoft.com/download"
    exit 1
}
Write-Host ".NET SDK version: $DotnetVersion"

# Validate project file
if (-not (Test-Path $ProjectFile)) {
    Write-Host "ERROR: Project file not found: $ProjectFile" -ForegroundColor Red
    exit 1
}

# Clean if requested
if ($Clean) {
    Write-Host "`nCleaning previous build..."
    
    $BinDir = Join-Path $FrontendDir "bin"
    $ObjDir = Join-Path $FrontendDir "obj"
    
    if (Test-Path $BinDir) { Remove-Item $BinDir -Recurse -Force }
    if (Test-Path $ObjDir) { Remove-Item $ObjDir -Recurse -Force }
    
    Write-Host "Clean completed"
}

# Restore packages
Write-Host "`nRestoring NuGet packages..."
dotnet restore $ProjectFile
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Package restore failed!" -ForegroundColor Red
    exit 1
}

# Build and publish
Write-Host "`nBuilding and publishing..."
Write-Host "This may take several minutes for self-contained deployment..."

$PublishDir = Join-Path $DistDir "Simanis62.WPF"

# Publish command dengan self-contained single file
# CATATAN: Tidak menggunakan trimming karena WPF tidak fully trim-compatible
$PublishArgs = @(
    "publish"
    $ProjectFile
    "-c", $Configuration
    "-r", $Runtime
    "--self-contained", "true"
    "-p:PublishSingleFile=true"
    "-p:IncludeNativeLibrariesForSelfExtract=true"
    "-p:EnableCompressionInSingleFile=true"
    "-o", $PublishDir
)

Write-Host "Running: dotnet $($PublishArgs -join ' ')"
& dotnet @PublishArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n=========================================="
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "=========================================="

# List output files
Write-Host "`nOutput files:"
$OutputFiles = Get-ChildItem $PublishDir -File
foreach ($file in $OutputFiles) {
    $SizeMB = [math]::Round($file.Length / 1MB, 2)
    Write-Host "  $($file.Name) - $SizeMB MB"
}

$TotalSize = ($OutputFiles | Measure-Object -Property Length -Sum).Sum
Write-Host "`nTotal size: $([math]::Round($TotalSize / 1MB, 2)) MB"
Write-Host "Output directory: $PublishDir"

# Copy appsettings.json if exists
$AppSettings = Join-Path $FrontendDir "appsettings.json"
if (Test-Path $AppSettings) {
    Copy-Item $AppSettings -Destination $PublishDir -Force
    Write-Host "Copied appsettings.json to output"
}
