"""Tests for Phase 1 and Phase 2 AI-friendly interface features."""
import json
import pytest
from journel.cli import main


class TestPhase1NonInteractive:
    """Test Phase 1 --yes flags for non-interactive mode."""

    def test_new_with_yes_flag(self, runner, temp_journel_dir):
        """Test creating project with --yes skips prompts."""
        result = runner.invoke(
            main,
            ["new", "TestProject", "A test project", "--yes"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0
        assert "Created project: TestProject" in result.output

    def test_archive_with_yes_flag(self, runner, temp_journel_dir, sample_project):
        """Test archiving with --yes skips confirmation."""
        result = runner.invoke(
            main,
            ["archive", "test-project", "--yes"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0
        assert "Archived" in result.output

    def test_done_with_yes_flag(self, runner, temp_journel_dir, sample_project):
        """Test completing project with --yes skips prompts."""
        result = runner.invoke(
            main,
            ["done", "test-project", "--yes", "--skip-celebration"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0
        assert "marked as complete" in result.output


class TestPhase1JSONOutput:
    """Test Phase 1 --format json for machine-readable output."""

    def test_status_json_output(self, runner, temp_journel_dir, sample_project):
        """Test status command with JSON output."""
        result = runner.invoke(
            main,
            ["status", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert "projects" in data
        assert "count" in data
        assert isinstance(data["projects"], list)
        assert len(data["projects"]) > 0

        # Check project structure
        project = data["projects"][0]
        assert "id" in project
        assert "name" in project
        assert "completion" in project
        assert "status" in project

    def test_list_json_output(self, runner, temp_journel_dir, multiple_projects):
        """Test list command with JSON output and filters."""
        result = runner.invoke(
            main,
            ["list", "--active", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert "projects" in data
        assert "count" in data
        assert "filter" in data
        assert data["filter"] == "Active Projects"


class TestPhase2Commands:
    """Test Phase 2 new commands (ctx, get, update)."""

    def test_ctx_json_output(self, runner, temp_journel_dir, sample_project):
        """Test ctx command with JSON output."""
        result = runner.invoke(
            main,
            ["ctx", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert "active_projects" in data
        assert "recent_logs" in data
        assert isinstance(data["active_projects"], list)

    def test_get_command_json(self, runner, temp_journel_dir, sample_project):
        """Test get command returns single project as JSON."""
        result = runner.invoke(
            main,
            ["get", "test-project", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert data["id"] == "test-project"
        assert data["name"] == "Test Project"
        assert data["completion"] == 25
        assert data["priority"] == "medium"
        assert "notes" in data
        assert "learned" in data

    def test_get_command_not_found(self, runner, temp_journel_dir):
        """Test get command with non-existent project."""
        result = runner.invoke(
            main,
            ["get", "nonexistent", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        # Command succeeds but returns error in JSON
        data = json.loads(result.output)
        assert "error" in data

    def test_update_command_completion(self, runner, temp_journel_dir, sample_project):
        """Test update command changes completion."""
        result = runner.invoke(
            main,
            ["update", "test-project", "--completion", "75", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert data["success"] is True
        assert "completion: 75%" in data["changes"]
        assert data["updated_fields"]["completion"] == 75

    def test_update_command_priority(self, runner, temp_journel_dir, sample_project):
        """Test update command changes priority."""
        result = runner.invoke(
            main,
            ["update", "test-project", "--priority", "high", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0

        data = json.loads(result.output)
        assert data["success"] is True
        assert data["updated_fields"]["priority"] == "high"

    def test_update_command_tags(self, runner, temp_journel_dir, sample_project):
        """Test update command manages tags."""
        # Add tag
        result = runner.invoke(
            main,
            ["update", "test-project", "--add-tag", "urgent", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "urgent" in data["updated_fields"]["tags"]

        # Remove tag
        result = runner.invoke(
            main,
            ["update", "test-project", "--remove-tag", "test", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "test" not in data["updated_fields"]["tags"]

    def test_update_command_no_fields(self, runner, temp_journel_dir, sample_project):
        """Test update command with no fields returns error."""
        result = runner.invoke(
            main,
            ["update", "test-project", "--format", "json"],
            env={"JOURNEL_DIR": str(temp_journel_dir)},
        )

        data = json.loads(result.output)
        assert data["success"] is False
        assert "error" in data
