"""Code-Lese-Tools (Eingabe).

Funktionen zum Lesen und Analysieren von Quellcode.
"""
from __future__ import annotations

import re
from pathlib import Path


def read_module(config, module_name: str) -> str:
    """Liest ein Modul und gibt den Inhalt zurück.
    
    Args:
        config: Konfiguration
        module_name: Modulname (z.B. 'Order::Validation')
        
    Returns:
        Dateiinhalt oder Fehlermeldung
    """
    full_path = config.module_to_path(module_name)

    if not full_path.exists():
        return f"Modul nicht gefunden: {module_name}\nErwarteter Pfad: {full_path}"

    content = full_path.read_text(encoding="utf-8", errors="replace")

    if len(content) > config.max_file_size:
        content = (
            content[:config.max_file_size] + 
            f"\n\n... (gekürzt, Datei hat {len(content)} Zeichen)"
        )

    return content


def find_modules(config, pattern: str) -> str:
    """Findet Module die einem Muster entsprechen.
    
    Args:
        config: Konfiguration
        pattern: Suchmuster (Teil des Modulnamens)
        
    Returns:
        Liste gefundener Module oder Fehlermeldung
    """
    lib_path = config.lib_path
    
    if not lib_path.exists():
        return f"lib-Verzeichnis nicht gefunden: {lib_path}"
    
    ext = config.file_extension
    # Suche nach Pattern im Dateinamen ODER im Pfad
    all_files = list(lib_path.rglob(f"*{ext}"))
    matches = [f for f in all_files if pattern.lower() in str(f).lower()]

    if not matches:
        return f"Keine Module gefunden für: {pattern}"

    modules = []
    for m in sorted(matches)[:config.max_results]:
        modules.append(config.path_to_module(m))

    result = "\n".join(modules)
    if len(matches) > config.max_results:
        result += f"\n\n... und {len(matches) - config.max_results} weitere"
    
    return result


def module_dependencies(config, module_name: str) -> str:
    """Zeigt welche Module ein Modul verwendet.
    
    Args:
        config: Konfiguration
        module_name: Modulname
        
    Returns:
        Liste der Abhängigkeiten oder Fehlermeldung
    """
    full_path = config.module_to_path(module_name)

    if not full_path.exists():
        return f"Modul nicht gefunden: {module_name}"

    content = full_path.read_text(encoding="utf-8", errors="replace")

    # Regex für use/require Statements (Perl)
    uses = re.findall(r'^use\s+([\w:]+)', content, re.MULTILINE)
    requires = re.findall(r'^require\s+([\w:]+)', content, re.MULTILINE)

    deps = sorted(set(uses + requires))

    if not deps:
        return "Keine Abhängigkeiten gefunden"

    return "\n".join(deps)


def module_stats(config, module_name: str) -> str:
    """Gibt Statistiken über ein Modul aus.
    
    Args:
        config: Konfiguration
        module_name: Modulname
        
    Returns:
        Statistiken (Zeilen, Funktionen, etc.)
    """
    full_path = config.module_to_path(module_name)

    if not full_path.exists():
        return f"Modul nicht gefunden: {module_name}"

    content = full_path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    
    # Perl-spezifische Patterns
    subs = re.findall(r'^sub\s+(\w+)', content, re.MULTILINE)
    packages = re.findall(r'^package\s+([\w:]+)', content, re.MULTILINE)
    
    stats = [
        f"Modul: {module_name}",
        f"Pfad: {full_path}",
        f"Zeilen: {len(lines)}",
        f"Zeichen: {len(content)}",
        f"Packages: {len(packages)}",
        f"Subroutines: {len(subs)}",
    ]
    
    if subs:
        stats.append(f"\nFunktionen:\n  " + "\n  ".join(subs[:20]))
        if len(subs) > 20:
            stats.append(f"  ... und {len(subs) - 20} weitere")
    
    return "\n".join(stats)
