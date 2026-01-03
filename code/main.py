#!/usr/bin/env python3
"""MCP Doku Tool - Haupteinstiegspunkt.

Ein MCP-Server zum Erschließen und Dokumentieren von Legacy-Code.
Speichert Dokumentation als Markdown (Obsidian-kompatibel).

Aufruf:
    python code/main.py serve                    # MCP-Server starten (stdio)
    python code/main.py serve --http 8080        # HTTP-Modus
    python code/main.py serve -c config.yaml     # Mit Config-Datei
    python code/main.py check Order::Validation  # Einzelnes Modul prüfen
    python code/main.py check --all              # Alle Module prüfen
    python code/main.py stats                    # Statistiken anzeigen
"""
import argparse
import sys
from pathlib import Path

# code/ zum Pfad hinzufügen für direkte Ausführung
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config, apply_cli_overrides, Config


def create_parser() -> argparse.ArgumentParser:
    """Erstellt den Argument-Parser."""
    parser = argparse.ArgumentParser(
        prog="mcp-doku-tool",
        description="MCP-Server für Code-Dokumentation. "
                    "Hilft beim Erschließen und Dokumentieren von Legacy-Code.",
        epilog="Beispiele:\n"
               "  %(prog)s serve                     Startet den MCP-Server\n"
               "  %(prog)s serve --http 8080         HTTP-Modus auf Port 8080\n"
               "  %(prog)s serve -c myconfig.yaml    Mit Config-Datei\n"
               "  %(prog)s check Order::Validation   Prüft ein Modul auf Änderungen\n"
               "  %(prog)s check --all               Prüft alle dokumentierten Module\n"
               "  %(prog)s stats                     Zeigt Dokumentations-Statistiken\n"
               "  %(prog)s list                      Listet dokumentierte Module\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Globale Optionen
    parser.add_argument(
        "-c", "--config",
        type=Path,
        metavar="FILE",
        help="Pfad zur Config-Datei (YAML)",
    )
    parser.add_argument(
        "-p", "--project-root",
        type=Path,
        metavar="DIR",
        help="Projekt-Wurzelverzeichnis (überschreibt Config)",
    )
    parser.add_argument(
        "-d", "--docs-root",
        type=Path,
        metavar="DIR",
        help="Dokumentations-Verzeichnis (überschreibt Config)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Ausführliche Ausgabe",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest="command",
        title="Befehle",
        description="Verfügbare Befehle (--help für Details)",
    )
    
    # serve - Server starten
    serve_parser = subparsers.add_parser(
        "serve",
        help="MCP-Server starten",
        description="Startet den MCP-Server. Standard: stdio-Modus für Claude Desktop.",
    )
    serve_parser.add_argument(
        "--http",
        type=int,
        metavar="PORT",
        nargs="?",
        const=8080,
        help="HTTP-Modus statt stdio (Standard-Port: 8080)",
    )
    
    # check - Änderungen prüfen
    check_parser = subparsers.add_parser(
        "check",
        help="Module auf Änderungen prüfen",
        description="Prüft ob sich Module seit der letzten Dokumentation geändert haben.",
    )
    check_parser.add_argument(
        "module",
        nargs="?",
        metavar="MODULE",
        help="Modulname (z.B. Order::Validation)",
    )
    check_parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Alle dokumentierten Module prüfen",
    )
    
    # stats - Statistiken
    subparsers.add_parser(
        "stats",
        help="Dokumentations-Statistiken anzeigen",
        description="Zeigt eine Übersicht über die vorhandene Dokumentation.",
    )
    
    # list - Dokumentierte Module auflisten
    list_parser = subparsers.add_parser(
        "list",
        help="Dokumentierte Module auflisten",
        description="Listet alle als dokumentiert markierten Module auf.",
    )
    list_parser.add_argument(
        "-t", "--type",
        choices=["module", "table", "flow", "note"],
        help="Nur bestimmten Dokumentationstyp anzeigen",
    )
    
    # find - Module suchen
    find_parser = subparsers.add_parser(
        "find",
        help="Module suchen",
        description="Sucht Module nach einem Muster.",
    )
    find_parser.add_argument(
        "pattern",
        metavar="PATTERN",
        help="Suchmuster",
    )
    
    # init - Config-Datei erstellen
    init_parser = subparsers.add_parser(
        "init",
        help="Beispiel-Config erstellen",
        description="Erstellt eine Beispiel-Konfigurationsdatei.",
    )
    init_parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("config.yaml"),
        metavar="FILE",
        help="Ausgabedatei (Standard: config.yaml)",
    )
    
    return parser


def get_config(args: argparse.Namespace) -> Config:
    """Lädt und überschreibt die Konfiguration basierend auf CLI-Argumenten."""
    # Config aus Datei laden (falls angegeben)
    config = load_config(args.config)
    
    # CLI-Overrides anwenden
    overrides = {}
    if args.project_root:
        overrides["project_root"] = args.project_root
    if args.docs_root:
        overrides["docs_root"] = args.docs_root
    
    return apply_cli_overrides(config, **overrides)


def cmd_serve(args: argparse.Namespace, config: Config) -> int:
    """Server starten."""
    from server import run_server
    
    if args.http:
        config.transport = "http"
        config.http_port = args.http
        print(f"Starte HTTP-Server auf Port {config.http_port}...")
    else:
        print("Starte MCP-Server (stdio)...", file=sys.stderr)
    
    if args.verbose:
        print(f"Projekt: {config.project_root}", file=sys.stderr)
        print(f"Doku: {config.docs_root}", file=sys.stderr)
    
    run_server(config)
    return 0


def cmd_check(args: argparse.Namespace, config: Config) -> int:
    """Änderungen prüfen."""
    import tools
    
    if args.all:
        print(tools.check_all_changes(config))
    elif args.module:
        print(tools.check_changes(config, args.module))
    else:
        print("Fehler: Modulname oder --all angeben", file=sys.stderr)
        return 1
    return 0


def cmd_stats(args: argparse.Namespace, config: Config) -> int:
    """Statistiken anzeigen."""
    import tools
    print(tools.documentation_stats(config))
    return 0


def cmd_list(args: argparse.Namespace, config: Config) -> int:
    """Module auflisten."""
    import tools
    
    if args.type:
        print(tools.list_docs(config, args.type))
    else:
        print("=== Dokumentierte Module ===")
        print(tools.list_documented(config))
        print("\n=== Dokumentations-Dateien ===")
        print(tools.list_docs(config))
    return 0


def cmd_find(args: argparse.Namespace, config: Config) -> int:
    """Module suchen."""
    import tools
    print(tools.find_modules(config, args.pattern))
    return 0


def cmd_init(args: argparse.Namespace, config: Config) -> int:
    """Beispiel-Config erstellen."""
    example_config = """\
# MCP Doku Tool Konfiguration

project:
  # Wurzelverzeichnis des zu dokumentierenden Projekts
  root: "/path/to/your/project"
  # Unterverzeichnis mit dem Code
  lib_subdir: "lib"
  # Dateiendung der Module
  file_extension: ".pm"
  # Trennzeichen in Modulnamen (Perl: "::", Python: ".")
  module_separator: "::"

docs:
  # Wo die Dokumentation gespeichert wird
  root: "~/Documents/project-docs"
  # Erlaubte Dokumentationstypen
  types:
    - module
    - table
    - flow
    - note

server:
  # Name des MCP-Servers
  name: "doku-tool"
  # Transport: "stdio" oder "http"
  transport: "stdio"
  # Port für HTTP-Modus
  http_port: 8080

limits:
  # Maximale Dateigröße für Ausgabe (Zeichen)
  max_file_size: 15000
  # Maximale Anzahl Suchergebnisse
  max_results: 30
"""
    
    output = args.output
    if output.exists():
        print(f"Fehler: {output} existiert bereits", file=sys.stderr)
        return 1
    
    output.write_text(example_config, encoding="utf-8")
    print(f"Config erstellt: {output}")
    print("Bitte anpassen und mit -c verwenden.")
    return 0


def main() -> int:
    """Hauptfunktion."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Ohne Command: Help anzeigen
    if not args.command:
        parser.print_help()
        return 0
    
    # Config laden (außer für init)
    if args.command != "init":
        config = get_config(args)
    else:
        config = Config()  # Dummy für init
    
    # Command ausführen
    commands = {
        "serve": cmd_serve,
        "check": cmd_check,
        "stats": cmd_stats,
        "list": cmd_list,
        "find": cmd_find,
        "init": cmd_init,
    }
    
    return commands[args.command](args, config)


if __name__ == "__main__":
    sys.exit(main())
