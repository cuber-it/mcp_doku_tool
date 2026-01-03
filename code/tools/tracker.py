"""Änderungs-Tracking-Tools (Verarbeitung).

Funktionen zur Verfolgung von Code-Änderungen via Hashes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional


def _load_hashes(config) -> dict:
    """Lädt die gespeicherten Hashes."""
    if config.hash_file.exists():
        return json.loads(config.hash_file.read_text(encoding="utf-8"))
    return {}


def _save_hashes(config, hashes: dict) -> None:
    """Speichert die Hashes."""
    config.hash_file.parent.mkdir(parents=True, exist_ok=True)
    config.hash_file.write_text(json.dumps(hashes, indent=2, sort_keys=True), encoding="utf-8")


def _compute_hash(filepath: Path) -> Optional[str]:
    """Berechnet den MD5-Hash einer Datei."""
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding="utf-8", errors="replace")
    return hashlib.md5(content.encode()).hexdigest()


def check_changes(config, module_name: str) -> str:
    """Prüft ob sich ein Modul seit der letzten Dokumentation geändert hat.
    
    Args:
        config: Konfiguration
        module_name: Modulname
        
    Returns:
        Status-Meldung
    """
    full_path = config.module_to_path(module_name)
    current_hash = _compute_hash(full_path)
    
    if current_hash is None:
        return f"Modul nicht gefunden: {module_name}"

    hashes = _load_hashes(config)
    stored_hash = hashes.get(module_name)

    if stored_hash is None:
        return f"{module_name}: Noch nie dokumentiert"
    elif stored_hash != current_hash:
        return f"{module_name}: GEÄNDERT seit letzter Dokumentation"
    else:
        return f"{module_name}: Unverändert"


def mark_documented(config, module_name: str) -> str:
    """Markiert ein Modul als dokumentiert (speichert Hash).
    
    Args:
        config: Konfiguration
        module_name: Modulname
        
    Returns:
        Bestätigung oder Fehlermeldung
    """
    full_path = config.module_to_path(module_name)
    current_hash = _compute_hash(full_path)
    
    if current_hash is None:
        return f"Modul nicht gefunden: {module_name}"

    hashes = _load_hashes(config)
    hashes[module_name] = current_hash
    _save_hashes(config, hashes)

    return f"{module_name}: Als dokumentiert markiert"


def unmark_documented(config, module_name: str) -> str:
    """Entfernt die Dokumentations-Markierung für ein Modul.
    
    Args:
        config: Konfiguration
        module_name: Modulname
        
    Returns:
        Bestätigung oder Fehlermeldung
    """
    hashes = _load_hashes(config)
    
    if module_name not in hashes:
        return f"{module_name}: War nicht als dokumentiert markiert"
    
    del hashes[module_name]
    _save_hashes(config, hashes)
    
    return f"{module_name}: Markierung entfernt"


def check_all_changes(config) -> str:
    """Prüft alle dokumentierten Module auf Änderungen.
    
    Args:
        config: Konfiguration
        
    Returns:
        Zusammenfassung der Änderungen
    """
    hashes = _load_hashes(config)
    
    if not hashes:
        return "Keine Module als dokumentiert markiert"
    
    changed = []
    unchanged = []
    missing = []
    
    for module_name, stored_hash in sorted(hashes.items()):
        full_path = config.module_to_path(module_name)
        current_hash = _compute_hash(full_path)
        
        if current_hash is None:
            missing.append(module_name)
        elif current_hash != stored_hash:
            changed.append(module_name)
        else:
            unchanged.append(module_name)
    
    result = []
    if changed:
        result.append(f"GEÄNDERT ({len(changed)}):")
        for m in changed:
            result.append(f"  ⚠ {m}")
    if missing:
        result.append(f"\nNICHT GEFUNDEN ({len(missing)}):")
        for m in missing:
            result.append(f"  ✗ {m}")
    if unchanged:
        result.append(f"\nUnverändert: {len(unchanged)} Module")
    
    return "\n".join(result) if result else "Keine Module dokumentiert"


def list_documented(config) -> str:
    """Listet alle als dokumentiert markierten Module.
    
    Args:
        config: Konfiguration
        
    Returns:
        Liste der Module
    """
    hashes = _load_hashes(config)
    
    if not hashes:
        return "Keine Module als dokumentiert markiert"
    
    return "\n".join(sorted(hashes.keys()))


def documentation_stats(config) -> str:
    """Gibt Statistiken über die Dokumentation aus.
    
    Args:
        config: Konfiguration
        
    Returns:
        Statistik-Übersicht
    """
    hashes = _load_hashes(config)
    
    # Zähle Doku-Dateien
    doc_counts = {}
    for doc_type in config.doc_types:
        folder = config.docs_root / f"{doc_type}s"
        if folder.exists():
            doc_counts[doc_type] = len(list(folder.glob("*.md")))
        else:
            doc_counts[doc_type] = 0
    
    total_docs = sum(doc_counts.values())
    
    result = [
        "Dokumentations-Statistik",
        "=" * 30,
        f"Verfolgte Module: {len(hashes)}",
        f"Dokumentationen: {total_docs}",
        "",
        "Nach Typ:",
    ]
    for doc_type, count in doc_counts.items():
        result.append(f"  {doc_type}s: {count}")
    
    return "\n".join(result)
