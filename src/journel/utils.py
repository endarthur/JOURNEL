"""Utility functions for JOURNEL."""

import re
from datetime import date
from pathlib import Path
from typing import Optional


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    import yaml

    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
        body = parts[2].strip()
        return frontmatter, body
    except yaml.YAMLError:
        return {}, content


def format_frontmatter(data: dict, body: str) -> str:
    """Format frontmatter and body into markdown content."""
    import yaml

    frontmatter = yaml.dump(data, default_flow_style=False, sort_keys=False)
    return f"---\n{frontmatter}---\n\n{body}"


def get_month_file(target_date: Optional[date] = None) -> str:
    """Get the log filename for a given date."""
    if target_date is None:
        target_date = date.today()
    return f"{target_date.year}-{target_date.month:02d}.md"


def format_date_relative(target_date: date) -> str:
    """Format a date as a relative string."""
    delta = (date.today() - target_date).days

    if delta == 0:
        return "today"
    elif delta == 1:
        return "yesterday"
    elif delta < 7:
        return f"{delta} days ago"
    elif delta < 14:
        return "1 week ago"
    elif delta < 30:
        weeks = delta // 7
        return f"{weeks} weeks ago"
    elif delta < 60:
        return "1 month ago"
    else:
        months = delta // 30
        return f"{months} months ago"


def ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
