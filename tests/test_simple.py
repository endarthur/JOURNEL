"""Simple smoke tests to verify basic functionality."""
import json


def test_import():
    """Test that we can import the module."""
    from journel import cli
    assert cli is not None


def test_cli_main_exists():
    """Test that main command exists."""
    from journel.cli import main
    assert main is not None


def test_models():
    """Test that models work."""
    from journel.models import Project
    from datetime import date

    p = Project(
        id="test",
        name="Test",
        created=date.today(),
        last_active=date.today(),
    )
    assert p.id == "test"
    assert p.name == "Test"
    assert p.completion == 0
    assert p.days_since_active() == 0
