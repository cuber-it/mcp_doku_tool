"""Tests für config.py."""
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from code.config import Config, load_config, apply_cli_overrides


class TestConfig:
    """Tests für Config Dataclass."""
    
    def test_default_values(self):
        """Standard-Werte."""
        config = Config()
        assert config.lib_subdir == "lib"
        assert config.file_extension == ".pm"
        assert config.module_separator == "::"
    
    def test_lib_path(self, tmp_path):
        """lib_path Property."""
        config = Config(project_root=tmp_path, lib_subdir="src")
        assert config.lib_path == tmp_path / "src"
    
    def test_hash_file(self, tmp_path):
        """hash_file Property."""
        config = Config(docs_root=tmp_path)
        assert config.hash_file == tmp_path / ".module_hashes.json"
    
    def test_module_to_path(self, tmp_path):
        """Modulname zu Pfad konvertieren."""
        config = Config(project_root=tmp_path)
        path = config.module_to_path("Order::Validation")
        assert path == tmp_path / "lib" / "Order" / "Validation.pm"
    
    def test_path_to_module(self, tmp_path):
        """Pfad zu Modulname konvertieren."""
        config = Config(project_root=tmp_path)
        lib = tmp_path / "lib"
        lib.mkdir()
        path = lib / "Order" / "Validation.pm"
        
        module = config.path_to_module(path)
        assert module == "Order::Validation"


class TestLoadConfig:
    """Tests für load_config()."""
    
    def test_load_default(self):
        """Ohne Config-Datei."""
        config = load_config(None)
        assert isinstance(config, Config)
    
    def test_load_from_file(self, tmp_path):
        """Config aus Datei laden."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""\
project:
  root: /test/project
  lib_subdir: src
  
docs:
  root: ~/test-docs

server:
  http_port: 9999
""")
        
        config = load_config(config_file)
        assert str(config.project_root) == "/test/project"
        assert config.lib_subdir == "src"
        assert config.http_port == 9999
    
    def test_load_nonexistent_file(self, tmp_path):
        """Nicht existierende Datei."""
        config = load_config(tmp_path / "nonexistent.yaml")
        # Sollte Default-Config zurückgeben
        assert isinstance(config, Config)


class TestApplyCliOverrides:
    """Tests für apply_cli_overrides()."""
    
    def test_override_project_root(self, tmp_path):
        """project_root überschreiben."""
        config = Config()
        config = apply_cli_overrides(config, project_root=str(tmp_path))
        assert config.project_root == tmp_path
    
    def test_override_docs_root(self, tmp_path):
        """docs_root überschreiben."""
        config = Config()
        config = apply_cli_overrides(config, docs_root=str(tmp_path))
        assert config.docs_root == tmp_path
    
    def test_no_overrides(self):
        """Keine Überschreibungen."""
        original = Config()
        config = apply_cli_overrides(original)
        assert config.project_root == original.project_root
