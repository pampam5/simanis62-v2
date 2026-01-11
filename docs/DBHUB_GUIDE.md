# DBHub Setup Guide - SIMANIS62 V2

## Apa itu DBHub?

DBHub adalah MCP server untuk database management yang menyediakan:
- Visual interface untuk explore database
- Query testing dan optimization
- Multi-database support (dev/test/prod)
- MCP tools untuk database operations

## Installation

### Via NPX (Recommended)
```bash
# Install dan run langsung
npx @bytebase/dbhub --config dbhub.toml --port 8080
```

### Via NPM Global
```bash
# Install global
npm install -g @bytebase/dbhub

# Run
dbhub --config dbhub.toml --port 8080
```

### Via Docker
```bash
docker run -p 8080:8080 \
  -v $(pwd)/dbhub.toml:/app/dbhub.toml \
  -v $(pwd)/backend:/app/backend \
  bytebase/dbhub --config /app/dbhub.toml
```

## Configuration

File `dbhub.toml` sudah dikonfigurasi dengan 3 database sources:

### Correct TOML Format
DBHub menggunakan `[[sources]]` array syntax dengan field wajib:
- `id` - Unique identifier untuk database
- `name` - Display name
- `type` - Database type ("sqlite", "postgres", "mysql", dll)
- `database` - Database path atau connection string

### 1. Development
```toml
[[sources]]
id = "development"
name = "SIMANIS62 Development"
type = "sqlite"
database = "D:/simanis62-v2/backend/simanis62-dev.db"
```

**Use Case**: Daily development dan testing

### 2. Testing
```toml
[[sources]]
id = "testing"
name = "SIMANIS62 Testing"
type = "sqlite"
database = ":memory:"
```

**Use Case**: Unit testing dengan in-memory database

### 3. Production
```toml
[[sources]]
id = "production"
name = "SIMANIS62 Production"
type = "sqlite"
database = "C:/ProgramData/Simanis62/simanis62.db"
```

**Use Case**: Read-only access ke production database (untuk debugging)

### Important Notes:
- ⚠️ Use **absolute paths** for database files
- ⚠️ Use `type` not `driver` for SQLite
- ⚠️ Each source must have unique `id`
- ⚠️ Use `[[sources]]` array syntax, not `[section]`

## Usage

### 1. Start DBHub Server
```bash
# Using absolute path (recommended for MCP)
dbhub --config D:\simanis62-v2\dbhub.toml --port 8080

# Using quick start script (PowerShell)
.\scripts\start_dbhub.ps1

# Using quick start script (Bash)
./scripts/start_dbhub.sh

# With custom port
.\scripts\start_dbhub.ps1 -Port 8081
```

### 2. Access Workbench
Buka browser: http://localhost:8080

### 3. Available MCP Tools

DBHub menyediakan tools per database source:

#### Search Objects
```
Tools:
  - mcp_dbhub_search_objects_development
  - mcp_dbhub_search_objects_testing
  - mcp_dbhub_search_objects_production

Parameters:
  - object_type: "table" | "column" | "index" | "schema" | "procedure"
  - pattern: SQL LIKE pattern (default: "%")
  - detail_level: "names" | "summary" | "full"
  - schema: Filter by schema (optional)
  - table: Filter by table (optional, for columns/indexes)
  - limit: Max results (default: 100, max: 1000)

Description: Search and list database objects
```

#### Execute SQL
```
Tools:
  - mcp_dbhub_execute_sql_development
  - mcp_dbhub_execute_sql_testing
  - mcp_dbhub_execute_sql_production

Parameters:
  - sql: SQL query to execute (multiple statements separated by ;)

Description: Execute SQL queries and get results
```

## Common Use Cases

### 1. Explore Database Schema
```sql
-- List all tables
SELECT name FROM sqlite_master WHERE type='table';

-- Describe table structure
PRAGMA table_info(aset);

-- Check relationships
SELECT * FROM sqlite_master WHERE type='foreign_key';
```

### 2. Test Queries untuk KIB Reports
```sql
-- Test query untuk KIB B
SELECT
    nomor_register,
    nama_barang,
    kode_barang,
    harga,
    tahun_perolehan
FROM aset
WHERE jenis_kib = 'B'
ORDER BY nomor_register;
```

### 3. Verify Data Integrity
```sql
-- Check duplicate kode_barang
SELECT kode_barang, COUNT(*) as count
FROM aset
GROUP BY kode_barang
HAVING count > 1;

-- Check orphaned records
SELECT a.* FROM aset a
LEFT JOIN ruangan r ON a.ruangan_id = r.id
WHERE r.id IS NULL;
```

### 4. Performance Testing
```sql
-- Test query performance
EXPLAIN QUERY PLAN
SELECT * FROM aset WHERE kode_barang = '02.06.01.0001';

-- Check indexes
SELECT * FROM sqlite_master WHERE type='index';
```

## Integration dengan Kiro

DBHub dapat digunakan langsung dari Kiro sebagai MCP server:

### 1. Add to MCP Config
```json
{
  "mcpServers": {
    "dbhub": {
      "command": "dbhub",
      "args": [
        "--config",
        "D:\\simanis62-v2\\dbhub.toml"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "list_tables",
        "describe_table",
        "execute_query",
        "get_schema"
      ],
      "description": "DBHub - Visual database management untuk SIMANIS62 V2"
    }
  }
}
```

**Important**:
- Use absolute path untuk `--config` argument
- Tidak perlu `--port` untuk MCP (uses stdio)
- Tidak perlu `--env` karena semua sources tersedia

### 2. Use dari Kiro
```
User: "List all tables in development database"
Kiro: [calls mcp_dbhub_search_objects_development with object_type="table"]

User: "Show me all columns in aset table"
Kiro: [calls mcp_dbhub_search_objects_development with object_type="column", table="aset"]

User: "Run query: SELECT * FROM aset LIMIT 10"
Kiro: [calls mcp_dbhub_execute_sql_development with sql="SELECT * FROM aset LIMIT 10"]

User: "Check SQLite version"
Kiro: [calls mcp_dbhub_execute_sql_development with sql="SELECT sqlite_version()"]
```

## Development Workflow

### Phase 2: Database Models
```
1. Design model di SQLModel
2. Test di DBHub workbench
3. Implement di backend/app/models/
4. Verify di DBHub
5. Write unit tests
```

### Query Development
```
1. Write query di DBHub workbench
2. Test dengan sample data
3. Optimize dengan EXPLAIN QUERY PLAN
4. Implement di service layer
5. Verify results di DBHub
```

### Data Migration
```
1. Create migration script
2. Test di DBHub dengan development database
3. Backup production database
4. Run migration
5. Verify di DBHub
```

## Tips & Best Practices

### 1. Always Use Development Database
- Jangan langsung test di production
- Gunakan `backend/simanis62-dev.db` untuk development
- Copy production data ke dev jika perlu

### 2. Test Queries Before Implementation
- Test di DBHub workbench dulu
- Verify results
- Check performance dengan EXPLAIN QUERY PLAN
- Baru implement di code

### 3. Use Transactions
```sql
BEGIN TRANSACTION;
-- Your queries here
ROLLBACK; -- or COMMIT;
```

### 4. Monitor Performance
- Check query execution time di workbench
- Use EXPLAIN QUERY PLAN untuk optimization
- Add indexes jika perlu

### 5. Backup Before Major Changes
```bash
# Backup development database
cp backend/simanis62-dev.db backend/simanis62-dev.db.backup
```

## Troubleshooting

### MCP Connection Issues

#### Error: "Configuration file not found"
**Solution**: Use absolute path in MCP config
```json
"args": ["--config", "D:\\simanis62-v2\\dbhub.toml"]
```

#### Error: "must contain a [[sources]] array"
**Solution**: Check TOML syntax, use `[[sources]]` not `[section]`
```toml
# ✅ CORRECT
[[sources]]
id = "development"
name = "My Database"
type = "sqlite"
database = "/path/to/db.db"

# ❌ WRONG
[development]
name = "My Database"
driver = "sqlite"
database = "/path/to/db.db"
```

#### Error: "each source must have an 'id' field"
**Solution**: Add unique `id` to each source
```toml
[[sources]]
id = "development"  # ← Required!
name = "SIMANIS62 Development"
type = "sqlite"
database = "D:/simanis62-v2/backend/simanis62-dev.db"
```

#### Error: "source must have either 'dsn' field or connection parameters"
**Solution**: For SQLite, use `type` not `driver`
```toml
# ✅ CORRECT
type = "sqlite"

# ❌ WRONG
driver = "sqlite"
```

### Workbench Issues

#### Port Already in Use
```bash
# Use different port
dbhub --config D:\simanis62-v2\dbhub.toml --port 8081
```

#### Database Locked
```powershell
# Check for other connections (Windows)
Get-Process | Where-Object {$_.Path -like "*python*"}

# Close connections and retry
```

#### Cannot Connect to Database
```powershell
# Verify database exists
Test-Path D:\simanis62-v2\backend\simanis62-dev.db

# Check permissions
icacls D:\simanis62-v2\backend\simanis62-dev.db
```

## Security Notes

### Development
- ✅ DBHub workbench hanya untuk development
- ✅ Jangan expose ke public network
- ✅ Use localhost only (127.0.0.1)

### Production
- ⚠️ Production database di `dbhub.toml` adalah READ-ONLY
- ⚠️ Jangan run DBHub di production server
- ⚠️ Jangan commit database files ke git

## References

- [DBHub Official Docs](https://dbhub.ai/)
- [DBHub GitHub](https://github.com/bytebase/dbhub)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SIMANIS62 Data Schema](../../docs/data_schema.md)
- [MCP Configuration](.kiro/settings/mcp.json)
- [Quick Start Scripts](../../scripts/)

---

**Last Updated**: 2026-01-11
**Version**: 2.0 (Updated with correct TOML format and MCP integration)
