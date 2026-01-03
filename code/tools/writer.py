"""Dokumentations-Schreib-Tools (Ausgabe).

Funktionen zum Schreiben und Lesen von Dokumentation.
"""
from __future__ import annotations

from pathlib import Path


def write_doc(config, doc_type: str, name: str, content: str) -> str:
    """Schreibt eine Dokumentations-Datei.

    Args:
        config: Konfiguration
        doc_type: 'module', 'table', 'flow' oder 'note'
        name: Name der Datei (ohne .md)
        content: Markdown-Inhalt
        
    Returns:
        Bestätigung oder Fehlermeldung
    """
    if doc_type not in config.doc_types:
        return f"Ungültiger Typ '{doc_type}'. Erlaubt: {config.doc_types}"

    folder = config.docs_root / f"{doc_type}s"
    folder.mkdir(parents=True, exist_ok=True)

    # Dateiname bereinigen
    safe_name = sanitize_filename(name)
    filepath = folder / f"{safe_name}.md"

    filepath.write_text(content, encoding="utf-8")
    return f"Geschrieben: {filepath}"


def read_doc(config, doc_type: str, name: str) -> str:
    """Liest eine existierende Dokumentations-Datei.
    
    Args:
        config: Konfiguration
        doc_type: 'module', 'table', 'flow' oder 'note'
        name: Name der Datei (ohne .md)
        
    Returns:
        Dateiinhalt oder Fehlermeldung
    """
    if doc_type not in config.doc_types:
        return f"Ungültiger Typ '{doc_type}'. Erlaubt: {config.doc_types}"
    
    safe_name = sanitize_filename(name)
    filepath = config.docs_root / f"{doc_type}s" / f"{safe_name}.md"

    if not filepath.exists():
        return f"Dokumentation nicht gefunden: {filepath}"

    return filepath.read_text(encoding="utf-8")


def list_docs(config, doc_type: str = "") -> str:
    """Listet vorhandene Dokumentation auf.
    
    Args:
        config: Konfiguration
        doc_type: Optional - 'module', 'table', 'flow' oder 'note'. Leer = alle.
        
    Returns:
        Liste der Dokumente oder Fehlermeldung
    """
    if doc_type:
        if doc_type not in config.doc_types:
            return f"Ungültiger Typ '{doc_type}'. Erlaubt: {config.doc_types}"
        folder = config.docs_root / f"{doc_type}s"
        if not folder.exists():
            return f"Keine Dokumentation vom Typ: {doc_type}"
        files = sorted(folder.glob("*.md"))
    else:
        if not config.docs_root.exists():
            return "Dokumentationsverzeichnis existiert noch nicht"
        files = sorted(config.docs_root.rglob("*.md"))

    if not files:
        return "Keine Dokumentation vorhanden"

    # Gruppiert nach Typ ausgeben
    if not doc_type:
        result = []
        for dt in config.doc_types:
            folder = config.docs_root / f"{dt}s"
            if folder.exists():
                type_files = sorted(folder.glob("*.md"))
                if type_files:
                    result.append(f"\n{dt.upper()}S ({len(type_files)}):")
                    for f in type_files[:15]:
                        result.append(f"  - {f.stem}")
                    if len(type_files) > 15:
                        result.append(f"  ... und {len(type_files) - 15} weitere")
        return "\n".join(result) if result else "Keine Dokumentation vorhanden"
    
    return "\n".join(f.stem for f in files[:50])


def delete_doc(config, doc_type: str, name: str) -> str:
    """Löscht eine Dokumentations-Datei.
    
    Args:
        config: Konfiguration
        doc_type: 'module', 'table', 'flow' oder 'note'
        name: Name der Datei (ohne .md)
        
    Returns:
        Bestätigung oder Fehlermeldung
    """
    if doc_type not in config.doc_types:
        return f"Ungültiger Typ '{doc_type}'. Erlaubt: {config.doc_types}"
    
    safe_name = sanitize_filename(name)
    filepath = config.docs_root / f"{doc_type}s" / f"{safe_name}.md"

    if not filepath.exists():
        return f"Dokumentation nicht gefunden: {filepath}"

    filepath.unlink()
    return f"Gelöscht: {filepath}"


def sanitize_filename(name: str) -> str:
    """Bereinigt einen Namen für die Verwendung als Dateiname."""
    return name.replace("::", "_").replace("/", "_").replace("\\", "_")
