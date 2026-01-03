"""Tests für tools/tracker.py (Verarbeitung)."""
import pytest
from code.tools import tracker


class TestCheckChanges:
    """Tests für check_changes()."""
    
    def test_never_documented(self, config):
        """Modul wurde noch nie dokumentiert."""
        result = tracker.check_changes(config, "Order::Validation")
        assert "noch nie dokumentiert" in result.lower()
    
    def test_unchanged(self, config):
        """Modul unverändert seit Dokumentation."""
        tracker.mark_documented(config, "Order::Validation")
        result = tracker.check_changes(config, "Order::Validation")
        assert "unverändert" in result.lower()
    
    def test_changed(self, config, temp_project):
        """Modul wurde geändert."""
        tracker.mark_documented(config, "Order::Validation")
        
        # Datei ändern
        path = temp_project / "lib" / "Order" / "Validation.pm"
        path.write_text(path.read_text() + "\n# Modified")
        
        result = tracker.check_changes(config, "Order::Validation")
        assert "geändert" in result.lower()
    
    def test_nonexistent_module(self, config):
        """Nicht existierendes Modul."""
        result = tracker.check_changes(config, "Does::Not::Exist")
        assert "nicht gefunden" in result.lower()


class TestMarkDocumented:
    """Tests für mark_documented()."""
    
    def test_mark_new(self, config):
        """Neues Modul markieren."""
        result = tracker.mark_documented(config, "Order::Validation")
        assert "dokumentiert markiert" in result.lower()
        assert config.hash_file.exists()
    
    def test_mark_updates_hash(self, config, temp_project):
        """Hash wird aktualisiert."""
        tracker.mark_documented(config, "Order::Validation")
        
        # Datei ändern
        path = temp_project / "lib" / "Order" / "Validation.pm"
        path.write_text(path.read_text() + "\n# Modified")
        
        # Neu markieren
        tracker.mark_documented(config, "Order::Validation")
        
        # Sollte jetzt unverändert sein
        result = tracker.check_changes(config, "Order::Validation")
        assert "unverändert" in result.lower()


class TestUnmarkDocumented:
    """Tests für unmark_documented()."""
    
    def test_unmark_existing(self, config):
        """Markierung entfernen."""
        tracker.mark_documented(config, "Order::Validation")
        result = tracker.unmark_documented(config, "Order::Validation")
        assert "entfernt" in result.lower()
        
        # Sollte jetzt "nie dokumentiert" sein
        result = tracker.check_changes(config, "Order::Validation")
        assert "noch nie dokumentiert" in result.lower()
    
    def test_unmark_nonexistent(self, config):
        """Nicht markiertes Modul."""
        result = tracker.unmark_documented(config, "Order::Validation")
        assert "nicht als dokumentiert" in result.lower()


class TestCheckAllChanges:
    """Tests für check_all_changes()."""
    
    def test_no_documented(self, config):
        """Keine dokumentierten Module."""
        result = tracker.check_all_changes(config)
        assert "keine module" in result.lower()
    
    def test_all_unchanged(self, config):
        """Alle Module unverändert."""
        tracker.mark_documented(config, "Order::Validation")
        tracker.mark_documented(config, "Order::Base")
        
        result = tracker.check_all_changes(config)
        assert "unverändert: 2" in result.lower()
    
    def test_mixed_status(self, config, temp_project):
        """Gemischter Status."""
        tracker.mark_documented(config, "Order::Validation")
        tracker.mark_documented(config, "Order::Base")
        
        # Ein Modul ändern
        path = temp_project / "lib" / "Order" / "Validation.pm"
        path.write_text(path.read_text() + "\n# Modified")
        
        result = tracker.check_all_changes(config)
        assert "geändert" in result.lower()
        assert "Order::Validation" in result


class TestListDocumented:
    """Tests für list_documented()."""
    
    def test_empty(self, config):
        """Keine dokumentierten Module."""
        result = tracker.list_documented(config)
        assert "keine module" in result.lower()
    
    def test_list_modules(self, config):
        """Dokumentierte Module auflisten."""
        tracker.mark_documented(config, "Order::Validation")
        tracker.mark_documented(config, "Payment::Gateway")
        
        result = tracker.list_documented(config)
        assert "Order::Validation" in result
        assert "Payment::Gateway" in result


class TestDocumentationStats:
    """Tests für documentation_stats()."""
    
    def test_stats_output(self, config):
        """Statistiken ausgeben."""
        from code.tools import writer
        
        tracker.mark_documented(config, "Order::Validation")
        writer.write_doc(config, "module", "Test", "content")
        
        result = tracker.documentation_stats(config)
        assert "Verfolgte Module: 1" in result
        assert "modules: 1" in result.lower()
