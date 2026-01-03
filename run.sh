#!/bin/bash
# Startet den MCP Doku Tool Server aus dem venv
# Verwende dieses Script in der Claude Desktop Config
#
# Nutzung:
#   ./run.sh -c config/meine-config.yaml
#   ./run.sh -c config/meine-config.yaml --http 8080

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec "$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/code/main.py" "$@" serve
