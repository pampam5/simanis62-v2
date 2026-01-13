<#
.SYNOPSIS
    SIMANIS62 Database Backup Script
    
.DESCRIPTION
    Script PowerShell untuk backup database SQLite dengan WAL mode.
    - Melakukan checkpoint WAL sebelum backup
    - Membuat backup dengan timestamp
    - Kompresi ke format ZIP
    - Retention policy: simpan 7 backup terakhir
    
.PARAMETER DatabasePath
    Path ke file database SQLite. Default: C:\ProgramData\Simanis62\simanis62.db
    
.PARAMETER BackupDir
    Direktori untuk menyimpan backup. Default: C:\ProgramData\Simanis62\backups
    
.PARAMETER RetentionCount
    Jumlah backup yang disimpan. Default: 7
    
.EXAMPLE
    .\backup_database.ps1
    
.EXAMPLE
    .\backup_database.ps1 -DatabasePath "D:\simanis62-v2\backend\simanis62-dev.db" -BackupDir "D:\backups"
    
.NOTES
    Author: SIMANIS62 Team
    Version: 1.0
    Date: 2026-01-12
#>

param(
    [string]$DatabasePath = "C:\ProgramData\Simanis62\simanis62.db",
    [string]$BackupDir = "C:\ProgramData\Simanis62\backups",
    [int]$RetentionCount = 7
)

# Konfigurasi
$ErrorActionPreference = "Stop"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupName = "simanis62_backup_$Timestamp"
$BackupDbPath = Join-Path $BackupDir "$BackupName.db"
$BackupZipPath = Join-Path $BackupDir "$BackupName.zip"

# Fungsi logging
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $LogTimestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$LogTimestamp] [$Level] $Message"
    Write-Host $LogMessage
    
    # Tulis ke log file juga
    $LogFile = Join-Path $BackupDir "backup.log"
    if (Test-Path $BackupDir) {
        Add-Content -Path $LogFile -Value $LogMessage -ErrorAction SilentlyContinue
    }
}


# Fungsi untuk menjalankan SQLite command
function Invoke-SqliteCommand {
    param(
        [string]$DbPath,
        [string]$Command
    )
    
    # Cari sqlite3.exe
    $SqlitePaths = @(
        "sqlite3.exe",
        "C:\Program Files\SQLite\sqlite3.exe",
        "C:\ProgramData\chocolatey\bin\sqlite3.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\Scripts\sqlite3.exe"
    )
    
    $SqliteExe = $null
    foreach ($path in $SqlitePaths) {
        if (Get-Command $path -ErrorAction SilentlyContinue) {
            $SqliteExe = $path
            break
        }
    }
    
    if (-not $SqliteExe) {
        # Fallback: gunakan Python untuk menjalankan SQLite command
        Write-Log "sqlite3.exe tidak ditemukan, menggunakan Python fallback" "WARN"
        $PythonScript = @"
import sqlite3
conn = sqlite3.connect('$($DbPath -replace '\\', '/')')
conn.execute('$Command')
conn.close()
print('OK')
"@
        $Result = python -c $PythonScript 2>&1
        return $Result
    }
    
    $Result = & $SqliteExe $DbPath $Command 2>&1
    return $Result
}

# Fungsi untuk checkpoint WAL
function Invoke-WalCheckpoint {
    param([string]$DbPath)
    
    Write-Log "Menjalankan WAL checkpoint pada database..."
    
    try {
        # Gunakan Python untuk checkpoint (lebih reliable)
        $PythonScript = @"
import sqlite3
import sys

try:
    conn = sqlite3.connect(r'$DbPath')
    cursor = conn.cursor()
    
    # Check journal mode
    cursor.execute('PRAGMA journal_mode;')
    mode = cursor.fetchone()[0]
    print(f'Journal mode: {mode}')
    
    if mode.lower() == 'wal':
        # Run checkpoint
        cursor.execute('PRAGMA wal_checkpoint(TRUNCATE);')
        result = cursor.fetchone()
        print(f'Checkpoint result: blocked={result[0]}, log={result[1]}, checkpointed={result[2]}')
    
    conn.close()
    print('Checkpoint completed successfully')
    sys.exit(0)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"@
        
        $Result = python -c $PythonScript 2>&1
        Write-Log "Checkpoint result: $Result"
        
        if ($LASTEXITCODE -ne 0) {
            throw "Checkpoint failed: $Result"
        }
        
        return $true
    }
    catch {
        Write-Log "Error saat checkpoint: $_" "ERROR"
        return $false
    }
}


# Fungsi untuk membersihkan backup lama
function Remove-OldBackups {
    param(
        [string]$BackupDirectory,
        [int]$KeepCount
    )
    
    Write-Log "Membersihkan backup lama (keep: $KeepCount)..."
    
    $BackupFiles = Get-ChildItem -Path $BackupDirectory -Filter "simanis62_backup_*.zip" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending
    
    if ($BackupFiles.Count -gt $KeepCount) {
        $FilesToDelete = $BackupFiles | Select-Object -Skip $KeepCount
        
        foreach ($file in $FilesToDelete) {
            Write-Log "Menghapus backup lama: $($file.Name)"
            Remove-Item $file.FullName -Force
            
            # Hapus juga file .db jika ada
            $DbFile = $file.FullName -replace '\.zip$', '.db'
            if (Test-Path $DbFile) {
                Remove-Item $DbFile -Force
            }
        }
        
        Write-Log "Berhasil menghapus $($FilesToDelete.Count) backup lama"
    }
    else {
        Write-Log "Tidak ada backup lama yang perlu dihapus"
    }
}

# Main script
try {
    Write-Log "=========================================="
    Write-Log "SIMANIS62 Database Backup"
    Write-Log "=========================================="
    Write-Log "Database: $DatabasePath"
    Write-Log "Backup Dir: $BackupDir"
    Write-Log "Retention: $RetentionCount backups"
    
    # Validasi database exists
    if (-not (Test-Path $DatabasePath)) {
        throw "Database tidak ditemukan: $DatabasePath"
    }
    
    # Buat direktori backup jika belum ada
    if (-not (Test-Path $BackupDir)) {
        Write-Log "Membuat direktori backup: $BackupDir"
        New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    }
    
    # Step 1: Checkpoint WAL
    Write-Log "Step 1: WAL Checkpoint"
    $CheckpointSuccess = Invoke-WalCheckpoint -DbPath $DatabasePath
    
    if (-not $CheckpointSuccess) {
        Write-Log "Warning: Checkpoint gagal, melanjutkan backup..." "WARN"
    }
    
    # Step 2: Copy database file
    Write-Log "Step 2: Copying database file"
    Copy-Item -Path $DatabasePath -Destination $BackupDbPath -Force
    Write-Log "Database copied to: $BackupDbPath"
    
    # Verifikasi ukuran file
    $OriginalSize = (Get-Item $DatabasePath).Length
    $BackupSize = (Get-Item $BackupDbPath).Length
    Write-Log "Original size: $([math]::Round($OriginalSize / 1MB, 2)) MB"
    Write-Log "Backup size: $([math]::Round($BackupSize / 1MB, 2)) MB"
    
    # Step 3: Compress to ZIP
    Write-Log "Step 3: Compressing to ZIP"
    Compress-Archive -Path $BackupDbPath -DestinationPath $BackupZipPath -Force
    
    $ZipSize = (Get-Item $BackupZipPath).Length
    $CompressionRatio = [math]::Round(($ZipSize / $BackupSize) * 100, 1)
    Write-Log "ZIP size: $([math]::Round($ZipSize / 1MB, 2)) MB (compression: $CompressionRatio%)"
    
    # Step 4: Remove temporary .db file
    Write-Log "Step 4: Cleaning up temporary files"
    Remove-Item $BackupDbPath -Force
    Write-Log "Temporary .db file removed"
    
    # Step 5: Cleanup old backups
    Write-Log "Step 5: Retention cleanup"
    Remove-OldBackups -BackupDirectory $BackupDir -KeepCount $RetentionCount
    
    # Summary
    Write-Log "=========================================="
    Write-Log "Backup completed successfully!"
    Write-Log "Backup file: $BackupZipPath"
    Write-Log "=========================================="
    
    # Return success
    exit 0
}
catch {
    Write-Log "BACKUP FAILED: $_" "ERROR"
    Write-Log "Stack trace: $($_.ScriptStackTrace)" "ERROR"
    
    # Cleanup partial backup if exists
    if (Test-Path $BackupDbPath) {
        Remove-Item $BackupDbPath -Force -ErrorAction SilentlyContinue
    }
    if (Test-Path $BackupZipPath) {
        Remove-Item $BackupZipPath -Force -ErrorAction SilentlyContinue
    }
    
    exit 1
}
    
