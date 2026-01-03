"""MCP Doku Tool - Tools Package.

Eingabe (reader):
    - read_module: Modul-Code lesen
    - find_modules: Module suchen
    - module_dependencies: Abhängigkeiten anzeigen
    - module_stats: Modul-Statistiken

Verarbeitung (tracker):
    - check_changes: Änderungen prüfen
    - check_all_changes: Alle Module prüfen
    - mark_documented: Als dokumentiert markieren
    - unmark_documented: Markierung entfernen
    - list_documented: Dokumentierte Module listen
    - documentation_stats: Statistiken

Ausgabe (writer):
    - write_doc: Dokumentation schreiben
    - read_doc: Dokumentation lesen
    - list_docs: Dokumentation auflisten
    - delete_doc: Dokumentation löschen
"""
from .reader import (
    read_module,
    find_modules,
    module_dependencies,
    module_stats,
)

from .tracker import (
    check_changes,
    check_all_changes,
    mark_documented,
    unmark_documented,
    list_documented,
    documentation_stats,
)

from .writer import (
    write_doc,
    read_doc,
    list_docs,
    delete_doc,
)

__all__ = [
    # Reader (Eingabe)
    "read_module",
    "find_modules",
    "module_dependencies",
    "module_stats",
    # Tracker (Verarbeitung)
    "check_changes",
    "check_all_changes",
    "mark_documented",
    "unmark_documented",
    "list_documented",
    "documentation_stats",
    # Writer (Ausgabe)
    "write_doc",
    "read_doc",
    "list_docs",
    "delete_doc",
]
