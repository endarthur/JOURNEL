"""GitHub API client using gh CLI."""

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class GitHubRepo:
    """Represents a GitHub repository."""

    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    stargazers_count: int
    pushed_at: datetime
    language: Optional[str]
    topics: List[str]
    fork: bool
    archived: bool
    size: int
    open_issues_count: int

    @classmethod
    def from_dict(cls, data: dict) -> "GitHubRepo":
        """Create GitHubRepo from gh CLI JSON output."""
        # Handle topics - might be already flattened or need flattening
        topics = data.get("repositoryTopics", [])
        if isinstance(topics, list) and not isinstance(topics, dict):
            # Already flattened
            pass
        else:
            # Need to flatten
            topics = [t["topic"]["name"] for t in topics.get("nodes", [])] if topics else []

        return cls(
            name=data.get("name", ""),
            full_name=data.get("nameWithOwner", ""),
            description=data.get("description"),
            html_url=data.get("url", ""),
            stargazers_count=data.get("stargazerCount", 0),
            pushed_at=datetime.fromisoformat(data.get("pushedAt", "").replace("Z", "+00:00")),
            language=data.get("primaryLanguage", {}).get("name") if data.get("primaryLanguage") else None,
            topics=topics,
            fork=data.get("isFork", False),
            archived=data.get("isArchived", False),
            size=data.get("diskUsage", 0),
            open_issues_count=data.get("openIssues", {}).get("totalCount", 0),
        )


class GitHubClient:
    """Client for interacting with GitHub via gh CLI."""

    def __init__(self):
        """Initialize GitHub client."""
        self._check_gh_installed()

    def _check_gh_installed(self) -> bool:
        """Check if gh CLI is installed and authenticated."""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            raise RuntimeError(
                "GitHub CLI (gh) not found or not authenticated.\n"
                "Install: https://cli.github.com/\n"
                "Authenticate: gh auth login"
            )

    def fetch_user_repos(self, limit: int = 100) -> List[GitHubRepo]:
        """Fetch all repositories for the authenticated user.

        Args:
            limit: Maximum number of repos to fetch (default: 1000)

        Returns:
            List of GitHubRepo objects
        """
        # Build GraphQL query for detailed repo info
        query = """
        query($limit: Int!) {
          viewer {
            repositories(first: $limit, orderBy: {field: PUSHED_AT, direction: DESC}) {
              nodes {
                name
                nameWithOwner
                description
                url
                stargazerCount
                pushedAt
                primaryLanguage {
                  name
                }
                repositoryTopics(first: 10) {
                  nodes {
                    topic {
                      name
                    }
                  }
                }
                isFork
                isArchived
                diskUsage
                openIssues: issues(states: OPEN) {
                  totalCount
                }
              }
            }
          }
        }
        """

        try:
            result = subprocess.run(
                ["gh", "api", "graphql", "-f", f"query={query}", "-F", f"limit={limit}"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                raise RuntimeError(f"Failed to fetch repos: {result.stderr}")

            data = json.loads(result.stdout)
            repo_nodes = data.get("data", {}).get("viewer", {}).get("repositories", {}).get("nodes", [])

            repos = []
            for node in repo_nodes:
                # Flatten topics
                topics = [t["topic"]["name"] for t in node.get("repositoryTopics", {}).get("nodes", [])]
                node["repositoryTopics"] = topics

                repos.append(GitHubRepo.from_dict(node))

            return repos

        except subprocess.TimeoutExpired:
            raise RuntimeError("GitHub API request timed out")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse GitHub response: {e}")

    def get_user_commits_count(self, repo_full_name: str) -> int:
        """Get number of commits by authenticated user in a repo.

        Args:
            repo_full_name: Full repo name (e.g., "owner/repo")

        Returns:
            Number of commits by the user
        """
        try:
            # Get authenticated user
            user_result = subprocess.run(
                ["gh", "api", "user", "-q", ".login"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if user_result.returncode != 0:
                return 0

            username = user_result.stdout.strip()

            # Count commits by user
            commits_result = subprocess.run(
                ["gh", "api", f"repos/{repo_full_name}/commits",
                 "--paginate", "-q", f'.[].commit.author.name | select(. == "{username}") | length'],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if commits_result.returncode != 0:
                return 0

            # Count non-empty lines
            count = len([line for line in commits_result.stdout.strip().split("\n") if line])
            return count

        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            return 0
