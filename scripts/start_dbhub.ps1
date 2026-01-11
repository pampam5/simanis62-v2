# Start DBHub for SIMANIS62 V2 Development
# Usage: .\scripts\start_dbhub.ps1 [environment] [port]

param(
    [string]$Environment = "development",
    [int]$Port = 8080
)

Write-Host "🚀 Starting DBHub for SIMANIS62 V2..." -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Port: $Port" -ForegroundColor Yellow
Write-Host ""

# Check if dbhub is installed
$dbhubInstalled = Get-Command dbhub -ErrorAction SilentlyContinue
if (-not $dbhubInstalled) {
    Write-Host "❌ DBHub not found. Installing..." -ForegroundColor Red
    npm install -g @bytebase/dbhub
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install DBHub" -ForegroundColor Red
        exit 1
    }
}

# Check if config file exists
if (-not (Test-Path "dbhub.toml")) {
    Write-Host "❌ dbhub.toml not found in current directory" -ForegroundColor Red
    Write-Host "Please run this script from project root" -ForegroundColor Yellow
    exit 1
}

# Check if development database exists
if ($Environment -eq "development") {
    if (-not (Test-Path "backend/simanis62-dev.db")) {
        Write-Host "⚠️  Development database not found. Creating..." -ForegroundColor Yellow
        python -c "import sqlite3; conn = sqlite3.connect('backend/simanis62-dev.db'); conn.execute('PRAGMA journal_mode=WAL'); conn.execute('CREATE TABLE IF NOT EXISTS _init (id INTEGER PRIMARY KEY, created_at TEXT DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close(); print('✅ Development database created')"
    }
}

Write-Host ""
Write-Host "✅ Starting DBHub..." -ForegroundColor Green
Write-Host "📊 Workbench URL: http://localhost:$Port" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Start DBHub
dbhub --config dbhub.toml --env $Environment --port $Port
