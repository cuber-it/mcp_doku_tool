"""Tests für tools/reader.py (Eingabe)."""
import pytest
from code.tools import reader


class TestReadModule:
    """Tests für read_module()."""
    
    def test_read_existing_module(self, config):
        """Vorhandenes Modul lesen."""
        result = reader.read_module(config, "Order::Validation")
        assert "package Order::Validation" in result
        assert "sub validate_order" in result
    
    def test_read_nonexistent_module(self, config):
        """Nicht vorhandenes Modul."""
        result = reader.read_module(config, "Does::Not::Exist")
        assert "nicht gefunden" in result.lower()
    
    def test_truncate_large_file(self, config, temp_project):
        """Große Dateien werden gekürzt."""
        # Große Datei erstellen
        large_content = "x" * 20000
        (temp_project / "lib" / "Large.pm").write_text(large_content)
        
        config.max_file_size = 1000
        result = reader.read_module(config, "Large")
        
        assert len(result) < 20000
        assert "gekürzt" in result


class TestFindModules:
    """Tests für find_modules()."""
    
    def test_find_by_pattern(self, config):
        """Module nach Muster finden."""
        result = reader.find_modules(config, "Order")
        assert "Order::Validation" in result
        assert "Order::Base" in result
    
    def test_find_no_match(self, config):
        """Keine Treffer."""
        result = reader.find_modules(config, "XYZ123")
        assert "keine module gefunden" in result.lower()
    
    def test_find_partial_match(self, config):
        """Teilübereinstimmung."""
        result = reader.find_modules(config, "Valid")
        assert "Order::Validation" in result


class TestModuleDependencies:
    """Tests für module_dependencies()."""
    
    def test_find_dependencies(self, config):
        """Abhängigkeiten finden."""
        result = reader.module_dependencies(config, "Order::Validation")
        assert "Order::Base" in result
        assert "Payment::Gateway" in result
    
    def test_no_dependencies(self, config, temp_project):
        """Modul ohne Abhängigkeiten."""
        (temp_project / "lib" / "Empty.pm").write_text("package Empty;\n1;")
        result = reader.module_dependencies(config, "Empty")
        assert "keine abhängigkeiten" in result.lower()


class TestModuleStats:
    """Tests für module_stats()."""
    
    def test_stats_output(self, config):
        """Statistiken ausgeben."""
        result = reader.module_stats(config, "Order::Validation")
        assert "Order::Validation" in result
        assert "Zeilen:" in result
        assert "validate_order" in result
        assert "validate_payment" in result
