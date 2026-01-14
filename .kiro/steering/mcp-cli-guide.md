---
inclusion: manual
---

# MCP-CLI Guide

## Overview

mcp-cli adalah lightweight CLI untuk berinteraksi dengan MCP servers dari terminal. Berguna untuk testing, debugging, dan scripting dengan MCP tools.

## Installation

```powershell
# Sudah terinstall via Bun
bun install -g https://github.com/philschmid/mcp-cli

# Alias di PowerShell profile (~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1)
function mcp-cli { bun C:\Users\24riz\.bun\install\global\node_modules\mcp-cli\src\index.ts $args }
```

## Configuration

Config file: `C:\Users\24riz\.config\mcp\mcp_servers.json`

### Available Servers

| Server | Command | Tools |
|--------|---------|-------|
| analyzer | uvx mcp-server-analyzer | ruff-check, ruff-format, vulture-scan, analyze-code |
| fetch | uvx mcp-server-fetch | fetch |
| filesystem | npx @modelcontextprotocol/server-filesystem | read_file, list_directory, search_files |
| serena | uvx serena | find_symbol, replace_content, execute_shell_command |
| maxential-thinking | npx @bam-devcrew/maxential-thinking-mcp | think, branch, complete |
| sequential-thinking | npx @modelcontextprotocol/server-sequential-thinking | sequentialthinking |
| basic-memory | uvx basic-memory mcp | write_note, read_note, search_notes |
| drawio | npx @next-ai-drawio/mcp-server | create_new_diagram, edit_diagram |
| playwright | npx @playwright/mcp | browser_navigate, browser_click |
| aws-diagram | uvx awslabs.aws-diagram-mcp-server | generate_diagram |
| aws-docs | uvx awslabs.aws-documentation-mcp-server | search_documentation |
| sqlite | uvx mcp-server-sqlite | list_tables, execute_query |
| dbhub | dbhub | list_tables, execute_sql |

## Usage

```powershell
# List semua servers dan tools
mcp-cli

# List dengan deskripsi
mcp-cli -d

# Search tools by pattern
mcp-cli grep "*ruff*"

# Lihat detail server
mcp-cli analyzer

# Lihat schema tool
mcp-cli analyzer/ruff-check

# Panggil tool
mcp-cli analyzer/analyze-code '{"code": "import os\nx = 1"}'

# Output JSON untuk scripting
mcp-cli analyzer/ruff-check '{"code": "x=1"}' --json
```

## Useful Commands for SIMANIS62

```powershell
# Analyze Python code quality
mcp-cli analyzer/analyze-code '{"code": "def foo():\n    pass"}'

# Check for dead code
mcp-cli analyzer/vulture-scan '{"code": "import os\nimport sys\nprint(os.getcwd())"}'

# Lint with Ruff
mcp-cli analyzer/ruff-check '{"code": "x=1\ny=2"}'

# Format code
mcp-cli analyzer/ruff-format '{"code": "x=1\ny=2"}'

# Fetch URL content
mcp-cli fetch/fetch '{"url": "https://example.com"}'
```

## Notes

- mcp-cli connects to ALL servers when listing, which can be slow
- Use `mcp-cli <server>` to connect to single server (faster)
- Servers run via stdio, not HTTP
- Config compatible dengan Claude Desktop dan VS Code format
