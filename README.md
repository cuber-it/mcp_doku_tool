# MCP Doku Tool

MCP-Server zum Erschließen und Dokumentieren von Legacy-Code.  
Speichert Dokumentation als Markdown (Obsidian-kompatibel).

## Features

- **Code lesen**: Module lesen und analysieren
- **Module finden**: Nach Modulen suchen
- **Abhängigkeiten**: use/require Statements extrahieren
- **Dokumentation schreiben**: Markdown-Dateien in strukturierten Ordnern
- **Änderungserkennung**: Hash-basiert prüfen ob Module sich geändert haben
- **CLI**: Vollständige Kommandozeilen-Schnittstelle

Primär für Perl-Projekte entwickelt, aber anpassbar für andere Sprachen.

## Installation

```bash
git clone https://github.com/ucuber/mcp_doku_tool.git
cd mcp_doku_tool
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Konfiguration

```bash
# Beispiel-Config als Vorlage
cp config/config.example.yaml config/.myproject.yaml
```

Anpassen:

```yaml
project:
  root: "/pfad/zum/projekt"
  lib_subdir: "lib"
  file_extension: ".pm"
  module_separator: "::"

docs:
  root: "~/Documents/projekt-docs"
  types: [module, table, flow, note]

server:
  name: "mein-doku-tool"
  transport: "stdio"
  http_port: 8080

limits:
  max_file_size: 20000
  max_results: 50
```

**Hinweis:** Configs mit `.` Prefix (z.B. `.myproject.yaml`) werden von Git ignoriert.

## CLI

```bash
# Server starten
python code/main.py -c config/.myproject.yaml serve

# HTTP-Modus zum Testen
python code/main.py -c config/.myproject.yaml serve --http 8080

# Module suchen
python code/main.py -c config/.myproject.yaml find Payment

# Änderungen prüfen
python code/main.py -c config/.myproject.yaml check --all

# Statistiken
python code/main.py -c config/.myproject.yaml stats
```

## Claude Desktop Integration

`run.sh` anpassen (Config-Pfad setzen), dann in `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mein-doku-tool": {
      "command": "/pfad/zu/mcp_doku_tool/run.sh"
    }
  }
}
```

## Projektstruktur

```
mcp_doku_tool/
├── code/
│   ├── main.py          # CLI Entry Point
│   ├── config.py        # Konfigurationsmanagement
│   ├── server.py        # MCP Server
│   └── tools/           # EVA-Struktur
│       ├── reader.py    # Eingabe: Code lesen
│       ├── tracker.py   # Verarbeitung: Änderungsverfolgung
│       └── writer.py    # Ausgabe: Doku schreiben
├── config/
│   └── config.example.yaml
├── templates/
│   └── module.md
├── tests/
└── run.sh
```

## MCP Tools

| Tool | Beschreibung |
|------|-------------|
| `read_module` | Liest ein Modul |
| `find_modules` | Sucht Module nach Pattern |
| `module_dependencies` | Zeigt Abhängigkeiten |
| `module_stats` | Modul-Statistiken |
| `check_changes` | Prüft ob Modul geändert |
| `check_all_changes` | Prüft alle Module |
| `mark_documented` | Markiert als dokumentiert |
| `unmark_documented` | Entfernt Markierung |
| `list_documented` | Listet dokumentierte Module |
| `documentation_stats` | Statistiken |
| `write_doc` | Schreibt Dokumentation |
| `read_doc` | Liest Dokumentation |
| `list_docs` | Listet Dokumentation |
| `delete_doc` | Löscht Dokumentation |

## Lizenz

MIT - siehe [LICENSE](LICENSE)
