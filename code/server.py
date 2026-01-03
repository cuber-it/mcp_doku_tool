"""MCP Server für Code-Dokumentation.

Exponiert die Tools als MCP-Werkzeuge für Claude.
"""
from mcp.server.fastmcp import FastMCP

from config import Config
import tools


def create_server(config: Config) -> FastMCP:
    """Erstellt und konfiguriert den MCP-Server.
    
    Args:
        config: Konfiguration
        
    Returns:
        Konfigurierter FastMCP-Server
    """
    mcp = FastMCP(config.server_name)
    
    # === Code lesen (Eingabe) ===
    
    @mcp.tool()
    def read_module(module_name: str) -> str:
        """Liest ein Modul und gibt den Inhalt zurück.
        
        Args:
            module_name: Modulname (z.B. 'Order::Validation')
        """
        return tools.read_module(config, module_name)
    
    @mcp.tool()
    def find_modules(pattern: str) -> str:
        """Findet Module die einem Muster entsprechen.
        
        Args:
            pattern: Suchmuster (Teil des Modulnamens)
        """
        return tools.find_modules(config, pattern)
    
    @mcp.tool()
    def module_dependencies(module_name: str) -> str:
        """Zeigt welche Module ein Modul verwendet (use/require).
        
        Args:
            module_name: Modulname
        """
        return tools.module_dependencies(config, module_name)
    
    @mcp.tool()
    def module_stats(module_name: str) -> str:
        """Gibt Statistiken über ein Modul aus (Zeilen, Funktionen, etc.).
        
        Args:
            module_name: Modulname
        """
        return tools.module_stats(config, module_name)
    
    # === Änderungs-Tracking (Verarbeitung) ===
    
    @mcp.tool()
    def check_changes(module_name: str) -> str:
        """Prüft ob sich ein Modul seit der letzten Dokumentation geändert hat.
        
        Args:
            module_name: Modulname
        """
        return tools.check_changes(config, module_name)
    
    @mcp.tool()
    def check_all_changes() -> str:
        """Prüft alle dokumentierten Module auf Änderungen."""
        return tools.check_all_changes(config)
    
    @mcp.tool()
    def mark_documented(module_name: str) -> str:
        """Markiert ein Modul als dokumentiert (speichert Hash).
        
        Args:
            module_name: Modulname
        """
        return tools.mark_documented(config, module_name)
    
    @mcp.tool()
    def unmark_documented(module_name: str) -> str:
        """Entfernt die Dokumentations-Markierung für ein Modul.
        
        Args:
            module_name: Modulname
        """
        return tools.unmark_documented(config, module_name)
    
    @mcp.tool()
    def list_documented() -> str:
        """Listet alle als dokumentiert markierten Module."""
        return tools.list_documented(config)
    
    @mcp.tool()
    def documentation_stats() -> str:
        """Gibt Statistiken über die Dokumentation aus."""
        return tools.documentation_stats(config)
    
    # === Dokumentation (Ausgabe) ===
    
    @mcp.tool()
    def write_doc(doc_type: str, name: str, content: str) -> str:
        """Schreibt eine Dokumentations-Datei.

        Args:
            doc_type: 'module', 'table', 'flow' oder 'note'
            name: Name der Datei (ohne .md)
            content: Markdown-Inhalt
        """
        return tools.write_doc(config, doc_type, name, content)
    
    @mcp.tool()
    def read_doc(doc_type: str, name: str) -> str:
        """Liest eine existierende Dokumentations-Datei.
        
        Args:
            doc_type: 'module', 'table', 'flow' oder 'note'
            name: Name der Datei (ohne .md)
        """
        return tools.read_doc(config, doc_type, name)
    
    @mcp.tool()
    def list_docs(doc_type: str = "") -> str:
        """Listet vorhandene Dokumentation auf.
        
        Args:
            doc_type: Optional - 'module', 'table', 'flow' oder 'note'. Leer = alle.
        """
        return tools.list_docs(config, doc_type)
    
    @mcp.tool()
    def delete_doc(doc_type: str, name: str) -> str:
        """Löscht eine Dokumentations-Datei.
        
        Args:
            doc_type: 'module', 'table', 'flow' oder 'note'
            name: Name der Datei (ohne .md)
        """
        return tools.delete_doc(config, doc_type, name)
    
    return mcp


def run_server(config: Config) -> None:
    """Startet den MCP-Server.
    
    Args:
        config: Konfiguration
    """
    mcp = create_server(config)
    
    if config.transport == "http":
        mcp.run(transport="http", port=config.http_port)
    else:
        mcp.run()
