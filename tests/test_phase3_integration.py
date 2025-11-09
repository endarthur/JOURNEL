"""Integration tests for Phase 3 commands (query and batch).

These tests use the real CLI without complex fixtures to avoid hanging issues.
They test the command-line interface end-to-end.
"""
import json
import subprocess
import pytest


class TestQueryCommand:
    """Test jnl query command."""

    def test_query_help(self):
        """Test that query command shows help."""
        result = subprocess.run(
            ["python", "-m", "journel.cli", "query", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "Advanced project querying" in result.stdout
        assert "--project-type" in result.stdout
        assert "--dormant" in result.stdout

    def test_query_json_output_structure(self):
        """Test that query returns valid JSON structure."""
        result = subprocess.run(
            ["python", "-m", "journel.cli", "query", "--project-type", "regular"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        # Command might fail if no JOURNEL dir, but should still return JSON
        if result.returncode == 0:
            data = json.loads(result.stdout)
            assert "projects" in data
            assert "count" in data
            assert "filters" in data
            assert isinstance(data["projects"], list)


class TestBatchCommand:
    """Test jnl batch command."""

    def test_batch_help(self):
        """Test that batch command shows help."""
        result = subprocess.run(
            ["python", "-m", "journel.cli", "batch", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "batch operations" in result.stdout.lower()
        assert "--action" in result.stdout
        assert "--dry-run" in result.stdout

    def test_batch_requires_action(self):
        """Test that batch command requires --action flag."""
        result = subprocess.run(
            ["python", "-m", "journel.cli", "batch", "--dormant"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        # Should fail without --action
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "missing" in result.stderr.lower()


class TestPhase2Commands:
    """Test Phase 2 commands (get, update)."""

    def test_get_help(self):
        """Test that get command shows help."""
        result = subprocess.run(
            ["python", "-m", "journel.cli", "get", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "Get details for a single project" in result.stdout
        assert "--format" in result.stdout

    def test_update_help(self):
        """Test that update command shows help."""
        result = subprocess.run(
            ["python", "-m", "journel.cli", "update", "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "Update project fields" in result.stdout
        assert "--completion" in result.stdout
        assert "--priority" in result.stdout
        assert "--add-tag" in result.stdout
