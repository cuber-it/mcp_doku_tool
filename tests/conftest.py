"""Pytest Konfiguration für MCP Doku Tool Tests."""
import pytest
import tempfile
import shutil
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from code.config import Config


@pytest.fixture
def temp_project(tmp_path):
    """Erstellt ein temporäres Projekt mit Test-Modulen."""
    lib_dir = tmp_path / "lib"
    lib_dir.mkdir()
    
    # Test-Module erstellen
    (lib_dir / "Order").mkdir()
    (lib_dir / "Order" / "Validation.pm").write_text("""\
package Order::Validation;
use strict;
use warnings;
use Order::Base;
use Payment::Gateway;

sub validate_order {
    my ($order) = @_;
    return 1;
}

sub validate_payment {
    my ($payment_data) = @_;
    return 1;
}

1;
""")
    
    (lib_dir / "Order" / "Base.pm").write_text("""\
package Order::Base;
use strict;
use warnings;

sub new {
    my ($class) = @_;
    return bless {}, $class;
}

1;
""")
    
    (lib_dir / "Payment").mkdir()
    (lib_dir / "Payment" / "Gateway.pm").write_text("""\
package Payment::Gateway;
use strict;
use warnings;

sub process {
    my ($self, $amount) = @_;
    return 1;
}

1;
""")
    
    return tmp_path


@pytest.fixture
def temp_docs(tmp_path):
    """Erstellt ein temporäres Dokumentationsverzeichnis."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    return docs_dir


@pytest.fixture
def config(temp_project, temp_docs):
    """Erstellt eine Test-Konfiguration."""
    return Config(
        project_root=temp_project,
        docs_root=temp_docs,
        lib_subdir="lib",
        file_extension=".pm",
        module_separator="::",
    )
