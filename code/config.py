"""Konfigurationsmanagement für MCP Doku Tool.

Lädt Konfiguration aus:
1. Default-Werte
2. Config-Datei (YAML)
3. Kommandozeilen-Argumente (überschreiben alles)
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import yaml


@dataclass
class Config:
    """Zentrale Konfiguration."""
    
    # Projekt-Einstellungen
    project_root: Path = field(default_factory=lambda: Path("/path/to/project"))
    lib_subdir: str = "lib"
    file_extension: str = ".pm"
    module_separator: str = "::"
    
    # Dokumentations-Einstellungen
    docs_root: Path = field(default_factory=lambda: Path.home() / "Documents" / "project-docs")
    doc_types: list[str] = field(default_factory=lambda: ["module", "table", "flow", "note"])
    
    # Server-Einstellungen
    server_name: str = "doku-tool"
    transport: str = "stdio"
    http_port: int = 8080
    
    # Limits
    max_file_size: int = 15000
    max_results: int = 30
    
    @property
    def lib_path(self) -> Path:
        """Vollständiger Pfad zum lib-Verzeichnis."""
        return self.project_root / self.lib_subdir
    
    @property
    def hash_file(self) -> Path:
        """Pfad zur Hash-Datei."""
        return self.docs_root / ".module_hashes.json"
    
    def module_to_path(self, module_name: str) -> Path:
        """Konvertiert Modulname zu Dateipfad."""
        path = module_name.replace(self.module_separator, "/") + self.file_extension
        return self.lib_path / path
    
    def path_to_module(self, path: Path) -> str:
        """Konvertiert Dateipfad zu Modulname."""
        rel = path.relative_to(self.lib_path)
        return str(rel.with_suffix("")).replace("/", self.module_separator)


def load_config(config_file: Optional[Path] = None) -> Config:
    """Lädt Konfiguration aus Datei."""
    config = Config()
    
    if config_file and config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        
        # Projekt
        if "project" in data:
            proj = data["project"]
            if "root" in proj:
                config.project_root = Path(proj["root"]).expanduser()
            if "lib_subdir" in proj:
                config.lib_subdir = proj["lib_subdir"]
            if "file_extension" in proj:
                config.file_extension = proj["file_extension"]
            if "module_separator" in proj:
                config.module_separator = proj["module_separator"]
        
        # Dokumentation
        if "docs" in data:
            docs = data["docs"]
            if "root" in docs:
                config.docs_root = Path(docs["root"]).expanduser()
            if "types" in docs:
                config.doc_types = docs["types"]
        
        # Server
        if "server" in data:
            srv = data["server"]
            if "name" in srv:
                config.server_name = srv["name"]
            if "transport" in srv:
                config.transport = srv["transport"]
            if "http_port" in srv:
                config.http_port = srv["http_port"]
        
        # Limits
        if "limits" in data:
            lim = data["limits"]
            if "max_file_size" in lim:
                config.max_file_size = lim["max_file_size"]
            if "max_results" in lim:
                config.max_results = lim["max_results"]
    
    return config


def apply_cli_overrides(config: Config, **kwargs) -> Config:
    """Wendet CLI-Argumente auf Config an."""
    if kwargs.get("project_root"):
        config.project_root = Path(kwargs["project_root"]).expanduser()
    if kwargs.get("docs_root"):
        config.docs_root = Path(kwargs["docs_root"]).expanduser()
    if kwargs.get("http_port"):
        config.http_port = kwargs["http_port"]
    if kwargs.get("transport"):
        config.transport = kwargs["transport"]
    return config
