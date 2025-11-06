"""Data models for JOURNEL."""

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class Project:
    """Represents a project in JOURNEL."""

    id: str
    name: str
    full_name: str = ""
    status: str = "in-progress"  # in-progress, completed, dormant
    tags: List[str] = field(default_factory=list)
    created: date = field(default_factory=date.today)
    last_active: date = field(default_factory=date.today)
    completion: int = 0  # 0-100
    priority: str = "medium"  # low, medium, high
    github: str = ""
    claude_project: str = ""
    next_steps: str = ""
    blockers: str = ""
    notes: str = ""
    learned: str = ""

    @property
    def file_name(self) -> str:
        """Get the filename for this project."""
        return f"{self.id}.md"

    def to_frontmatter(self) -> dict:
        """Convert project to YAML frontmatter dict."""
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "status": self.status,
            "tags": self.tags,
            "created": self.created.isoformat() if isinstance(self.created, date) else self.created,
            "last_active": self.last_active.isoformat() if isinstance(self.last_active, date) else self.last_active,
            "completion": self.completion,
            "priority": self.priority,
            "github": self.github,
            "claude_project": self.claude_project,
            "next_steps": self.next_steps,
            "blockers": self.blockers,
        }

    @classmethod
    def from_frontmatter(cls, data: dict, notes: str = "") -> "Project":
        """Create project from YAML frontmatter dict."""
        # Convert date strings to date objects
        if isinstance(data.get("created"), str):
            data["created"] = datetime.fromisoformat(data["created"]).date()
        if isinstance(data.get("last_active"), str):
            data["last_active"] = datetime.fromisoformat(data["last_active"]).date()

        project = cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
        project.notes = notes
        return project

    def days_since_active(self) -> int:
        """Get number of days since last activity."""
        if isinstance(self.last_active, str):
            last_active = datetime.fromisoformat(self.last_active).date()
        else:
            last_active = self.last_active
        return (date.today() - last_active).days


@dataclass
class LogEntry:
    """Represents a log entry."""

    date: date
    project: Optional[str]
    message: str
    hours: Optional[float] = None

    def to_markdown(self) -> str:
        """Convert log entry to markdown."""
        if self.project:
            base = f"- **{self.project}**"
            if self.hours:
                base += f" ({self.hours}h)"
            base += f": {self.message}"
            return base
        return f"- {self.message}"
