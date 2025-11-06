"""Storage and file I/O operations for JOURNEL."""

import json
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

import git

from .config import Config
from .models import LogEntry, Project
from .utils import ensure_dir, format_frontmatter, get_month_file, parse_frontmatter


class Storage:
    """Handles all file I/O and git operations for JOURNEL."""

    def __init__(self, config: Config):
        """Initialize storage handler."""
        self.config = config
        self.repo: Optional[git.Repo] = None

    def init_structure(self) -> None:
        """Initialize the ~/.journel/ directory structure."""
        # Create directories
        ensure_dir(self.config.projects_dir)
        ensure_dir(self.config.logs_dir)
        ensure_dir(self.config.completed_dir)
        ensure_dir(self.config.meta_dir)

        # Create README
        readme_path = self.config.journel_dir / "README.md"
        if not readme_path.exists():
            readme_content = """# JOURNEL Data Directory

This directory contains all your JOURNEL project tracking data.

## Structure

- `projects/` - Active project files (one .md file per project)
- `completed/` - Completed project files
- `logs/` - Monthly activity logs
- `.meta/` - Machine-readable indexes (auto-generated)
- `config.yaml` - Your configuration settings

## Format

All files are plain markdown with YAML frontmatter. You can edit them directly
or use the `jnl` command-line tool.

## Sync

This directory is a git repository. Use `git push`/`pull` to sync across machines,
or use `jnl sync` for convenience.

## LLM Integration

These files are designed to be readable by AI assistants. Use `jnl ctx` to
generate context summaries for Claude or other LLMs.
"""
            readme_path.write_text(readme_content, encoding="utf-8")

        # Initialize git repository
        if not (self.config.journel_dir / ".git").exists():
            self.repo = git.Repo.init(self.config.journel_dir)
            # Create initial commit
            self.repo.index.add(["."])
            self.repo.index.commit("Initialize JOURNEL")
        else:
            self.repo = git.Repo(self.config.journel_dir)

        # Save default config
        self.config.save()

    def load_project(self, project_id: str) -> Optional[Project]:
        """Load a project by ID."""
        # Check active projects
        project_file = self.config.projects_dir / f"{project_id}.md"
        if project_file.exists():
            return self._load_project_file(project_file)

        # Check completed projects
        project_file = self.config.completed_dir / f"{project_id}.md"
        if project_file.exists():
            return self._load_project_file(project_file)

        return None

    def _load_project_file(self, path: Path) -> Project:
        """Load project from file."""
        content = path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(content)
        return Project.from_frontmatter(frontmatter, notes=body)

    def save_project(self, project: Project) -> None:
        """Save a project to disk."""
        # Determine directory based on status
        if project.status == "completed":
            project_dir = self.config.completed_dir
        else:
            project_dir = self.config.projects_dir

        project_file = project_dir / project.file_name

        # Create project body
        if project.notes:
            # Use existing notes (already has header)
            body = project.notes
        else:
            # Create default template
            body = f"# {project.full_name or project.name}\n\n"
            body += "## Overview\n\n## Recent Activity\n\n## What I Learned\n\n## Notes\n"

        # Write file
        content = format_frontmatter(project.to_frontmatter(), body)
        ensure_dir(project_dir)
        project_file.write_text(content, encoding="utf-8")

        # Auto-commit if enabled
        if self.config.get("auto_git_commit"):
            self._git_commit(f"Update project: {project.name}")

    def list_projects(self, status: Optional[str] = None) -> List[Project]:
        """List all projects, optionally filtered by status."""
        projects = []

        # Load active/dormant projects
        if status is None or status in ["in-progress", "dormant"]:
            for project_file in self.config.projects_dir.glob("*.md"):
                project = self._load_project_file(project_file)
                if status is None or project.status == status:
                    projects.append(project)

        # Load completed projects
        if status is None or status == "completed":
            for project_file in self.config.completed_dir.glob("*.md"):
                project = self._load_project_file(project_file)
                projects.append(project)

        return projects

    def add_log_entry(self, entry: LogEntry) -> None:
        """Add a log entry to the monthly log file."""
        log_file = self.config.logs_dir / get_month_file(entry.date)
        ensure_dir(self.config.logs_dir)

        # Load existing content
        if log_file.exists():
            content = log_file.read_text(encoding="utf-8")
        else:
            month_name = entry.date.strftime("%B %Y")
            content = f"# {month_name} Activity Log\n\n"

        # Find or create date section
        date_str = entry.date.isoformat()
        date_header = f"## {date_str}"

        if date_header in content:
            # Append to existing date section
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith(date_header):
                    # Insert after the header
                    lines.insert(i + 1, entry.to_markdown())
                    break
            content = "\n".join(lines)
        else:
            # Add new date section at the top (after title)
            lines = content.split("\n")
            # Find first line after title
            insert_pos = 2 if len(lines) > 2 else len(lines)
            lines.insert(insert_pos, f"\n{date_header}")
            lines.insert(insert_pos + 1, entry.to_markdown())
            content = "\n".join(lines)

        log_file.write_text(content, encoding="utf-8")

        # Auto-commit if enabled
        if self.config.get("auto_git_commit"):
            self._git_commit(f"Add log entry: {date_str}")

    def get_recent_logs(self, days: int = 7) -> str:
        """Get recent log entries as markdown."""
        logs = []
        current_date = date.today()

        # Check last 2 months of log files
        for month_offset in range(2):
            target_date = date(current_date.year, current_date.month, 1)
            if month_offset > 0:
                # Go back a month
                if target_date.month == 1:
                    target_date = date(target_date.year - 1, 12, 1)
                else:
                    target_date = date(target_date.year, target_date.month - 1, 1)

            log_file = self.config.logs_dir / get_month_file(target_date)
            if log_file.exists():
                logs.append(log_file.read_text(encoding="utf-8"))

        return "\n\n".join(logs) if logs else "No recent activity logged."

    def move_to_completed(self, project: Project) -> None:
        """Move a project to the completed directory."""
        old_path = self.config.projects_dir / project.file_name
        new_path = self.config.completed_dir / project.file_name

        if old_path.exists():
            project.status = "completed"
            self.save_project(project)
            old_path.unlink()  # Remove from active projects

            if self.config.get("auto_git_commit"):
                self._git_commit(f"Complete project: {project.name}")

    def _git_commit(self, message: str) -> None:
        """Create a git commit."""
        if self.repo is None:
            return

        try:
            self.repo.index.add(["."])
            if self.repo.index.diff("HEAD"):  # Only commit if there are changes
                self.repo.index.commit(message)
        except Exception:
            # Silently fail git operations
            pass

    def update_project_index(self) -> None:
        """Update the machine-readable project index."""
        projects = self.list_projects()
        index = {
            "updated": datetime.now().isoformat(),
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "status": p.status,
                    "completion": p.completion,
                    "last_active": p.last_active.isoformat() if isinstance(p.last_active, date) else p.last_active,
                    "tags": p.tags,
                }
                for p in projects
            ],
        }

        index_file = self.config.meta_dir / "projects.json"
        ensure_dir(self.config.meta_dir)
        index_file.write_text(json.dumps(index, indent=2), encoding="utf-8")
