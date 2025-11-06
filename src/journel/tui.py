"""Terminal UI for JOURNEL using Textual."""

from datetime import date
from typing import List, Optional

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Label, ListItem, ListView, Static
from textual.binding import Binding

from .config import Config
from .storage import Storage
from .models import Project
from .utils import format_date_relative


class ProjectDetail(Static):
    """Widget to display project details."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project: Optional[Project] = None

    def set_project(self, project: Optional[Project]) -> None:
        """Update the displayed project."""
        self.project = project
        if project is None:
            self.update("[dim]No project selected[/dim]")
            return

        # Build rich markup for project details
        details = f"""[bold]{project.full_name or project.name}[/bold]

[cyan]Status:[/cyan] {project.status}
[cyan]Completion:[/cyan] {project.completion}%
[cyan]Last Active:[/cyan] {format_date_relative(project.last_active)}
[cyan]Created:[/cyan] {project.created}
"""

        if project.tags:
            details += f"\n[cyan]Tags:[/cyan] {', '.join(project.tags)}"

        if project.priority != "medium":
            details += f"\n[cyan]Priority:[/cyan] {project.priority}"

        if project.next_steps:
            details += f"\n\n[bold yellow]Next Steps:[/bold yellow]\n{project.next_steps}"

        if project.blockers:
            details += f"\n\n[bold red]Blockers:[/bold red]\n{project.blockers}"

        if project.github:
            details += f"\n\n[cyan]GitHub:[/cyan] {project.github}"

        if project.claude_project:
            details += f"\n[cyan]Claude:[/cyan] {project.claude_project}"

        if project.learned:
            details += f"\n\n[bold green]Learned:[/bold green]\n{project.learned}"

        self.update(details)


class ProjectListItem(ListItem):
    """Custom list item for projects."""

    def __init__(self, project: Project, *args, **kwargs):
        self.project = project

        # Build the label
        status_icon = {
            "in-progress": "▶",
            "completed": "✓",
            "dormant": "⏸",
            "archived": "📦",
        }.get(project.status, "•")

        self.label_text = f"{status_icon} {project.name} ({project.completion}%)"
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """Compose the list item with a label."""
        yield Static(self.label_text)


class JournelTUI(App):
    """A Textual TUI for JOURNEL."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 1fr 2fr;
    }

    #left-panel {
        width: 100%;
        height: 100%;
        border: solid $primary;
    }

    #right-panel {
        width: 100%;
        height: 100%;
        border: solid $secondary;
        padding: 1 2;
    }

    ListView {
        height: 100%;
    }

    ListItem {
        padding: 0 1;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: $boost;
        color: $text;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("f1", "filter_active", "Active"),
        Binding("f2", "filter_dormant", "Dormant"),
        Binding("f3", "filter_completed", "Completed"),
        Binding("f4", "filter_archived", "Archived"),
        Binding("f5", "filter_all", "All"),
        Binding("r", "refresh", "Refresh"),
        Binding("d", "mark_done", "Done"),
        Binding("a", "archive_project", "Archive"),
        Binding("u", "unarchive_project", "Unarchive"),
        Binding("e", "edit_project", "Edit"),
    ]

    def __init__(self, storage: Storage):
        super().__init__()
        self.storage = storage
        self.config = storage.config
        self.current_filter = "active"
        self.projects: List[Project] = []
        self.selected_project: Optional[Project] = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()

        with Horizontal():
            with Vertical(id="left-panel"):
                yield ListView(id="project-list")

            with Vertical(id="right-panel"):
                yield ProjectDetail(id="project-detail")

        yield Static("F1: Active | F2: Dormant | F3: Completed | F4: Archived | F5: All | R: Refresh | Q: Quit", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app when mounted."""
        self.title = "JOURNEL - Project Browser"
        self.sub_title = f"Filter: {self.current_filter.title()}"
        self.load_projects()

    def load_projects(self) -> None:
        """Load projects based on current filter."""
        dormant_days = self.config.get("dormant_days", 14)

        if self.current_filter == "all":
            self.projects = self.storage.list_projects(include_archived=True)
        elif self.current_filter == "archived":
            self.projects = self.storage.list_projects(status="archived")
        elif self.current_filter == "completed":
            self.projects = self.storage.list_projects(status="completed")
        elif self.current_filter == "dormant":
            all_projects = self.storage.list_projects()
            self.projects = [
                p for p in all_projects
                if p.status == "in-progress" and p.days_since_active() > dormant_days
            ]
        else:  # active
            all_projects = self.storage.list_projects()
            self.projects = [
                p for p in all_projects
                if p.status == "in-progress" and p.days_since_active() <= dormant_days
            ]

        # Sort by last_active
        self.projects.sort(key=lambda p: p.last_active, reverse=True)

        # Update the list
        list_view = self.query_one("#project-list", ListView)
        list_view.clear()

        if not self.projects:
            list_view.append(ListItem(Static("[dim]No projects found[/dim]")))
        else:
            for project in self.projects:
                list_view.append(ProjectListItem(project))

    @on(ListView.Selected)
    def on_list_selected(self, event: ListView.Selected) -> None:
        """Handle project selection."""
        if isinstance(event.item, ProjectListItem):
            self.selected_project = event.item.project
            detail = self.query_one("#project-detail", ProjectDetail)
            detail.set_project(self.selected_project)

    def action_filter_active(self) -> None:
        """Filter to show only active projects."""
        self.current_filter = "active"
        self.sub_title = "Filter: Active"
        self.load_projects()

    def action_filter_dormant(self) -> None:
        """Filter to show only dormant projects."""
        self.current_filter = "dormant"
        self.sub_title = "Filter: Dormant"
        self.load_projects()

    def action_filter_completed(self) -> None:
        """Filter to show only completed projects."""
        self.current_filter = "completed"
        self.sub_title = "Filter: Completed"
        self.load_projects()

    def action_filter_archived(self) -> None:
        """Filter to show only archived projects."""
        self.current_filter = "archived"
        self.sub_title = "Filter: Archived"
        self.load_projects()

    def action_filter_all(self) -> None:
        """Show all projects."""
        self.current_filter = "all"
        self.sub_title = "Filter: All"
        self.load_projects()

    def action_refresh(self) -> None:
        """Refresh the project list."""
        self.load_projects()
        self.notify("Projects refreshed")

    def action_mark_done(self) -> None:
        """Mark selected project as done."""
        if self.selected_project:
            if self.selected_project.status == "completed":
                self.notify("Project is already completed", severity="warning")
                return

            # Mark as complete
            self.selected_project.status = "completed"
            self.selected_project.completion = 100
            self.selected_project.last_active = date.today()
            self.storage.move_to_completed(self.selected_project)
            self.storage.update_project_index()

            self.notify(f"✓ Completed: {self.selected_project.name}", severity="information")
            self.action_refresh()
        else:
            self.notify("No project selected", severity="warning")

    def action_archive_project(self) -> None:
        """Archive the selected project."""
        if self.selected_project:
            if self.selected_project.status == "archived":
                self.notify("Project is already archived", severity="warning")
                return

            self.storage.move_to_archived(self.selected_project)
            self.storage.update_project_index()

            self.notify(f"📦 Archived: {self.selected_project.name}", severity="information")
            self.action_refresh()
        else:
            self.notify("No project selected", severity="warning")

    def action_unarchive_project(self) -> None:
        """Unarchive the selected project."""
        if self.selected_project:
            if self.selected_project.status != "archived":
                self.notify("Project is not archived", severity="warning")
                return

            self.storage.unarchive_project(self.selected_project)
            self.storage.update_project_index()

            self.notify(f"▶ Unarchived: {self.selected_project.name}", severity="information")
            self.action_refresh()
        else:
            self.notify("No project selected", severity="warning")

    def action_edit_project(self) -> None:
        """Edit the selected project."""
        if self.selected_project:
            self.notify(f"Use 'jnl edit {self.selected_project.id}' to edit in your editor", severity="information")
        else:
            self.notify("No project selected", severity="warning")


def run_tui(storage: Storage) -> None:
    """Run the TUI application."""
    app = JournelTUI(storage)
    app.run()
