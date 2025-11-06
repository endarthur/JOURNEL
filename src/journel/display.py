"""Display and formatting utilities using Rich."""

from datetime import date
from typing import List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .models import Project
from .utils import format_date_relative


console = Console()

# Emoji mappings (can be disabled via config)
EMOJIS = {
    "fire": "🔥",
    "sleep": "💤",
    "check": "✅",
    "bulb": "💡",
    "warning": "⚠️",
    "party": "🎉",
    "star": "🌟",
}

ASCII_FALLBACKS = {
    "fire": ">>",
    "sleep": "--",
    "check": "[DONE]",
    "bulb": "[TIP]",
    "warning": "[!]",
    "party": "***",
    "star": "*",
}


def get_icon(name: str, use_emojis: bool = True) -> str:
    """Get an icon (emoji or ASCII fallback)."""
    if use_emojis:
        return EMOJIS.get(name, "")
    return ASCII_FALLBACKS.get(name, "")


def print_welcome() -> None:
    """Print welcome message after init."""
    welcome = """
[bold green]Welcome to JOURNEL![/bold green]

Your ADHD-friendly project tracking system is ready.

[bold]Quick start:[/bold]
  jnl new <project>    Create your first project
  jnl                  Check status
  jnl log "message"    Log what you're working on
  jnl ctx              Get context for AI assistance

[dim]JOURNEL data is stored in ~/.journel/
All files are plain markdown - edit them anytime![/dim]
"""
    console.print(Panel(welcome, border_style="green"))


def print_status(projects: List[Project], config) -> None:
    """Print project status overview."""
    # Categorize projects
    active = []
    dormant = []
    completed = []

    dormant_days = config.get("dormant_days", 14)
    use_emojis = config.get("use_emojis", True)

    for p in projects:
        if p.status == "completed":
            completed.append(p)
        elif p.days_since_active() > dormant_days:
            dormant.append(p)
        else:
            active.append(p)

    # Sort by last_active
    active.sort(key=lambda p: p.last_active, reverse=True)
    dormant.sort(key=lambda p: p.last_active, reverse=True)
    completed.sort(key=lambda p: p.last_active, reverse=True)

    # Print active projects
    if active:
        fire = get_icon("fire", use_emojis)
        console.print(f"\n[bold yellow]{fire} ACTIVE[/bold yellow]", f"({len(active)})")
        for p in active:
            status_line = f"  [bold]{p.name:<20}[/bold] {p.completion:>3}%   {format_date_relative(p.last_active):<15}"
            if p.next_steps:
                status_line += f"  [dim][{p.next_steps[:40]}][/dim]"
            console.print(status_line)
    else:
        console.print("\n[dim]No active projects[/dim]")

    # Print dormant projects
    if dormant:
        sleep = get_icon("sleep", use_emojis)
        console.print(f"\n[bold blue]{sleep} DORMANT[/bold blue] ({len(dormant)})")
        for p in dormant[:5]:  # Show max 5
            console.print(f"  [dim]{p.name:<20}[/dim] {p.completion:>3}%   {format_date_relative(p.last_active):<15}")
        if len(dormant) > 5:
            console.print(f"  [dim]... and {len(dormant) - 5} more[/dim]")

    # Print completed summary
    if completed:
        check = get_icon("check", use_emojis)
        console.print(f"\n[bold green]{check} COMPLETED[/bold green] ({len(completed)})")
        recent = completed[:3]
        if recent:
            names = ", ".join([p.name for p in recent])
            console.print(f"  [dim]Recently: {names}[/dim]")

    # Print tips/nudges
    if config.get("gentle_nudges"):
        if active:
            # Find nearly done projects
            nearly_done = [p for p in active if p.completion >= 80]
            if nearly_done:
                p = nearly_done[0]
                bulb = get_icon("bulb", use_emojis)
                console.print(f"\n[bold cyan]{bulb} Tip:[/bold cyan] {p.name} is {p.completion}% done - finish it first?")

        # Warn about too many active projects
        max_active = config.get("max_active_projects", 5)
        if len(active) > max_active:
            warn = get_icon("warning", use_emojis)
            console.print(f"\n[yellow]{warn} You have {len(active)} active projects. Consider completing some before starting new ones.[/yellow]")

    console.print()  # Blank line


def print_project_details(project: Project) -> None:
    """Print detailed project information."""
    console.print(f"\n[bold]{project.full_name or project.name}[/bold]")
    console.print(f"Status: {project.status} | Completion: {project.completion}%")
    console.print(f"Last active: {format_date_relative(project.last_active)}")

    if project.tags:
        console.print(f"Tags: {', '.join(project.tags)}")

    if project.next_steps:
        console.print(f"\n[bold cyan]Next steps:[/bold cyan] {project.next_steps}")

    if project.blockers:
        console.print(f"[bold red]Blockers:[/bold red] {project.blockers}")

    if project.github:
        console.print(f"\nGitHub: {project.github}")

    if project.claude_project:
        console.print(f"Claude: {project.claude_project}")

    console.print()


def print_completion_celebration(project: Project, total_completed: int, use_emojis: bool = True) -> None:
    """Print celebration message when completing a project."""
    party = get_icon("party", use_emojis)
    star = get_icon("star", use_emojis)

    celebration = f"""
[bold green]{party} CONGRATULATIONS! {party}[/bold green]

[bold]{project.name}[/bold] is COMPLETE!

"""
    if total_completed > 1:
        celebration += f"That's your {_ordinal(total_completed)} completion!"
    else:
        celebration += f"That's your first completion! {star}"

    console.print(Panel(celebration, border_style="green", expand=False))


def print_list(projects: List[Project], title: str = "Projects") -> None:
    """Print a list of projects in table format."""
    if not projects:
        console.print("[dim]No projects found[/dim]")
        return

    table = Table(title=title, show_header=True, header_style="bold")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Status", style="yellow")
    table.add_column("Progress", justify="right")
    table.add_column("Last Active", style="dim")
    table.add_column("Tags", style="dim")

    for p in projects:
        table.add_row(
            p.name,
            p.status,
            f"{p.completion}%",
            format_date_relative(p.last_active),
            ", ".join(p.tags[:2]) if p.tags else "",
        )

    console.print(table)


def print_context_export(projects: List[Project], recent_logs: str, question: str = None) -> None:
    """Print context export for LLM."""
    output = ["# JOURNEL Context Export", ""]

    # Active projects
    active = [p for p in projects if p.status != "completed" and p.days_since_active() <= 14]
    if active:
        output.append("## Active Projects")
        output.append("")
        for p in active:
            output.append(f"### {p.name} ({p.completion}% complete)")
            output.append(f"- Last active: {format_date_relative(p.last_active)}")
            if p.next_steps:
                output.append(f"- Next steps: {p.next_steps}")
            if p.blockers:
                output.append(f"- Blockers: {p.blockers}")
            output.append("")

    # Recent activity
    output.append("## Recent Activity")
    output.append("")
    output.append(recent_logs)
    output.append("")

    # Question if provided
    if question:
        output.append("## Question")
        output.append("")
        output.append(question)
        output.append("")

    output.append("---")
    output.append("[Copy this to Claude for analysis]")

    console.print("\n".join(output))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green][OK][/green] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[cyan]>>>[/cyan] {message}")


def _ordinal(n: int) -> str:
    """Convert number to ordinal string (1st, 2nd, 3rd, etc.)."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
