"""GitHub repository import with ADHD-friendly batch workflow."""

import json
import sys
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any

import click

from .config import Config
from .display import console, print_error, print_success, print_info
from .github_client import GitHubClient, GitHubRepo
from .models import Project
from .storage import Storage
from .utils import slugify, format_date_relative


BATCH_SIZE = 10


def load_import_state(storage: Storage) -> Optional[Dict[str, Any]]:
    """Load import state from meta directory."""
    import yaml
    state_file = storage.config.meta_dir / "import_state.yaml"

    if not state_file.exists():
        return None

    with open(state_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_import_state(storage: Storage, state: Dict[str, Any]) -> None:
    """Save import state to meta directory."""
    import yaml
    storage.config.meta_dir.mkdir(parents=True, exist_ok=True)
    state_file = storage.config.meta_dir / "import_state.yaml"

    state["last_updated"] = datetime.now().isoformat()

    with open(state_file, "w", encoding="utf-8") as f:
        yaml.dump(state, f, default_flow_style=False)


def clear_import_state(storage: Storage) -> None:
    """Clear import state file."""
    state_file = storage.config.meta_dir / "import_state.yaml"
    if state_file.exists():
        state_file.unlink()


def create_new_import_state() -> Dict[str, Any]:
    """Create new import state."""
    return {
        "session_id": datetime.now().strftime("%Y-%m-%d-%H%M%S"),
        "started": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "stats": {
            "total_repos": 0,
            "filtered_out": 0,
            "remaining": 0,
        },
        "processed": {
            "imported_as_active": 0,
            "imported_as_ongoing": 0,
            "imported_as_maintenance": 0,
            "imported_as_archived": 0,
            "skipped": 0,
        },
        "repos_processed": [],
        "current_position": 0,
    }


def apply_filters(
    repos: List[GitHubRepo],
    include_archived: bool = False,
    include_forks: bool = False,
    recent_only: bool = False,
    months: int = 3,
) -> tuple[List[GitHubRepo], int]:
    """Apply filters to repo list.

    Returns:
        Tuple of (filtered_repos, filtered_out_count)
    """
    filtered = []
    filtered_out = 0

    for repo in repos:
        # Skip archived repos unless included
        if repo.archived and not include_archived:
            filtered_out += 1
            continue

        # Skip forks unless included (heuristic: fork with no stars likely unused)
        if repo.fork and not include_forks and repo.stargazers_count == 0:
            filtered_out += 1
            continue

        # Skip empty repos
        if repo.size == 0:
            filtered_out += 1
            continue

        # Filter by recency
        if recent_only:
            cutoff = datetime.now().replace(tzinfo=repo.pushed_at.tzinfo) - timedelta(days=30 * months)
            if repo.pushed_at < cutoff:
                filtered_out += 1
                continue

        filtered.append(repo)

    return filtered, filtered_out


def get_single_keypress() -> str:
    """Get single keypress without requiring Enter.

    Falls back to input() on systems without termios.
    """
    try:
        # Try Unix-style (termios)
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
            return char
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except (ImportError, AttributeError):
        # Fall back to regular input on Windows
        return input().strip().lower()[:1] if input().strip() else ""


def process_repo_ai_mode(
    repo: GitHubRepo,
    index: int,
    total: int,
    storage: Storage,
    state: Dict[str, Any],
    json_output: bool = False,
) -> Optional[str]:
    """Process a single repo in AI-friendly mode.

    If json_output=True:
        - Emits JSON lines to stdout
        - Reads single-line decisions from stdin
        - No prompts, no colors, pure data exchange

    If json_output=False (AI-mode but human-readable):
        - Emits plain text (no colors/formatting)
        - Clear, parseable structure
        - Machine-readable but also human-debuggable

    Returns:
        None to continue, "quit" to quit
    """
    config = storage.config

    if json_output:
        # Emit repo as JSON
        repo_data = {
            "type": "repo",
            "index": index,
            "total": total,
            "name": repo.name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "last_push": repo.pushed_at.date().isoformat(),
            "language": repo.language,
            "open_issues": repo.open_issues_count,
            "url": repo.html_url,
        }
        print(json.dumps(repo_data), flush=True)

        # Emit prompt
        prompt_data = {
            "type": "prompt",
            "message": "Classify as: active | ongoing | maintenance | archive | skip | quit",
            "options": ["active", "ongoing", "maintenance", "archive", "skip", "quit"],
        }
        print(json.dumps(prompt_data), flush=True)

        # Signal ready for input
        print(json.dumps({"type": "awaiting_input"}), flush=True)

        # Read response from stdin (blocking)
        try:
            response = input().strip().lower()
        except EOFError:
            response = "quit"

    else:
        # Plain text AI mode (debuggable)
        print(f"\n{'-' * 60}")
        print(f"REPO {index}/{total}")
        print(f"{'-' * 60}")
        print(f"Name: {repo.name}")
        print(f"Description: {repo.description or 'N/A'}")
        print(f"Stars: {repo.stargazers_count} | Language: {repo.language or 'N/A'}")
        print(f"Last push: {repo.pushed_at.date()}")
        if repo.open_issues_count > 0:
            print(f"Open issues: {repo.open_issues_count}")
        print(f"\nClassify as: active | ongoing | maintenance | archive | skip | quit")
        print("> ", end="", flush=True)

        try:
            response = input().strip().lower()
        except EOFError:
            response = "quit"

    # Process response
    if response == "quit" or response == "q":
        return "quit"

    elif response == "active" or response == "a":
        # Check gate-keeping for active projects
        projects = storage.list_projects()
        active_regular = [p for p in projects if p.status == "in-progress" and p.project_type == "regular"]

        max_active = config.get("max_active_projects", 5)
        gate_issue = False

        if len(active_regular) >= max_active:
            gate_issue = True
            if json_output:
                warning_data = {
                    "type": "gate_warning",
                    "severity": "high",
                    "message": f"Already have {len(active_regular)} active projects (limit: {max_active})",
                    "current_count": len(active_regular),
                    "limit": max_active,
                    "recommendation": "ongoing_or_archive",
                }
                print(json.dumps(warning_data), flush=True)
            else:
                print(f"\n⚠️  You already have {len(active_regular)} active projects (limit: {max_active})!")
                print("Current active projects:")
                for p in active_regular[:5]:
                    print(f"  - {p.name} ({p.completion}% complete)")
                print("\nArchiving instead...")

        if gate_issue:
            create_project_from_repo(repo, storage, "archived")
            state["processed"]["imported_as_archived"] += 1
            if json_output:
                result = {
                    "type": "result",
                    "action": "imported_as_archived",
                    "name": repo.name,
                    "reason": "active_limit_hit",
                }
                print(json.dumps(result), flush=True)
            else:
                print("Result: Archived (active limit reached)")
        else:
            create_project_from_repo(repo, storage, "active")
            state["processed"]["imported_as_active"] += 1
            if json_output:
                result = {
                    "type": "result",
                    "action": "imported_as_active",
                    "name": repo.name,
                }
                print(json.dumps(result), flush=True)
            else:
                print("Result: Created as ACTIVE")

    elif response == "ongoing" or response == "o":
        create_project_from_repo(repo, storage, "ongoing")
        state["processed"]["imported_as_ongoing"] += 1
        if json_output:
            result = {
                "type": "result",
                "action": "imported_as_ongoing",
                "name": repo.name,
            }
            print(json.dumps(result), flush=True)
        else:
            print("Result: Created as ONGOING")

    elif response == "maintenance" or response == "m":
        create_project_from_repo(repo, storage, "maintenance")
        state["processed"]["imported_as_maintenance"] += 1
        if json_output:
            result = {
                "type": "result",
                "action": "imported_as_maintenance",
                "name": repo.name,
            }
            print(json.dumps(result), flush=True)
        else:
            print("Result: Created as MAINTENANCE")

    elif response == "skip" or response == "s":
        state["processed"]["skipped"] += 1
        if json_output:
            result = {
                "type": "result",
                "action": "skipped",
                "name": repo.name,
            }
            print(json.dumps(result), flush=True)
        else:
            print("Result: Skipped")

    else:  # archive or Enter or any other key
        create_project_from_repo(repo, storage, "archived")
        state["processed"]["imported_as_archived"] += 1
        if json_output:
            result = {
                "type": "result",
                "action": "imported_as_archived",
                "name": repo.name,
            }
            print(json.dumps(result), flush=True)
        else:
            print("Result: Archived")

    # Track in state
    state["repos_processed"].append({
        "name": repo.name,
        "action": response or "archive",
        "timestamp": datetime.now().isoformat(),
    })
    state["current_position"] = index

    return None


def process_repo_interactive(
    repo: GitHubRepo,
    index: int,
    total: int,
    storage: Storage,
    state: Dict[str, Any],
) -> Optional[str]:
    """Process a single repo interactively.

    Returns:
        None to continue, "quit" to quit, "next_batch" for next batch prompt
    """
    config = storage.config

    # Display repo info
    console.print(f"\n{'-' * 60}\n")
    console.print(f"[bold cyan][{index}/{total}] {repo.name}[/bold cyan]")
    console.print(f"      ⭐ {repo.stargazers_count} stars | 📅 {format_date_relative(repo.pushed_at.date())}")

    if repo.description:
        desc = repo.description[:70] + "..." if len(repo.description) > 70 else repo.description
        console.print(f"      {desc}")

    if repo.open_issues_count > 0:
        console.print(f"      🔧 {repo.open_issues_count} open issues")

    if repo.language:
        console.print(f"      💻 {repo.language}")

    console.print(f"\n      [dim][a]ctive / [o]ngoing / [Enter]=archive / [s]kip / [q]uit[/dim]")
    console.print("      > ", end="")

    # Get input
    choice = get_single_keypress().lower()
    console.print(choice if choice else "[Enter]")  # Echo the choice

    # Process choice
    if choice == 'q':
        return "quit"

    elif choice == 'a':
        # Check gate-keeping for active projects
        projects = storage.list_projects()
        active_regular = [p for p in projects if p.status == "in-progress" and p.project_type == "regular"]

        max_active = config.get("max_active_projects", 5)
        if len(active_regular) >= max_active:
            console.print(f"\n[yellow]⚠️  You already have {len(active_regular)} active projects![/yellow]")
            console.print("\nCurrent active projects:")
            for p in active_regular[:5]:
                console.print(f"  - {p.name} ({p.completion}% complete)")

            if not click.confirm("\nReally add as active?", default=False):
                console.print("\n[dim]Archiving instead...[/dim]")
                create_project_from_repo(repo, storage, "archived")
                state["processed"]["imported_as_archived"] += 1
            else:
                create_project_from_repo(repo, storage, "active")
                state["processed"]["imported_as_active"] += 1
        else:
            create_project_from_repo(repo, storage, "active")
            state["processed"]["imported_as_active"] += 1
            console.print("\n✅ Created as ACTIVE")

    elif choice == 'o':
        create_project_from_repo(repo, storage, "ongoing")
        state["processed"]["imported_as_ongoing"] += 1
        console.print("\n✅ Created as ONGOING")

    elif choice == 's':
        state["processed"]["skipped"] += 1
        console.print("\n⏭️  Skipped (not imported)")

    else:  # Enter or any other key = archive
        create_project_from_repo(repo, storage, "archived")
        state["processed"]["imported_as_archived"] += 1
        console.print("\n✅ Archived")

    # Track in state
    state["repos_processed"].append({
        "name": repo.name,
        "action": choice or "archive",
        "timestamp": datetime.now().isoformat(),
    })
    state["current_position"] = index

    return None


def create_project_from_repo(repo: GitHubRepo, storage: Storage, status: str) -> None:
    """Create JOURNEL project from GitHub repo."""
    project_id = slugify(repo.name)

    # Check if already exists
    existing = storage.load_project(project_id)
    if existing:
        console.print(f"[yellow]Note:[/yellow] Project '{project_id}' already exists, skipping")
        return

    # Determine project type and status
    if status == "ongoing":
        project_type = "ongoing"
    elif status == "maintenance":
        project_type = "maintenance"
    else:
        project_type = "regular"

    project_status = "in-progress" if status in ["active", "ongoing", "maintenance"] else "archived"

    # Create project
    project = Project(
        id=project_id,
        name=repo.name,
        full_name=repo.description or repo.name,
        tags=repo.topics if repo.topics else [],
        created=date.today(),
        last_active=repo.pushed_at.date(),
        status=project_status,
        project_type=project_type,
        github=repo.html_url,
    )

    # Add import metadata to notes
    lang_line = f"Language: {repo.language}" if repo.language else ""
    project.notes = f"""# GitHub Import

Imported from: {repo.html_url}
Last activity: {repo.pushed_at.date()}
Stars: {repo.stargazers_count}
{lang_line}

## Next Steps

[Add your next steps here]
"""

    # Save project
    if status == "archived":
        # Save to archived directory
        storage.config.archived_dir.mkdir(parents=True, exist_ok=True)
        archived_path = storage.config.archived_dir / f"{project_id}.md"
        storage._save_project_to_path(project, archived_path)
    else:
        storage.save_project(project)

    storage.update_project_index()


def show_batch_summary(state: Dict[str, Any], batch_num: int, total_batches: int) -> None:
    """Show summary after completing a batch."""
    console.print(f"\n{'-' * 60}\n")
    console.print(f"[bold green]Batch {batch_num} complete![/bold green]")
    console.print(f"\n[cyan]Summary so far:[/cyan]")
    console.print(f"  Active: {state['processed']['imported_as_active']} projects")
    console.print(f"  Ongoing: {state['processed']['imported_as_ongoing']} projects")
    console.print(f"  Archived: {state['processed']['imported_as_archived']} projects")
    console.print(f"  Skipped: {state['processed']['skipped']} repos")

    # Show gate-keeping status
    active_count = state['processed']['imported_as_active']
    if active_count >= 3:
        console.print(f"\n[yellow]⚠️  You have {active_count} active projects now (limit: 5)[/yellow]")


def show_quit_summary(state: Dict[str, Any], remaining: int) -> None:
    """Show summary when user quits."""
    console.print(f"\n{'-' * 60}\n")
    console.print("[bold cyan]Import paused! Progress saved.[/bold cyan]")
    console.print("\nYou can resume anytime with: [bold]jnl import github --resume[/bold]")
    console.print("\n[cyan]What you've done:[/cyan]")
    console.print(f"  ✅ Processed: {state['current_position']} repos")
    console.print(f"  📦 Archived: {state['processed']['imported_as_archived']}")
    console.print(f"  ⭐ Created: {state['processed']['imported_as_active'] + state['processed']['imported_as_ongoing']} projects")
    console.print(f"  ⏭️  Skipped: {state['processed']['skipped']}")
    console.print(f"\nRemaining: {remaining} repos")
    console.print("\n[bold green]Great work! Take a break. 🎉[/bold green]\n")


def show_completion_summary(state: Dict[str, Any]) -> None:
    """Show summary when import is complete."""
    console.print(f"\n{'-' * 60}\n")
    console.print("[bold green]🎉 GitHub Import Complete! 🎉[/bold green]")
    console.print("\n[cyan]Final Summary:[/cyan]")
    console.print(f"  Total processed: {state['current_position']} repos")
    console.print(f"  Active projects: {state['processed']['imported_as_active']}")
    console.print(f"  Ongoing projects: {state['processed']['imported_as_ongoing']}")
    console.print(f"  Archived: {state['processed']['imported_as_archived']}")
    console.print(f"  Skipped: {state['processed']['skipped']}")
    console.print("\nUse [bold]jnl status[/bold] to see your projects!")
    console.print("Use [bold]jnl list --archived[/bold] to see archived projects.\n")


def import_github_repos(
    recent_only: bool = False,
    resume: bool = False,
    preview: bool = False,
    archive_remaining: bool = False,
    include_archived: bool = False,
    include_forks: bool = False,
    ai_mode: bool = False,
    json_output: bool = False,
    force_new: bool = False,
) -> None:
    """Import GitHub repos with ADHD-friendly batch workflow."""
    config = Config()
    storage = Storage(config)

    # json_output implies ai_mode
    if json_output:
        ai_mode = True

    # Initialize GitHub client
    try:
        client = GitHubClient()
    except RuntimeError as e:
        print_error(str(e))
        return

    # Load or create state
    if force_new:
        # Clear existing state
        clear_import_state(storage)
        state = create_new_import_state()
    elif resume:
        state = load_import_state(storage)
        if not state:
            if not ai_mode:
                print_error("No previous import session found")
                console.print("[dim]Start a new import with: jnl import github[/dim]\n")
            else:
                # AI mode: just start new silently
                state = create_new_import_state()
            return
        if not ai_mode:
            console.print(f"\n[cyan]Resuming import from {state['started'][:10]}[/cyan]")
            console.print(f"Progress: {state['current_position']} processed, continuing...")
    else:
        # Check for existing state (auto-resume in AI mode)
        existing_state = load_import_state(storage)
        if existing_state and ai_mode:
            # AI mode: auto-resume
            state = existing_state
        elif existing_state and not ai_mode:
            # Human mode: ask
            state = existing_state
            console.print(f"\n[cyan]Import in progress detected ({state['current_position']} processed)[/cyan]")
            if not click.confirm("Resume where you left off?", default=True):
                clear_import_state(storage)
                state = create_new_import_state()
        else:
            state = create_new_import_state()

    # Fetch repos
    console.print("\n[cyan]Fetching your GitHub repos...[/cyan]")
    try:
        all_repos = client.fetch_user_repos()
    except RuntimeError as e:
        print_error(f"Failed to fetch repos: {e}")
        return

    if not all_repos:
        print_info("No repositories found")
        return

    # Apply filters
    repos, filtered_out = apply_filters(
        all_repos,
        include_archived=include_archived,
        include_forks=include_forks,
        recent_only=recent_only,
    )

    if not repos:
        print_info("No repositories match the filters")
        return

    # Update state
    state["stats"]["total_repos"] = len(all_repos)
    state["stats"]["filtered_out"] = filtered_out
    state["stats"]["remaining"] = len(repos)

    # Show summary
    console.print(f"\nFound [bold]{len(all_repos)}[/bold] repos total")
    console.print(f"Filtered to [bold]{len(repos)}[/bold] (excluded: {filtered_out})")

    if preview:
        console.print("\n[bold]Preview Mode - Repos to import:[/bold]\n")
        for i, repo in enumerate(repos[:20], 1):
            console.print(f"  {i}. {repo.name} - {format_date_relative(repo.pushed_at.date())}")
        if len(repos) > 20:
            console.print(f"  ... and {len(repos) - 20} more")
        console.print(f"\nRun [bold]jnl import github[/bold] to start importing.\n")
        return

    # Start position (for resume)
    start_pos = state.get("current_position", 0)
    remaining_repos = repos[start_pos:]

    # Show header (skip in AI mode)
    if not ai_mode:
        console.print("\n" + "=" * 60)
        console.print("[bold cyan]GitHub Import - ADHD-Friendly Batch Mode[/bold cyan]")
        console.print("=" * 60)
        console.print("\nPress [bold]Enter[/bold] to ARCHIVE (default)")
        console.print("Press [bold]'a'[/bold] for ACTIVE, [bold]'o'[/bold] for ONGOING, [bold]'s'[/bold] to SKIP")
        console.print("Press [bold]'q'[/bold] to QUIT and save progress\n")

    # Process in batches
    total_batches = (len(remaining_repos) + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_num in range(1, total_batches + 1):
        start_idx = (batch_num - 1) * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(remaining_repos))
        batch = remaining_repos[start_idx:end_idx]

        # Show batch header (skip in AI mode)
        if not ai_mode:
            console.print(f"\n[bold]BATCH {batch_num} of {total_batches}[/bold] (showing {len(batch)} repos)\n")

        for i, repo in enumerate(batch):
            global_index = start_pos + start_idx + i + 1

            # Use AI mode or interactive mode
            if ai_mode:
                result = process_repo_ai_mode(repo, global_index, len(repos), storage, state, json_output)
            else:
                result = process_repo_interactive(repo, global_index, len(repos), storage, state)

            if result == "quit":
                save_import_state(storage, state)
                if not ai_mode:
                    show_quit_summary(state, len(repos) - global_index)
                elif json_output:
                    status_data = {
                        "type": "status",
                        "action": "quit",
                        "processed": global_index,
                        "remaining": len(repos) - global_index,
                        "stats": state["processed"],
                    }
                    print(json.dumps(status_data), flush=True)
                return

            # Save state after each repo
            save_import_state(storage, state)

        # Batch complete
        if not ai_mode:
            show_batch_summary(state, batch_num, total_batches)

            if batch_num < total_batches:
                console.print(f"\n[bold]Continue with next batch?[/bold] [Y/n/q] > ", end="")
                response = input().strip().lower()

                if response in ['q', 'quit']:
                    save_import_state(storage, state)
                    show_quit_summary(state, len(repos) - (start_pos + end_idx))
                    return
                elif response in ['n', 'no']:
                    save_import_state(storage, state)
                    show_quit_summary(state, len(repos) - (start_pos + end_idx))
                    return
        elif json_output:
            # Emit batch status in JSON mode
            status_data = {
                "type": "batch_complete",
                "batch": batch_num,
                "total_batches": total_batches,
                "processed": start_pos + end_idx,
                "remaining": len(repos) - (start_pos + end_idx),
                "stats": state["processed"],
            }
            print(json.dumps(status_data), flush=True)

    # All done!
    clear_import_state(storage)
    show_completion_summary(state)


def show_import_status() -> None:
    """Show GitHub import progress."""
    config = Config()
    storage = Storage(config)
    state = load_import_state(storage)

    if not state:
        console.print("\n[dim]No active import session.[/dim]")
        console.print("\nStart importing with: [bold]jnl import github[/bold]\n")
        return

    console.print("\n[bold cyan]GitHub Import Status[/bold cyan]\n")
    console.print(f"Session started: {state['started'][:19]}")
    console.print(f"Last updated: {state['last_updated'][:19]}")
    console.print(f"\n[cyan]Progress:[/cyan]")
    console.print(f"  Total repos: {state['stats']['total_repos']}")
    console.print(f"  Filtered out: {state['stats']['filtered_out']}")
    console.print(f"  Processed: {state['current_position']}")
    console.print(f"  Remaining: {state['stats']['remaining'] - state['current_position']}")
    console.print(f"\n[cyan]Actions:[/cyan]")
    console.print(f"  Imported as active: {state['processed']['imported_as_active']}")
    console.print(f"  Imported as ongoing: {state['processed']['imported_as_ongoing']}")
    console.print(f"  Archived: {state['processed']['imported_as_archived']}")
    console.print(f"  Skipped: {state['processed']['skipped']}")
    console.print(f"\nResume with: [bold]jnl import github --resume[/bold]\n")
