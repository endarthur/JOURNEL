"""Pytest configuration and fixtures for JOURNEL tests."""
import tempfile
import shutil
from pathlib import Path
from datetime import date
import pytest
from click.testing import CliRunner

from journel.cli import main
from journel.storage import Storage
from journel.config import Config
from journel.models import Project


@pytest.fixture
def runner():
    """Provide a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_journel_dir(monkeypatch, tmp_path):
    """Create a temporary JOURNEL directory for testing."""
    journel_dir = tmp_path / ".journel"
    journel_dir.mkdir()

    # Set environment to use temp directory
    monkeypatch.setenv("JOURNEL_DIR", str(journel_dir))

    return journel_dir


@pytest.fixture
def storage(temp_journel_dir):
    """Provide a Storage instance with temp directory."""
    config = Config(journel_dir=temp_journel_dir)
    storage = Storage(config)
    storage.init_structure(init_git=False)  # Skip git init during tests
    return storage


@pytest.fixture
def sample_project(storage):
    """Create a sample project for testing."""
    project = Project(
        id="test-project",
        name="Test Project",
        full_name="A test project for unit tests",
        tags=["test", "sample"],
        created=date.today(),
        last_active=date.today(),
        completion=25,
        priority="medium",
        project_type="regular",
        next_steps="Implement feature X",
        blockers="Waiting on API",
    )
    storage.save_project(project)
    return project


@pytest.fixture
def multiple_projects(storage):
    """Create multiple projects with different states."""
    projects = [
        Project(
            id="active-regular",
            name="Active Regular",
            status="in-progress",
            project_type="regular",
            completion=50,
            priority="high",
            tags=["urgent"],
            created=date.today(),
            last_active=date.today(),
        ),
        Project(
            id="active-ongoing",
            name="Active Ongoing",
            status="in-progress",
            project_type="ongoing",
            completion=30,
            priority="medium",
            tags=["long-term"],
            created=date.today(),
            last_active=date.today(),
        ),
        Project(
            id="completed-project",
            name="Completed Project",
            status="completed",
            project_type="regular",
            completion=100,
            priority="low",
            created=date.today(),
            last_active=date.today(),
        ),
        Project(
            id="maintenance-project",
            name="Maintenance Project",
            status="in-progress",
            project_type="maintenance",
            completion=0,
            priority="low",
            tags=["infra"],
            created=date.today(),
            last_active=date.today(),
        ),
    ]

    for project in projects:
        storage.save_project(project)

    return projects
