#!/bin/bash
# Start DBHub for SIMANIS62 V2 Development
# Usage: ./scripts/start_dbhub.sh [environment] [port]

ENVIRONMENT=${1:-development}
PORT=${2:-8080}

echo "🚀 Starting DBHub for SIMANIS62 V2..."
echo "Environment: $ENVIRONMENT"
echo "Port: $PORT"
echo ""

# Check if dbhub is installed
if ! command -v dbhub &> /dev/null; then
    echo "❌ DBHub not found. Installing..."
    npm install -g @bytebase/dbhub
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install DBHub"
        exit 1
    fi
fi

# Check if config file exists
if [ ! -f "dbhub.toml" ]; then
    echo "❌ dbhub.toml not found in current directory"
    echo "Please run this script from project root"
    exit 1
fi

# Check if development database exists
if [ "$ENVIRONMENT" = "development" ]; then
    if [ ! -f "backend/simanis62-dev.db" ]; then
        echo "⚠️  Development database not found. Creating..."
        python -c "import sqlite3; conn = sqlite3.connect('backend/simanis62-dev.db'); conn.execute('PRAGMA journal_mode=WAL'); conn.execute('CREATE TABLE IF NOT EXISTS _init (id INTEGER PRIMARY KEY, created_at TEXT DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close(); print('✅ Development database created')"
    fi
fi

echo ""
echo "✅ Starting DBHub..."
echo "📊 Workbench URL: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start DBHub
dbhub --config dbhub.toml --env "$ENVIRONMENT" --port "$PORT"
