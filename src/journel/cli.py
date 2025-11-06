"""Main CLI interface for JOURNEL."""

import sys
from datetime import date
from pathlib import Path

import click

from . import __version__
from .config import Config
from .display import (
    console,
    print_completion_celebration,
    print_context_export,
    print_error,
    print_info,
    print_list,
    print_project_details,
    print_status,
    print_success,
    print_welcome,
)
from .models import LogEntry, Project
from .storage import Storage
from .utils import slugify


def get_storage(no_emoji: bool = False) -> Storage:
    """Get storage instance with config."""
    config = Config()
    if no_emoji:
        config.set("use_emojis", False)
    return Storage(config)


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
@click.option("--no-emoji", is_flag=True, help="Disable emoji output (use ASCII)")
@click.pass_context
def main(ctx, no_emoji):
    """JOURNEL - ADHD-friendly project organization system.

    Run without arguments to show project status.
    """
    # Store no_emoji flag in context for subcommands to access
    ctx.ensure_object(dict)
    ctx.obj['no_emoji'] = no_emoji

    if ctx.invoked_subcommand is None:
        # Default to status command
        ctx.invoke(status)


@main.command()
def init():
    """Initialize JOURNEL for first-time use."""
    config = Config()

    # Check if already initialized
    if config.journel_dir.exists() and (config.journel_dir / ".git").exists():
        print_error("JOURNEL is already initialized")
        print_info(f"Location: {config.journel_dir}")
        return

    storage = Storage(config)
    storage.init_structure()

    print_welcome()
    print_success(f"JOURNEL initialized at {config.journel_dir}")


@main.command()
@click.argument("name")
@click.option("--full-name", help="Full descriptive name")
@click.option("--tags", help="Comma-separated tags")
def new(name, full_name, tags):
    """Create a new project.

    Includes gentle gate-keeping to prevent project-hopping.
    """
    storage = get_storage()
    config = storage.config

    # Check for existing projects
    projects = storage.list_projects()
    active = [p for p in projects if p.status == "in-progress" and p.days_since_active() <= 14]

    # Gate-keeping: warn if too many active projects
    max_active = config.get("max_active_projects", 5)
    if len(active) >= max_active:
        print_error(f"You already have {len(active)} active projects!")
        console.print("\nActive projects:")
        for p in active:
            console.print(f"  - {p.name} ({p.completion}% complete)")

        if not click.confirm("\nReally start something new?", default=False):
            print_info("Good choice! Focus on finishing what you started.")
            return

    # Create project ID
    project_id = slugify(name)

    # Check if project already exists
    if storage.load_project(project_id):
        print_error(f"Project '{project_id}' already exists")
        return

    # Create project
    project = Project(
        id=project_id,
        name=name,
        full_name=full_name or name,
        tags=tags.split(",") if tags else [],
        created=date.today(),
        last_active=date.today(),
    )

    storage.save_project(project)
    storage.update_project_index()

    print_success(f"Created project: {name}")
    print_info(f"ID: {project_id}")
    print_info("Next steps:")
    console.print("  1. Add project details: jnl edit " + project_id)
    console.print("  2. Link to GitHub/Claude: jnl link " + project_id + " <url>")
    console.print("  3. Start logging work: jnl log \"your message\"")


@main.command()
@click.option("--brief", is_flag=True, help="Brief output for prompts")
@click.pass_context
def status(ctx, brief):
    """Show overview of all projects (default command)."""
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    config = storage.config

    projects = storage.list_projects()

    if not projects:
        print_info("No projects yet. Create one with: jnl new <name>")
        return

    if brief:
        active = [p for p in projects if p.status == "in-progress" and p.days_since_active() <= 14]
        console.print(f"[JOURNEL: {len(active)} active projects]")
    else:
        print_status(projects, config)


@main.command()
@click.argument("message")
@click.option("--project", "-p", help="Project to log for")
@click.option("--hours", "-h", type=float, help="Hours spent")
def log(message, project, hours):
    """Quick activity logging.

    If --project is not specified, attempts to detect current project
    from the current directory.
    """
    storage = get_storage()

    # Auto-detect project if not specified
    if not project:
        cwd = Path.cwd()
        # Try to match directory name to project
        potential_id = slugify(cwd.name)
        if storage.load_project(potential_id):
            project = potential_id

    # Create log entry
    entry = LogEntry(
        date=date.today(),
        project=project,
        message=message,
        hours=hours,
    )

    storage.add_log_entry(entry)

    # Update project last_active if project specified
    if project:
        proj = storage.load_project(project)
        if proj:
            proj.last_active = date.today()
            storage.save_project(proj)
            storage.update_project_index()

    print_success("Logged activity")
    if project:
        print_info(f"Project: {project}")


@main.command()
@click.option("--project", "-p", help="Export context for specific project")
@click.argument("question", required=False)
def ctx(project, question):
    """Export context for LLM analysis.

    Generates a markdown summary of active projects and recent activity
    that you can copy/paste to Claude or other AI assistants.

    Usage:
        jnl ctx
        jnl ctx "what should I work on today?"
        jnl ctx --project mica
    """
    storage = get_storage()

    # Get projects
    if project:
        proj = storage.load_project(project)
        if not proj:
            print_error(f"Project '{project}' not found")
            return
        projects = [proj]
    else:
        projects = storage.list_projects()
        # Filter to active only
        projects = [p for p in projects if p.status != "completed"]

    # Get recent logs
    recent_logs = storage.get_recent_logs(days=7)

    # Print context
    print_context_export(projects, recent_logs, question)


@main.command()
@click.argument("question")
@click.option("--project", "-p", help="Focus on specific project")
def ask(question, project):
    """Format a question with auto-gathered context.

    This is similar to 'ctx' but formats output specifically as a question
    for AI assistants.

    Usage:
        jnl ask "what should I work on today?"
        jnl ask "how can I finish this faster?" --project mica
    """
    storage = get_storage()

    # Get projects
    if project:
        proj = storage.load_project(project)
        if not proj:
            print_error(f"Project '{project}' not found")
            return
        projects = [proj]
    else:
        projects = storage.list_projects()
        # Filter to active only
        projects = [p for p in projects if p.status != "completed"]

    # Get recent logs
    recent_logs = storage.get_recent_logs(days=7)

    # Print context with question prominently
    print_context_export(projects, recent_logs, question)


@main.command()
@click.argument("project_id")
@click.pass_context
def done(ctx, project_id):
    """Mark a project as complete with celebration ritual!"""
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    config = storage.config

    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        return

    if project.status == "completed":
        print_info(f"{project.name} is already completed!")
        return

    # Ask what they learned
    learned = click.prompt("\nWhat did you learn?", default="", show_default=False)
    if learned:
        project.learned = learned

    # Optional: how do you feel?
    feeling = click.prompt("How do you feel? (optional)", default="", show_default=False)
    if feeling:
        # Append to notes
        project.notes += f"\n\n## Completion Reflection\n{feeling}\n"

    # Mark as complete
    project.completion = 100
    project.status = "completed"
    project.last_active = date.today()

    storage.move_to_completed(project)
    storage.update_project_index()

    # Count total completed
    completed = [p for p in storage.list_projects() if p.status == "completed"]

    # Celebrate!
    if config.get("completion_celebration"):
        use_emojis = config.get("use_emojis", True)
        print_completion_celebration(project, len(completed), use_emojis)
    else:
        print_success(f"Project '{project.name}' marked as complete!")


@main.command()
@click.argument("project_id")
def resume(project_id):
    """Restore context for picking up work on a project."""
    storage = get_storage()

    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        return

    console.print(f"\n[bold]Resuming: {project.name}[/bold]\n")

    console.print(f"Last worked: {project.last_active} ({project.days_since_active()} days ago)")
    console.print(f"Completion: {project.completion}%\n")

    if project.next_steps:
        console.print(f"[bold cyan]Next steps:[/bold cyan] {project.next_steps}\n")

    if project.blockers:
        console.print(f"[bold red]Blockers:[/bold red] {project.blockers}\n")

    if project.claude_project:
        console.print(f"[dim]Claude:[/dim] {project.claude_project}")

    if project.github:
        console.print(f"[dim]GitHub:[/dim] {project.github}")

    console.print()

    # Update last_active
    project.last_active = date.today()
    storage.save_project(project)


@main.command(name="list")
@click.option("--active", is_flag=True, help="Show only active projects")
@click.option("--dormant", is_flag=True, help="Show only dormant projects")
@click.option("--completed", is_flag=True, help="Show only completed projects")
@click.option("--tag", help="Filter by tag")
def list_projects(active, dormant, completed, tag):
    """List all projects with optional filters."""
    storage = get_storage()
    projects = storage.list_projects()

    # Apply filters
    dormant_days = storage.config.get("dormant_days", 14)

    if active:
        projects = [p for p in projects if p.status == "in-progress" and p.days_since_active() <= dormant_days]
        title = "Active Projects"
    elif dormant:
        projects = [p for p in projects if p.days_since_active() > dormant_days and p.status != "completed"]
        title = "Dormant Projects"
    elif completed:
        projects = [p for p in projects if p.status == "completed"]
        title = "Completed Projects"
    else:
        title = "All Projects"

    if tag:
        projects = [p for p in projects if tag in p.tags]
        title += f" (tag: {tag})"

    print_list(projects, title=title)


@main.command()
@click.argument("project_id")
def edit(project_id):
    """Open project file in editor."""
    storage = get_storage()
    config = storage.config

    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        return

    # Determine file path
    if project.status == "completed":
        file_path = config.completed_dir / project.file_name
    else:
        file_path = config.projects_dir / project.file_name

    # Open in editor
    editor = config.get("editor", "notepad")
    import subprocess

    try:
        subprocess.run([editor, str(file_path)], check=True)
    except Exception as e:
        print_error(f"Failed to open editor: {e}")
        print_info(f"File location: {file_path}")


@main.command()
@click.argument("project_id")
@click.argument("url")
@click.option("--github", is_flag=True, help="Add as GitHub URL")
@click.option("--claude", is_flag=True, help="Add as Claude project URL")
def link(project_id, url, github, claude):
    """Add GitHub or Claude links to a project."""
    storage = get_storage()

    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        return

    if github or "github.com" in url:
        project.github = url
        print_success(f"Added GitHub link to {project.name}")
    elif claude or "claude.ai" in url:
        project.claude_project = url
        print_success(f"Added Claude project link to {project.name}")
    else:
        # Ask which type
        if click.confirm("Is this a GitHub URL?", default=True):
            project.github = url
        else:
            project.claude_project = url
        print_success(f"Added link to {project.name}")

    storage.save_project(project)


@main.command()
@click.argument("text")
def note(text):
    """Quick note capture (goes to today's log and current project if detected)."""
    storage = get_storage()

    # Try to detect current project
    cwd = Path.cwd()
    potential_id = slugify(cwd.name)
    project = None

    if storage.load_project(potential_id):
        project = potential_id

    # Add to log
    entry = LogEntry(
        date=date.today(),
        project=project,
        message=f"Note: {text}",
    )

    storage.add_log_entry(entry)
    print_success("Note saved")
    if project:
        print_info(f"Associated with project: {project}")


@main.command()
@click.pass_context
def wins(ctx):
    """Show completed projects and achievements."""
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    config = storage.config
    use_emojis = config.get("use_emojis", True)

    completed = [p for p in storage.list_projects(status="completed")]

    if not completed:
        print_info("No completed projects yet. Finish one with: jnl done <project>")
        return

    # Sort by completion date (last_active)
    completed.sort(key=lambda p: p.last_active, reverse=True)

    from .display import get_icon
    check = get_icon("check", use_emojis)
    party = get_icon("party", use_emojis)
    fire = get_icon("fire", use_emojis)

    console.print(f"\n[bold green]{check} COMPLETED PROJECTS[/bold green]", f"({len(completed)})\n")

    # Show recent completions
    recent = completed[:5]
    console.print("[bold]Recent completions:[/bold]")
    for p in recent:
        from .utils import format_date_relative
        console.print(f"  {party} {p.name:<30} (completed {format_date_relative(p.last_active)})")
        if p.learned:
            console.print(f"     [dim]Learned: {p.learned}[/dim]")

    if len(completed) > 5:
        console.print(f"\n[dim]All time:[/dim] {', '.join([p.name for p in completed[5:]])}")

    # Calculate streak (completions in last 30 days)
    recent_wins = [p for p in completed if p.days_since_active() <= 30]
    if recent_wins:
        console.print(f"\n[bold yellow]{fire} Current streak:[/bold yellow] {len(recent_wins)} completion(s) in the last month!")

    console.print()


@main.command()
@click.pass_context
def stats(ctx):
    """Show overall statistics and insights."""
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    config = storage.config

    all_projects = storage.list_projects()

    # Categorize
    dormant_days = config.get("dormant_days", 14)
    active = [p for p in all_projects if p.status == "in-progress" and p.days_since_active() <= dormant_days]
    dormant = [p for p in all_projects if p.status == "in-progress" and p.days_since_active() > dormant_days]
    completed = [p for p in all_projects if p.status == "completed"]

    console.print("\n[bold]📊 JOURNEL Statistics[/bold]\n" if config.get("use_emojis") else "\n[bold]JOURNEL Statistics[/bold]\n")

    # Project counts
    console.print("[bold]Projects:[/bold]")
    console.print(f"  Active: {len(active)}")
    console.print(f"  Dormant: {len(dormant)}")
    console.print(f"  Completed: {len(completed)}")
    console.print(f"  Total: {len(all_projects)}")

    # Completion rate
    if len(all_projects) > 0:
        completion_rate = (len(completed) / len(all_projects)) * 100
        console.print(f"\n[bold]Completion Rate:[/bold] {completion_rate:.1f}%")

    # Recent activity
    recent_active = [p for p in all_projects if p.days_since_active() <= 7]
    console.print(f"\n[bold]Active This Week:[/bold] {len(recent_active)} projects")

    # Streak
    recent_completions = [p for p in completed if p.days_since_active() <= 30]
    if recent_completions:
        console.print(f"[bold]Recent Wins:[/bold] {len(recent_completions)} completions in last 30 days")

    # Most complete project
    in_progress = [p for p in all_projects if p.status == "in-progress"]
    if in_progress:
        most_complete = max(in_progress, key=lambda p: p.completion)
        console.print(f"\n[bold]Closest to Done:[/bold] {most_complete.name} ({most_complete.completion}%)")

    # Oldest active project
    if active:
        oldest = min(active, key=lambda p: p.last_active)
        console.print(f"[bold]Oldest Active:[/bold] {oldest.name} (last worked {oldest.days_since_active()} days ago)")

    console.print()


@main.command()
def sync():
    """Sync JOURNEL data with git remote.

    Performs git pull, then git push to sync your ~/.journel directory
    across machines.
    """
    storage = get_storage()

    if not storage.repo:
        print_error("Git repository not initialized. Run 'journel init' first.")
        return

    try:
        console.print("[cyan]Syncing with git remote...[/cyan]")

        # Check if remote exists
        if not storage.repo.remotes:
            print_error("No git remote configured.")
            print_info("Set up a remote with: cd ~/.journel && git remote add origin <url>")
            return

        origin = storage.repo.remotes.origin

        # Pull first
        console.print("Pulling changes...")
        origin.pull()

        # Commit any local changes
        if storage.repo.is_dirty():
            storage.repo.index.add(["."])
            storage.repo.index.commit("Sync: local changes")

        # Push
        console.print("Pushing changes...")
        origin.push()

        print_success("Sync complete!")

    except Exception as e:
        print_error(f"Sync failed: {e}")
        print_info("You can manually sync with: cd ~/.journel && git pull && git push")


if __name__ == "__main__":
    main()
