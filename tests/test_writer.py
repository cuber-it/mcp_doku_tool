"""Tests für tools/writer.py (Ausgabe)."""
import pytest
from code.tools import writer


class TestWriteDoc:
    """Tests für write_doc()."""
    
    def test_write_module_doc(self, config):
        """Modul-Dokumentation schreiben."""
        result = writer.write_doc(config, "module", "Order_Validation", "# Test\n\nContent")
        assert "Geschrieben" in result
        
        # Datei existiert?
        filepath = config.docs_root / "modules" / "Order_Validation.md"
        assert filepath.exists()
        assert filepath.read_text() == "# Test\n\nContent"
    
    def test_write_creates_folder(self, config):
        """Ordner wird erstellt."""
        result = writer.write_doc(config, "flow", "checkout", "# Checkout Flow")
        assert "Geschrieben" in result
        assert (config.docs_root / "flows" / "checkout.md").exists()
    
    def test_invalid_doc_type(self, config):
        """Ungültiger Dokumentationstyp."""
        result = writer.write_doc(config, "invalid", "test", "content")
        assert "ungültiger typ" in result.lower()
    
    def test_sanitize_filename(self, config):
        """Dateiname wird bereinigt."""
        result = writer.write_doc(config, "module", "Order::Validation", "content")
        assert (config.docs_root / "modules" / "Order_Validation.md").exists()


class TestReadDoc:
    """Tests für read_doc()."""
    
    def test_read_existing_doc(self, config):
        """Vorhandene Dokumentation lesen."""
        # Erst schreiben
        writer.write_doc(config, "module", "Test", "# Test Content")
        
        # Dann lesen
        result = writer.read_doc(config, "module", "Test")
        assert "# Test Content" in result
    
    def test_read_nonexistent_doc(self, config):
        """Nicht vorhandene Dokumentation."""
        result = writer.read_doc(config, "module", "DoesNotExist")
        assert "nicht gefunden" in result.lower()


class TestListDocs:
    """Tests für list_docs()."""
    
    def test_list_empty(self, config):
        """Leere Dokumentation."""
        result = writer.list_docs(config)
        assert "keine" in result.lower() or "existiert noch nicht" in result.lower()
    
    def test_list_by_type(self, config):
        """Nach Typ filtern."""
        writer.write_doc(config, "module", "Test1", "content")
        writer.write_doc(config, "table", "Test2", "content")
        
        result = writer.list_docs(config, "module")
        assert "Test1" in result
        assert "Test2" not in result
    
    def test_list_all(self, config):
        """Alle Typen listen."""
        writer.write_doc(config, "module", "Mod1", "content")
        writer.write_doc(config, "table", "Tab1", "content")
        
        result = writer.list_docs(config)
        assert "MODULE" in result or "Mod1" in result


class TestDeleteDoc:
    """Tests für delete_doc()."""
    
    def test_delete_existing(self, config):
        """Vorhandene Dokumentation löschen."""
        writer.write_doc(config, "module", "ToDelete", "content")
        assert (config.docs_root / "modules" / "ToDelete.md").exists()
        
        result = writer.delete_doc(config, "module", "ToDelete")
        assert "Gelöscht" in result
        assert not (config.docs_root / "modules" / "ToDelete.md").exists()
    
    def test_delete_nonexistent(self, config):
        """Nicht vorhandene Dokumentation löschen."""
        result = writer.delete_doc(config, "module", "DoesNotExist")
        assert "nicht gefunden" in result.lower()
