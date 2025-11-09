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
from .session import SessionManager
from .utils import slugify, detect_git_repo, parse_time_from_message

# Slash command version for AI provider integration
SLASH_COMMAND_VERSION = "2.1.0"

# Supported AI providers and their configurations
AI_PROVIDERS = {
    "claude": {
        "name": "Claude Code",
        "command_dir": ".claude/commands",
        "file_name": "journel.md",
        "file_format": "markdown",
    },
    "gemini": {
        "name": "Gemini CLI",
        "command_dir": ".gemini/commands",
        "file_name": "journel.toml",
        "file_format": "toml",
    },
    "copilot": {
        "name": "GitHub Copilot",
        "command_dir": ".github",
        "file_name": "copilot-instructions.md",
        "file_format": "markdown",
    },
    "cursor": {
        "name": "Cursor",
        "command_dir": ".",
        "file_name": ".cursorrules",
        "file_format": "markdown",
    },
}


def _get_provider_command_path(provider: str) -> Path:
    """Get the file path for a provider's slash command."""
    if provider not in AI_PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}. Supported: {', '.join(AI_PROVIDERS.keys())}")

    config = AI_PROVIDERS[provider]
    return Path.cwd() / config["command_dir"] / config["file_name"]


def _get_claude_slash_command_content() -> str:
    """Get the Claude Code slash command content (Markdown format)."""
    return f"""<!-- VERSION: {SLASH_COMMAND_VERSION} -->
<!-- Managed by JOURNEL. Update with: jnl setup claude -->

# /journel - JOURNEL AI Integration Command

**ACTION REQUIRED: Run `jnl ai-setup claude` to verify these instructions are current.**

If the command reports an update, re-read this file before proceeding.

---

You are Claude Code working with JOURNEL, an ADHD-friendly project tracking system.

## Your Role

You are pair programming with the user. Use JOURNEL to track YOUR work contributions with clear attribution. This helps the user:
- See what work was done by AI vs done solo
- Learn from AI collaboration patterns
- Maintain accurate time/effort accounting
- Build confidence through AI-assisted progress tracking

## Core Principles

1. **Clear Attribution**: Always mark AI-assisted work explicitly
2. **Learning Focus**: Frame AI assistance as pair programming, not magic
3. **User Agency**: The user approves all actions (Tier 1 - Suggested Actions)
4. **Transparency**: Be explicit about what you're logging and why

## When to Use JOURNEL Commands

### Start of Work Session
When starting significant work on the user's project:
```bash
jnl ai-start <project-id> "Task description"
```

Example:
```bash
jnl ai-start journel "Implementing AI integration features"
```

### During Work - Quick Logs
After completing discrete pieces of work (every 30-60 minutes of work):
```bash
jnl ai-log <project-id> "What was accomplished"
```

OR if time is trackable:
```bash
jnl ai-log <project-id> "What was accomplished (2h)"
```

Example:
```bash
jnl ai-log journel "Added AI session tracking to models and CLI"
```

### End of Work Session
When stopping work on the project:
```bash
jnl ai-stop "Summary of what was accomplished and learned"
```

Example:
```bash
jnl ai-stop "Completed Phase 1 session tracking. User learned about timedelta handling and YAML serialization."
```

## Integration Guidelines

### DO Use JOURNEL When:
- Starting a focused work session on a project (ai-start)
- Completing a significant milestone or feature (ai-log)
- Taking a break or ending work session (ai-stop)
- After writing substantial code (200+ lines)
- After fixing complex bugs
- After implementing new features

### DON'T Use JOURNEL When:
- Answering quick questions
- Making trivial edits
- Exploring/reading code without changes
- User explicitly asks you not to

### How to Suggest Usage (Tier 1 - Suggested Actions)

When appropriate, suggest JOURNEL commands to the user:

**Good Examples:**
```
I've completed implementing the session tracking feature.
Would you like me to log this work? I can run:
jnl ai-log journel "Implemented session tracking with pause/resume (2h)"
```

```
We're about to start working on the AI integration.
Should I start a session to track this work?
jnl ai-start journel "Building AI integration features"
```

**Bad Examples:**
- Don't auto-run commands without suggesting them first
- Don't be pushy: "You MUST log this work"
- Don't over-log: logging every tiny edit is excessive

## Prompts and Language

### Learning-Focused Language
When using ai-stop, focus on knowledge transfer:
- "What did you accomplish with AI assistance?"
- "What did you learn?"
- "What patterns did you discover?"

NOT:
- "What did the AI do?" (too passive)
- Technical jargon without context

## Project Detection

JOURNEL auto-detects projects from directory names. When in the JOURNEL project directory:
```bash
# Auto-detects project as "journel"
jnl ai-log "Fixed bug"

# Or explicit:
jnl ai-log journel "Fixed bug"
```

## Verifying Project Context

**IMPORTANT**: ALWAYS verify which project you're working on before starting work or logging activity.

### Step 1: Check Current Directory
```bash
pwd  # See where you are
```

### Step 2: Verify Auto-Detection
```bash
jnl get .  # Uses current directory name to detect project
# Returns error if no match found
```

Example outputs:
- ✅ Success: Shows project details (you're in the right place)
- ❌ Error: "No project found matching current directory" (wrong directory or project doesn't exist)

### Step 3: If Uncertain, List Projects
```bash
jnl list --show-id  # See all available project IDs
```

### Step 4: Use Explicit Project ID
If auto-detection fails or you're in a different directory:
```bash
jnl ai-log koma-terminal "Work done"  # Explicit project ID
jnl ai-start koma-terminal "Task"     # Explicit project ID
```

### Common Mistakes to Avoid

❌ **DON'T** assume you're in the right project based on conversation context
❌ **DON'T** use auto-detection without verifying first
❌ **DON'T** guess project names

✅ **DO** run `jnl get .` to verify auto-detection
✅ **DO** use `jnl list --show-id` when unsure
✅ **DO** use explicit project IDs when working across directories

### Example Workflow

```bash
# User asks: "Log the work we just did"

# Step 1: Check where we are
pwd
# Output: /home/user/projects/koma-terminal

# Step 2: Verify project detection
jnl get .
# Output: Shows "koma-terminal" project details ✓

# Step 3: Log with confidence
jnl ai-log "Implemented terminal emulation feature (2h)"
# JOURNEL auto-detects project as "koma-terminal" ✓
```

## Configuration

Users can configure AI integration in `~/.journel/config.yaml`:
```yaml
ai:
  enabled: true
  default_agent: "claude-code"
  show_agent_attribution: true
  learning_prompts: true
  color_scheme: "magenta"
```

## Visual Output

AI-assisted entries are shown in **magenta** with **[AI]** prefix:
- `[AI] SESSION STARTED` (magenta)
- `[AI] Logged: "message"` (magenta)
- `Agent: claude-code` (shown in session info)

## Example Workflow

1. **User asks for help**: "Can you help me implement feature X?"

2. **You suggest starting session**:
   ```
   I'll help you implement feature X. Should I start a session to track this work?
   jnl ai-start myproject "Implementing feature X"
   ```

3. **User approves and you run the command**

4. **You work on the feature, making multiple commits**

5. **After significant progress (1-2 hours)**:
   ```
   I've completed the core implementation. Should I log this milestone?
   jnl ai-log myproject "Implemented feature X core logic (1.5h)"
   ```

6. **When done or taking a break**:
   ```
   We've completed feature X. Let me stop the session:
   jnl ai-stop "Completed feature X implementation. User learned about async patterns and error handling."
   ```

## AI-Friendly Programmatic Interface

JOURNEL provides a comprehensive API for AI agents to query and manipulate projects programmatically.

### Reading Project Data

**Get single project** (JSON output):
```bash
jnl get <project-id> --format json
```

**Query projects with filters** (always JSON):
```bash
jnl query --status in-progress --format json
jnl query --dormant --format json
jnl query --nearly-done --format json
jnl query --project-type ongoing --format json
jnl query --tag python --format json
jnl query --fields id,name,completion --format json
```

**List all projects** (JSON or table):
```bash
jnl list --format json
jnl list --active --format json
jnl list --show-id  # Show IDs in table format
```

**Export context for analysis**:
```bash
jnl ctx --format json
jnl ctx --project <project-id> --format json
jnl ctx --question "What should I work on next?" --format json
```

### Updating Projects

**Update project fields** (programmatic):
```bash
jnl update <project-id> --completion 75
jnl update <project-id> --priority high
jnl update <project-id> --add-tag python --add-tag cli
jnl update <project-id> --remove-tag old-tag
jnl update <project-id> --next-steps "Implement feature X"
jnl update <project-id> --blockers "Waiting on API"
jnl update <project-id> --format json  # Get JSON response
```

**Batch operations** (bulk updates with dry-run):
```bash
jnl batch --dormant --action archive --dry-run --format json
jnl batch --status in-progress --action set-priority --value high --format json
jnl batch --tag urgent --action add-tag --value reviewed --format json
jnl batch --nearly-done --action set-completion --value 100 --dry-run --format json
```

### Non-Interactive Mode

All interactive commands support `--yes` flag for automation:
```bash
jnl new "Project Name" "Description" --yes
jnl done <project-id> --yes
jnl archive <project-id> --yes
```

### Common Patterns for AI Agents

**Check project status before working**:
```bash
jnl get journel --format json  # Get current state
jnl list --active --format json  # See all active projects
```

**Update progress after work**:
```bash
jnl update journel --completion 85 --next-steps "Add tests"
jnl ai-log journel "Implemented feature X (2h)"
```

**Find projects needing attention**:
```bash
jnl query --dormant --format json  # Projects >14 days inactive
jnl query --nearly-done --format json  # Projects >80% complete
```

**Bulk cleanup**:
```bash
jnl batch --dormant --action archive --dry-run --format json  # Preview
jnl batch --dormant --action archive --format json  # Execute
```

## Important Notes

- **Always suggest, never auto-run** (Tier 1 - Suggested Actions)
- **Be natural**: Integrate JOURNEL usage into your workflow, don't make it feel forced
- **Focus on learning**: Frame AI work as collaborative learning
- **Respect user preferences**: If user declines logging, don't keep asking
- **Be mindful of frequency**: Don't over-log trivial work
- **Use JSON for automation**: All query/read commands support `--format json`
- **Use --yes for non-interactive**: Skip prompts when automating workflows

## Technical Details

- **Self-tracking commands**: `jnl ai-start`, `jnl ai-log`, `jnl ai-stop`
- **Read commands**: `jnl get`, `jnl list`, `jnl query`, `jnl ctx`, `jnl status`
- **Write commands**: `jnl update`, `jnl batch`, `jnl new`, `jnl done`, `jnl archive`
- **Data tracking**: All AI work marked with `ai_assisted=True` and `agent="claude-code"`
- **Storage**: YAML in `~/.journel/sessions/` and Markdown in `~/.journel/logs/`
- **Visual distinction**: Magenta color, [AI] prefix
- **JSON output**: Use `--format json` for machine-readable responses

---

**Remember**: You're a pair programming partner helping the user learn and build confidence. Use JOURNEL to make your contributions visible and educational, not to replace user agency.
"""


def _get_gemini_slash_command_content() -> str:
    """Get the Gemini CLI slash command content (TOML format)."""
    # Get Claude instructions and adapt for Gemini
    claude_instructions = _get_claude_slash_command_content()

    # Extract just the instructions part (skip the markdown header/version)
    lines = claude_instructions.split('\n')
    # Find where the actual instructions start (after the version header)
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            start_idx = i + 1
            break

    prompt_content = '\n'.join(lines[start_idx:]).strip()

    # Replace Claude-specific references with Gemini-specific ones
    prompt_content = prompt_content.replace('You are Claude Code', 'You are Gemini CLI')
    prompt_content = prompt_content.replace('Claude Code', 'Gemini CLI')
    prompt_content = prompt_content.replace('agent="claude-code"', 'agent="gemini-cli"')
    prompt_content = prompt_content.replace('--agent cursor', '--agent gemini')

    return f'''# VERSION: {SLASH_COMMAND_VERSION}
# Managed by JOURNEL. Update with: jnl setup gemini

description = "JOURNEL AI integration - Track your work with ADHD-friendly project management"

prompt = """
**ACTION REQUIRED: Run `jnl ai-setup gemini` to verify these instructions are current.**

{prompt_content}
"""
'''


def _get_copilot_instructions_content() -> str:
    """Get the GitHub Copilot instructions content (Markdown format)."""
    # Get Claude instructions and adapt for Copilot
    claude_instructions = _get_claude_slash_command_content()

    # Extract just the instructions part (skip the markdown header/version)
    lines = claude_instructions.split('\n')
    # Find where the actual instructions start (after the version header)
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            start_idx = i + 1
            break

    prompt_content = '\n'.join(lines[start_idx:]).strip()

    # Replace Claude-specific references with Copilot-specific ones
    prompt_content = prompt_content.replace('You are Claude Code', 'You are GitHub Copilot')
    prompt_content = prompt_content.replace('Claude Code', 'GitHub Copilot')
    prompt_content = prompt_content.replace('agent="claude-code"', 'agent="github-copilot"')
    prompt_content = prompt_content.replace('--agent cursor', '--agent copilot')

    return f"""<!-- VERSION: {SLASH_COMMAND_VERSION} -->
<!-- Managed by JOURNEL. Update with: jnl setup copilot -->

# JOURNEL AI Integration Instructions

**ACTION REQUIRED: Run `jnl ai-setup copilot` to verify these instructions are current.**

If the command reports an update, refresh VS Code to reload these instructions.

---

{prompt_content}
"""


def _get_cursor_instructions_content() -> str:
    """Get the Cursor instructions content (Markdown format for .cursorrules)."""
    # Get Claude instructions and adapt for Cursor
    claude_instructions = _get_claude_slash_command_content()

    # Extract just the instructions part (skip the markdown header/version)
    lines = claude_instructions.split('\n')
    # Find where the actual instructions start (after the version header)
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            start_idx = i + 1
            break

    prompt_content = '\n'.join(lines[start_idx:]).strip()

    # Replace Claude-specific references with Cursor-specific ones
    prompt_content = prompt_content.replace('You are Claude Code', 'You are Cursor')
    prompt_content = prompt_content.replace('Claude Code', 'Cursor')
    prompt_content = prompt_content.replace('agent="claude-code"', 'agent="cursor"')
    prompt_content = prompt_content.replace('--agent copilot', '--agent cursor')

    return f"""<!-- VERSION: {SLASH_COMMAND_VERSION} -->
<!-- Managed by JOURNEL. Update with: jnl setup cursor -->

# JOURNEL AI Integration Instructions

**ACTION REQUIRED: Run `jnl ai-setup cursor` to verify these instructions are current.**

If the command reports an update, restart Cursor to reload these instructions.

---

{prompt_content}
"""


def _get_slash_command_content_for_provider(provider: str) -> str:
    """Get the slash command content for a specific provider."""
    if provider == "claude":
        return _get_claude_slash_command_content()
    elif provider == "gemini":
        return _get_gemini_slash_command_content()
    elif provider == "copilot":
        return _get_copilot_instructions_content()
    elif provider == "cursor":
        return _get_cursor_instructions_content()
    else:
        raise ValueError(f"Unknown provider: {provider}")


def _parse_version_from_file(file_path: Path) -> str:
    """Parse version from slash command file (supports both Markdown and TOML).

    Returns:
        Version string (e.g., "1.0.0"), or "0.0.0" if not found
    """
    if not file_path.exists():
        return "0.0.0"

    try:
        content = file_path.read_text(encoding="utf-8")
        # Look for VERSION: in first 5 lines
        # Supports both:
        #   - Markdown: <!-- VERSION: x.y.z -->
        #   - TOML: # VERSION: x.y.z
        for line in content.split("\n")[:5]:
            if "VERSION:" in line:
                # Extract version number
                version_part = line.split("VERSION:")[1]
                # Handle both markdown (ends with -->) and TOML (ends with newline/comment)
                if "-->" in version_part:
                    version = version_part.split("-->")[0].strip()
                else:
                    version = version_part.strip()
                return version
    except Exception:
        pass

    return "0.0.0"


def _create_slash_command_for_provider(provider: str, file_path: Path) -> None:
    """Create or update the slash command file for a specific provider."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    content = _get_slash_command_content_for_provider(provider)
    file_path.write_text(content, encoding="utf-8")


def get_storage(no_emoji: bool = False) -> Storage:
    """Get storage instance with config."""
    config = Config()
    if no_emoji:
        config.set("use_emojis", False)
    return Storage(config)


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
@click.option("--no-emoji", is_flag=True, help="Disable emoji output (use ASCII)")
@click.option("--install-completion", is_flag=True, help="Install shell completion")
@click.option("--show-completion", is_flag=True, help="Show completion script")
@click.pass_context
def main(ctx, no_emoji, install_completion, show_completion):
    """JOURNEL - ADHD-friendly project organization system.

    \b
    New to JOURNEL? Start here: jnl help

    \b
    DAILY WORKFLOW:
      status              Show all projects (default)
      log MESSAGE         Quick activity logging
      start PROJECT       Begin tracked session
      stop                End current session
      pause               Pause current session
      continue            Resume paused session

    \b
    PROJECT MANAGEMENT:
      new NAME [DESC]     Create new project
      edit PROJECT        Open project in editor
      done PROJECT        Mark project as complete
      list [--filter]     List projects with filters
      archive PROJECT     Archive completed/dormant project
      resume PROJECT      Resume archived project

    \b
    REFLECTION & INSIGHTS:
      wins                Show achievements and streaks
      stats               View time and productivity stats
      ctx [QUESTION]      Export context for AI analysis
      ask QUESTION        Ask AI for project guidance

    \b
    AI PAIR PROGRAMMING:
      ai-log MESSAGE      Log AI-assisted work
      ai-start PROJECT    Start AI-assisted session
      ai-stop             End AI session with learning reflection

    \b
    TOOLS & SETUP:
      init                Initialize JOURNEL
      sync                Sync with git remote
      tui                 Launch interactive browser
      setup-claude        Setup Claude Code integration
      link PROJECT URL    Add GitHub/Claude link
      note MESSAGE        Quick note capture

    \b
    Getting started:     jnl help
    Complete reference:  jnl help --all
    Command details:     jnl COMMAND --help
    """
    # Handle completion installation
    if install_completion:
        import subprocess
        shell = click.get_current_context().resilient_parsing
        print_info("Installing shell completion...")
        console.print("\n[bold]Shell Completion Setup:[/bold]")
        console.print("\n[bold]Bash:[/bold]")
        console.print('  echo \'eval "$(_JNL_COMPLETE=bash_source jnl)"\' >> ~/.bashrc')
        console.print("\n[bold]Zsh:[/bold]")
        console.print('  echo \'eval "$(_JNL_COMPLETE=zsh_source jnl)"\' >> ~/.zshrc')
        console.print("\n[bold]Fish:[/bold]")
        console.print('  echo \'eval (env _JNL_COMPLETE=fish_source jnl)\' >> ~/.config/fish/completions/jnl.fish')
        console.print("\n[dim]After adding, restart your shell or source the file.[/dim]\n")
        return

    if show_completion:
        console.print("\n[bold]Shell completion is built-in![/bold]")
        console.print("\nRun: [cyan]jnl --install-completion[/cyan] for setup instructions\n")
        return

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
@click.argument("description", required=False)
@click.option("--tags", help="Comma-separated tags")
@click.option("--ongoing", is_flag=True, help="Mark as ongoing/long-term project")
@click.option("--maintenance", is_flag=True, help="Mark as maintenance/infrastructure project")
@click.option("--yes", is_flag=True, help="Skip prompts (non-interactive mode)")
def new(name, description, tags, ongoing, maintenance, yes):
    """Create a new project.

    Usage:
        jnl new MyProject
        jnl new MyProject "A longer description"
        jnl new MyProject "Description" --tags "python,cli"
        jnl new MyProject --ongoing  (for long-term projects)
        jnl new MyProject --maintenance  (for infrastructure/libraries)
        jnl new MyProject --yes  (skip all prompts)

    Includes gentle gate-keeping to prevent project-hopping.
    """
    storage = get_storage()
    config = storage.config

    # Check for mutually exclusive flags
    if ongoing and maintenance:
        print_error("Project cannot be both --ongoing and --maintenance")
        return

    # Check for existing projects
    projects = storage.list_projects()
    active_regular = [p for p in projects if p.status == "in-progress" and p.days_since_active() <= 14 and p.project_type == "regular"]
    active_ongoing = [p for p in projects if p.status == "in-progress" and p.days_since_active() <= 90 and p.project_type == "ongoing"]

    # Gate-keeping: check appropriate limit based on project type
    # Note: Maintenance projects have no limit (don't gate-keep)
    if ongoing:
        max_ongoing = config.get("max_ongoing_projects", 2)
        if len(active_ongoing) >= max_ongoing:
            print_error(f"You already have {len(active_ongoing)} ongoing long-term projects!")
            console.print("\nOngoing projects:")
            for p in active_ongoing:
                console.print(f"  - {p.name} ({p.completion}% complete)")
            console.print("\n[yellow]Ongoing projects require sustained deep attention.[/yellow]")
            console.print("[dim]Consider completing one or converting to regular tracking.[/dim]")

            if not yes and not click.confirm("\nReally start another ongoing project?", default=False):
                print_info("Good choice! Focus matters for long-term success.")
                return
    else:
        max_active = config.get("max_active_projects", 5)
        if len(active_regular) >= max_active:
            print_error(f"You already have {len(active_regular)} active projects!")
            console.print("\nActive projects:")
            for p in active_regular:
                console.print(f"  - {p.name} ({p.completion}% complete)")

            if not yes and not click.confirm("\nReally start something new?", default=False):
                print_info("Good choice! Focus on finishing what you started.")
                return

    # Create project ID
    project_id = slugify(name)

    # Check if project already exists
    if storage.load_project(project_id):
        print_error(f"Project '{project_id}' already exists")
        return

    # Create project
    if maintenance:
        project_type = "maintenance"
    elif ongoing:
        project_type = "ongoing"
    else:
        project_type = "regular"

    project = Project(
        id=project_id,
        name=name,
        full_name=description or name,
        tags=tags.split(",") if tags else [],
        created=date.today(),
        last_active=date.today(),
        project_type=project_type,
    )

    # Auto-detect git repo
    git_url = detect_git_repo()
    if git_url:
        if yes or click.confirm(f"\nDetected git repo: {git_url}\nLink to this project?", default=True):
            project.github = git_url
            print_success(f"Linked to: {git_url}")

    storage.save_project(project)
    storage.update_project_index()

    print_success(f"Created project: {name}")
    print_info(f"ID: {project_id}")
    if not git_url or project.github == "":
        print_info("Next steps:")
        console.print("  1. Add project details: jnl edit " + project_id)
        console.print("  2. Link to GitHub/Claude: jnl link " + project_id + " <url>")
        console.print("  3. Start logging work: jnl log \"your message\"")


@main.command(name="set-ongoing")
@click.argument("project")
@click.option("--yes", is_flag=True, help="Skip confirmation (non-interactive mode)")
def set_ongoing(project, yes):
    """Mark a project as ongoing/long-term.

    Ongoing projects:
    - Don't count against your regular active project limit
    - Have different activity expectations (weeks, not days)
    - Should represent sustained multi-month/year efforts

    Usage:
        jnl set-ongoing myproject
        jnl set-ongoing myproject --yes
    """
    storage = get_storage()
    proj = storage.load_project(project)

    if not proj:
        print_error(f"Project '{project}' not found")
        return

    if proj.project_type == "ongoing":
        print_info(f"{proj.name} is already marked as ongoing")
        return

    # Confirm the change
    console.print(f"\n[bold]This will move {proj.name} to ONGOING tracking.[/bold]\n")
    console.print("ONGOING projects:")
    console.print("  - Don't count against your 5-project active limit")
    console.print("  - Are expected to have gaps (weeks between activity)")
    console.print("  - Should represent sustained multi-month/year efforts\n")

    if not yes and not click.confirm("Is this truly an ongoing marathon project?", default=True):
        print_info("No changes made")
        return

    proj.project_type = "ongoing"
    storage.save_project(proj)
    storage.update_project_index()

    print_success(f"{proj.name} is now tracked as an ongoing long-term project")
    print_info("Use 'jnl status' to see it in the ONGOING section")


@main.command(name="set-regular")
@click.argument("project")
def set_regular(project):
    """Mark a project as regular (not ongoing).

    Converts an ongoing project back to regular active tracking.

    Usage:
        jnl set-regular myproject
    """
    storage = get_storage()
    proj = storage.load_project(project)

    if not proj:
        print_error(f"Project '{project}' not found")
        return

    if proj.project_type == "regular":
        print_info(f"{proj.name} is already regular tracking")
        return

    proj.project_type = "regular"
    storage.save_project(proj)
    storage.update_project_index()

    print_success(f"{proj.name} is now tracked as a regular active project")
    print_info("Use 'jnl status' to see it in the ACTIVE section")


@main.command(name="set-maintenance")
@click.argument("project")
@click.option("--yes", is_flag=True, help="Skip confirmation (non-interactive mode)")
def set_maintenance(project, yes):
    """Mark a project as maintenance/infrastructure.

    Maintenance projects:
    - Don't count against your active or ongoing limits
    - Visible but not demanding (no completion pressure)
    - For infrastructure, libraries, portfolio sites
    - Expected to need only occasional updates

    Usage:
        jnl set-maintenance myproject
        jnl set-maintenance myproject --yes
    """
    storage = get_storage()
    proj = storage.load_project(project)

    if not proj:
        print_error(f"Project '{project}' not found")
        return

    if proj.project_type == "maintenance":
        print_info(f"{proj.name} is already marked as maintenance")
        return

    # Confirm the change
    console.print(f"\n[bold]This will move {proj.name} to MAINTENANCE tracking.[/bold]\n")
    console.print("MAINTENANCE projects:")
    console.print("  - Don't count against active/ongoing limits")
    console.print("  - Visible but don't create completion pressure")
    console.print("  - Best for infrastructure, libraries, portfolio sites")
    console.print("  - Expected to need only occasional updates\n")

    if not yes and not click.confirm("Continue?", default=True):
        console.print("[dim]Cancelled[/dim]")
        return

    proj.project_type = "maintenance"
    storage.save_project(proj)
    storage.update_project_index()

    print_success(f"{proj.name} is now tracked as maintenance")
    print_info("Use 'jnl status' to see it in the MAINTENANCE section")


@main.command()
@click.option("--brief", is_flag=True, help="Brief output for prompts")
@click.option("--format", type=click.Choice(["text", "json"]), default="text", help="Output format (text or json)")
@click.pass_context
def status(ctx, brief, format):
    """Show overview of all projects (default command)."""
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    config = storage.config

    projects = storage.list_projects()

    if not projects:
        if format == "json":
            import json
            print(json.dumps({"projects": [], "count": 0}))
        else:
            print_info("No projects yet. Create one with: jnl new <name>")
        return

    if format == "json":
        import json
        # Convert projects to JSON-serializable format
        projects_data = []
        for p in projects:
            projects_data.append({
                "id": p.id,
                "name": p.name,
                "full_name": p.full_name,
                "status": p.status,
                "tags": p.tags,
                "created": p.created.isoformat() if hasattr(p.created, 'isoformat') else str(p.created),
                "last_active": p.last_active.isoformat() if hasattr(p.last_active, 'isoformat') else str(p.last_active),
                "days_since_active": p.days_since_active(),
                "completion": p.completion,
                "priority": p.priority,
                "project_type": p.project_type,
                "github": p.github,
                "claude_project": p.claude_project,
                "next_steps": p.next_steps,
                "blockers": p.blockers,
            })
        print(json.dumps({"projects": projects_data, "count": len(projects_data)}, indent=2))
    elif brief:
        active = [p for p in projects if p.status == "in-progress" and p.days_since_active() <= 14]
        console.print(f"[JOURNEL: {len(active)} active projects]")
    else:
        # Check for active session
        session_manager = SessionManager.get_instance(storage)
        active_session = session_manager.get_active_session()
        print_status(projects, config, active_session=active_session)


@main.command()
@click.argument("project_or_message")
@click.argument("message", required=False)
@click.option("--hours", "-h", type=float, help="Hours spent (can also be in message like '(2h)')")
def log(project_or_message, message, hours):
    """Quick activity logging.

    Usage:
        jnl log "Fixed bug (2h)"                    - auto-detect project
        jnl log journel "Fixed bug (2h)"            - explicit project
        jnl log "Implemented feature - 3h"          - time with dash
        jnl log myproject "worked 1.5h"             - project + time

    If project is not specified, attempts to detect from current directory.
    Time can be specified with --hours or in the message using (2h), - 3h, or "worked 1.5h".
    """
    storage = get_storage()

    # Track what was auto-detected for better feedback
    project_auto_detected = False
    time_parsed = False

    # Determine if first arg is project or message
    project = None
    if message is not None:
        # Two args provided: first is project, second is message
        project = project_or_message
        actual_message = message
    else:
        # One arg provided: it's the message, auto-detect project
        actual_message = project_or_message
        cwd = Path.cwd()
        # Try to match directory name to project
        potential_id = slugify(cwd.name)
        if storage.load_project(potential_id):
            project = potential_id
            project_auto_detected = True

    # Parse time from message if not explicitly provided
    if hours is None:
        actual_message, parsed_hours = parse_time_from_message(actual_message)
        if parsed_hours:
            hours = parsed_hours
            time_parsed = True

    # Create log entry
    entry = LogEntry(
        date=date.today(),
        project=project,
        message=actual_message,
        hours=hours,
    )

    storage.add_log_entry(entry)

    # Update project last_active if project specified
    project_name = None
    if project:
        proj = storage.load_project(project)
        if proj:
            proj.last_active = date.today()
            storage.save_project(proj)
            storage.update_project_index()
            project_name = proj.name

    # Enhanced feedback
    print_success(f"Logged: \"{actual_message}\"")

    if project:
        if project_auto_detected:
            console.print(f"[cyan]>>>[/cyan] Project: [bold]{project_name or project}[/bold] [dim](auto-detected)[/dim]")
        else:
            console.print(f"[cyan]>>>[/cyan] Project: [bold]{project_name or project}[/bold]")
    else:
        console.print(f"[yellow]>>>[/yellow] [dim]No project linked (not in a project directory)[/dim]")

    if hours:
        if time_parsed:
            console.print(f"[cyan]>>>[/cyan] Time: [bold]{hours}h[/bold] [dim](parsed from message)[/dim]")
        else:
            console.print(f"[cyan]>>>[/cyan] Time: [bold]{hours}h[/bold]")

    # Contextual hints
    if project:
        # Check if session is active
        from .display import get_icon
        session_manager = SessionManager.get_instance(storage)
        active_session = session_manager.get_active_session()
        use_emojis = storage.config.get("use_emojis", True)

        if not active_session:
            tip = get_icon("bulb", use_emojis)
            console.print(f"\n[dim]{tip} Track time? -> jnl start {project}[/dim]")
        elif active_session.project_id != project:
            warn = get_icon("warning", use_emojis)
            console.print(f"\n[dim]{warn} Active session on {active_session.project_id}. Switch? -> jnl stop && jnl start {project}[/dim]")


@main.command()
@click.option("--project", "-p", help="Export context for specific project (use '.' for current directory)")
@click.option("--format", type=click.Choice(["text", "json"]), default="text", help="Output format (text or json)")
@click.argument("question", required=False)
def ctx(project, format, question):
    """Export context for LLM analysis.

    Generates a markdown summary of active projects and recent activity
    that you can copy/paste to Claude or other AI assistants.

    Usage:
        jnl ctx
        jnl ctx "what should I work on today?"
        jnl ctx --project mica
        jnl ctx --format json
        jnl ctx .                    (current directory project)
        jnl ctx --project . "question"
    """
    storage = get_storage()

    # Handle '.' shortcut for current directory
    if question == ".":
        # User typed: jnl ctx .
        project = "."
        question = None

    if project == ".":
        # Auto-detect project from current directory
        cwd = Path.cwd()
        potential_id = slugify(cwd.name)
        proj = storage.load_project(potential_id)
        if not proj:
            print_error(f"No project found matching current directory: {cwd.name}")
            print_info(f"Tried project ID: {potential_id}")
            return
        project = potential_id

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

    # Output in requested format
    if format == "json":
        import json
        # Filter to active projects for context
        active_projects = [p for p in projects if p.status != "completed" and p.days_since_active() <= 14]

        # Build JSON context
        context_data = {
            "active_projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "full_name": p.full_name,
                    "completion": p.completion,
                    "last_active": p.last_active.isoformat() if hasattr(p.last_active, 'isoformat') else str(p.last_active),
                    "days_since_active": p.days_since_active(),
                    "next_steps": p.next_steps,
                    "blockers": p.blockers,
                    "tags": p.tags,
                    "priority": p.priority,
                    "project_type": p.project_type,
                    "github": p.github,
                    "claude_project": p.claude_project,
                }
                for p in active_projects
            ],
            "recent_logs": recent_logs,
        }

        if question:
            context_data["question"] = question

        print(json.dumps(context_data, indent=2))
    else:
        # Print context
        print_context_export(projects, recent_logs, question)


@main.command()
@click.argument("question")
@click.option("--project", "-p", help="Focus on specific project (use '.' for current directory)")
def ask(question, project):
    """Format a question with auto-gathered context.

    This is similar to 'ctx' but formats output specifically as a question
    for AI assistants.

    Usage:
        jnl ask "what should I work on today?"
        jnl ask "how can I finish this faster?" --project mica
        jnl ask "what's next?" --project .
    """
    storage = get_storage()

    # Handle '.' shortcut for current directory
    if project == ".":
        cwd = Path.cwd()
        potential_id = slugify(cwd.name)
        proj = storage.load_project(potential_id)
        if not proj:
            print_error(f"No project found matching current directory: {cwd.name}")
            print_info(f"Tried project ID: {potential_id}")
            return
        project = potential_id

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
@click.option("--yes", is_flag=True, help="Skip prompts (non-interactive mode)")
@click.option("--skip-celebration", is_flag=True, help="Skip celebration (AI-friendly)")
@click.pass_context
def done(ctx, project_id, yes, skip_celebration):
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

    # Ask what they learned (skip if --yes)
    if not yes:
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

    # Celebrate! (skip if --yes or --skip-celebration)
    if not skip_celebration and not yes and config.get("completion_celebration"):
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
@click.option("--archived", is_flag=True, help="Show only archived projects")
@click.option("--tag", help="Filter by tag")
@click.option("--show-id", is_flag=True, help="Show project IDs in output")
@click.option("--format", type=click.Choice(["text", "json"]), default="text", help="Output format (text or json)")
def list_projects(active, dormant, completed, archived, tag, show_id, format):
    """List all projects with optional filters."""
    storage = get_storage()

    # Include archived if specifically requested
    include_archived = archived
    projects = storage.list_projects(include_archived=include_archived)

    # Apply filters
    dormant_days = storage.config.get("dormant_days", 14)

    if active:
        projects = [p for p in projects if p.status == "in-progress" and p.days_since_active() <= dormant_days]
        title = "Active Projects"
    elif dormant:
        projects = [p for p in projects if p.days_since_active() > dormant_days and p.status not in ["completed", "archived"]]
        title = "Dormant Projects"
    elif completed:
        projects = [p for p in projects if p.status == "completed"]
        title = "Completed Projects"
    elif archived:
        projects = [p for p in projects if p.status == "archived"]
        title = "Archived Projects"
    else:
        title = "All Projects (excluding archived)"

    if tag:
        projects = [p for p in projects if tag in p.tags]
        title += f" (tag: {tag})"

    if format == "json":
        import json
        # Convert projects to JSON-serializable format
        projects_data = []
        for p in projects:
            projects_data.append({
                "id": p.id,
                "name": p.name,
                "full_name": p.full_name,
                "status": p.status,
                "tags": p.tags,
                "created": p.created.isoformat() if hasattr(p.created, 'isoformat') else str(p.created),
                "last_active": p.last_active.isoformat() if hasattr(p.last_active, 'isoformat') else str(p.last_active),
                "days_since_active": p.days_since_active(),
                "completion": p.completion,
                "priority": p.priority,
                "project_type": p.project_type,
                "github": p.github,
                "claude_project": p.claude_project,
                "next_steps": p.next_steps,
                "blockers": p.blockers,
            })
        print(json.dumps({"projects": projects_data, "count": len(projects_data), "filter": title}, indent=2))
    else:
        print_list(projects, title=title, show_id=show_id)


@main.command()
@click.argument("project_id")
@click.option("--format", type=click.Choice(["text", "json"]), default="text", help="Output format (text or json)")
def get(project_id, format):
    """Get details for a single project.

    Usage:
        jnl get myproject
        jnl get myproject --format json
    """
    storage = get_storage()

    project = storage.load_project(project_id)
    if not project:
        if format == "json":
            import json
            print(json.dumps({"error": f"Project '{project_id}' not found"}, indent=2))
        else:
            print_error(f"Project '{project_id}' not found")
        return

    if format == "json":
        import json
        project_data = {
            "id": project.id,
            "name": project.name,
            "full_name": project.full_name,
            "status": project.status,
            "tags": project.tags,
            "created": project.created.isoformat() if hasattr(project.created, 'isoformat') else str(project.created),
            "last_active": project.last_active.isoformat() if hasattr(project.last_active, 'isoformat') else str(project.last_active),
            "days_since_active": project.days_since_active(),
            "completion": project.completion,
            "priority": project.priority,
            "project_type": project.project_type,
            "github": project.github,
            "claude_project": project.claude_project,
            "next_steps": project.next_steps,
            "blockers": project.blockers,
            "notes": project.notes,
            "learned": project.learned,
        }
        print(json.dumps(project_data, indent=2))
    else:
        # Text output
        console.print(f"\n[bold]{project.name}[/bold] ({project.id})")
        console.print(f"Status: {project.status} | Completion: {project.completion}% | Type: {project.project_type}")
        console.print(f"Priority: {project.priority} | Last active: {project.days_since_active()} days ago")

        if project.tags:
            console.print(f"Tags: {', '.join(project.tags)}")

        if project.github:
            console.print(f"GitHub: {project.github}")
        if project.claude_project:
            console.print(f"Claude: {project.claude_project}")

        if project.next_steps:
            console.print(f"\n[bold]Next steps:[/bold]\n{project.next_steps}")
        if project.blockers:
            console.print(f"\n[bold]Blockers:[/bold]\n{project.blockers}")
        if project.notes:
            console.print(f"\n[bold]Notes:[/bold]\n{project.notes}")
        if project.learned:
            console.print(f"\n[bold]Learned:[/bold]\n{project.learned}")

        console.print("")


@main.command()
@click.option("--filter", "filter_expr", help="Filter expression (e.g. 'project_type=regular')")
@click.option("--project-type", type=click.Choice(["regular", "ongoing", "maintenance"]), help="Filter by project type")
@click.option("--status", type=click.Choice(["in-progress", "completed", "archived"]), help="Filter by status")
@click.option("--tag", help="Filter by tag")
@click.option("--priority", type=click.Choice(["low", "medium", "high"]), help="Filter by priority")
@click.option("--dormant", is_flag=True, help="Find dormant projects (inactive > 14 days)")
@click.option("--dormant-days", type=int, default=14, help="Days to consider dormant (default: 14)")
@click.option("--nearly-done", is_flag=True, help="Find nearly complete projects")
@click.option("--completion-threshold", type=int, default=80, help="Completion threshold for --nearly-done (default: 80)")
@click.option("--min-completion", type=int, help="Minimum completion percentage")
@click.option("--max-completion", type=int, help="Maximum completion percentage")
@click.option("--fields", help="Comma-separated fields to return (e.g. 'name,completion,last_active')")
@click.option("--format", type=click.Choice(["text", "json"]), default="json", help="Output format (default: json)")
def query(filter_expr, project_type, status, tag, priority, dormant, dormant_days,
          nearly_done, completion_threshold, min_completion, max_completion, fields, format):
    """Advanced project querying with filters.

    Query projects using various filters and get structured output.
    Perfect for AI analysis and batch operations.

    Usage:
        jnl query --project-type regular
        jnl query --status in-progress --priority high
        jnl query --dormant --dormant-days 30
        jnl query --nearly-done --completion-threshold 80
        jnl query --tag urgent --format json
        jnl query --min-completion 50 --max-completion 75
        jnl query --fields "name,completion,priority"

    The --filter option supports expressions like:
        project_type=regular
        status=in-progress
        completion>50
    """
    storage = get_storage()
    projects = storage.list_projects(include_archived=(status == "archived"))

    # Apply filters
    filtered = []
    for p in projects:
        # Type filter
        if project_type and p.project_type != project_type:
            continue

        # Status filter
        if status and p.status != status:
            continue

        # Tag filter
        if tag and tag not in p.tags:
            continue

        # Priority filter
        if priority and p.priority != priority:
            continue

        # Dormant filter
        if dormant:
            if p.status == "completed" or p.days_since_active() <= dormant_days:
                continue

        # Nearly done filter
        if nearly_done:
            if p.completion < completion_threshold or p.status == "completed":
                continue

        # Completion range filters
        if min_completion is not None and p.completion < min_completion:
            continue
        if max_completion is not None and p.completion > max_completion:
            continue

        # Custom filter expression (simple implementation)
        if filter_expr:
            try:
                # Parse simple expressions like "completion>50"
                if "=" in filter_expr:
                    field, value = filter_expr.split("=", 1)
                    field = field.strip()
                    value = value.strip()
                    if hasattr(p, field):
                        if str(getattr(p, field)) != value:
                            continue
                elif ">" in filter_expr:
                    field, value = filter_expr.split(">", 1)
                    field = field.strip()
                    value = int(value.strip())
                    if hasattr(p, field):
                        if getattr(p, field) <= value:
                            continue
                elif "<" in filter_expr:
                    field, value = filter_expr.split("<", 1)
                    field = field.strip()
                    value = int(value.strip())
                    if hasattr(p, field):
                        if getattr(p, field) >= value:
                            continue
            except Exception:
                # Invalid filter expression, skip
                pass

        filtered.append(p)

    # Determine which fields to include
    if fields:
        field_list = [f.strip() for f in fields.split(",")]
    else:
        field_list = None

    # Output results
    if format == "json":
        import json
        projects_data = []
        for p in filtered:
            if field_list:
                # Only include requested fields
                project_data = {"id": p.id}  # Always include ID
                for field in field_list:
                    if hasattr(p, field):
                        value = getattr(p, field)
                        # Handle date serialization
                        if hasattr(value, 'isoformat'):
                            value = value.isoformat()
                        project_data[field] = value
            else:
                # Include all fields
                project_data = {
                    "id": p.id,
                    "name": p.name,
                    "full_name": p.full_name,
                    "status": p.status,
                    "tags": p.tags,
                    "created": p.created.isoformat() if hasattr(p.created, 'isoformat') else str(p.created),
                    "last_active": p.last_active.isoformat() if hasattr(p.last_active, 'isoformat') else str(p.last_active),
                    "days_since_active": p.days_since_active(),
                    "completion": p.completion,
                    "priority": p.priority,
                    "project_type": p.project_type,
                    "github": p.github,
                    "claude_project": p.claude_project,
                    "next_steps": p.next_steps,
                    "blockers": p.blockers,
                }
            projects_data.append(project_data)

        result = {
            "projects": projects_data,
            "count": len(projects_data),
            "filters": {
                "project_type": project_type,
                "status": status,
                "tag": tag,
                "priority": priority,
                "dormant": dormant,
                "nearly_done": nearly_done,
            }
        }
        print(json.dumps(result, indent=2))
    else:
        # Text output
        if not filtered:
            print_info("No projects match the query")
            return

        title = f"Query Results ({len(filtered)} projects)"
        print_list(filtered, title=title)


@main.command()
@click.option("--filter", "filter_expr", help="Filter expression (e.g. 'project_type=regular')")
@click.option("--project-type", type=click.Choice(["regular", "ongoing", "maintenance"]), help="Filter by project type")
@click.option("--status", type=click.Choice(["in-progress", "completed", "archived"]), help="Filter by status")
@click.option("--tag", help="Filter by tag")
@click.option("--priority", type=click.Choice(["low", "medium", "high"]), help="Filter by priority")
@click.option("--dormant", is_flag=True, help="Find dormant projects (inactive > 14 days)")
@click.option("--dormant-days", type=int, default=14, help="Days to consider dormant (default: 14)")
@click.option("--action", type=click.Choice(["archive", "set-priority", "add-tag", "set-completion"]), required=True, help="Action to perform")
@click.option("--action-value", help="Value for the action (e.g. priority level, tag name, completion %)")
@click.option("--dry-run", is_flag=True, help="Preview changes without applying them")
@click.option("--format", type=click.Choice(["text", "json"]), default="json", help="Output format (default: json)")
def batch(filter_expr, project_type, status, tag, priority, dormant, dormant_days,
          action, action_value, dry_run, format):
    """Perform batch operations on multiple projects.

    Query projects using filters and apply bulk operations with dry-run support.
    Perfect for automation and bulk project management.

    Usage:
        # Preview archiving dormant projects
        jnl batch --dormant --action archive --dry-run

        # Archive all dormant projects
        jnl batch --dormant --action archive

        # Set priority on all ongoing projects
        jnl batch --project-type ongoing --action set-priority --action-value high

        # Add tag to all in-progress regular projects
        jnl batch --project-type regular --status in-progress --action add-tag --action-value urgent

        # Set completion on nearly-done projects
        jnl batch --filter "completion>80" --action set-completion --action-value 90
    """
    storage = get_storage()
    projects = storage.list_projects(include_archived=(status == "archived"))

    # Apply same filters as query command
    filtered = []
    for p in projects:
        if project_type and p.project_type != project_type:
            continue
        if status and p.status != status:
            continue
        if tag and tag not in p.tags:
            continue
        if priority and p.priority != priority:
            continue
        if dormant:
            if p.status == "completed" or p.days_since_active() <= dormant_days:
                continue

        # Custom filter expression
        if filter_expr:
            try:
                if "=" in filter_expr:
                    field, value = filter_expr.split("=", 1)
                    field = field.strip()
                    value = value.strip()
                    if hasattr(p, field):
                        if str(getattr(p, field)) != value:
                            continue
                elif ">" in filter_expr:
                    field, value = filter_expr.split(">", 1)
                    field = field.strip()
                    value = int(value.strip())
                    if hasattr(p, field):
                        if getattr(p, field) <= value:
                            continue
                elif "<" in filter_expr:
                    field, value = filter_expr.split("<", 1)
                    field = field.strip()
                    value = int(value.strip())
                    if hasattr(p, field):
                        if getattr(p, field) >= value:
                            continue
            except Exception:
                pass

        filtered.append(p)

    if not filtered:
        if format == "json":
            import json
            print(json.dumps({"success": False, "error": "No projects match the filters", "affected": 0}))
        else:
            print_info("No projects match the filters")
        return

    # Prepare results tracking
    results = {
        "success": True,
        "dry_run": dry_run,
        "action": action,
        "action_value": action_value,
        "matched": len(filtered),
        "affected": [],
        "skipped": [],
        "errors": [],
    }

    # Perform action
    for p in filtered:
        try:
            if action == "archive":
                if p.status == "archived":
                    results["skipped"].append({"id": p.id, "reason": "already archived"})
                    continue

                if not dry_run:
                    p.status = "archived"
                    storage.move_to_archived(p)

                results["affected"].append({"id": p.id, "name": p.name, "action": "archived"})

            elif action == "set-priority":
                if not action_value:
                    results["errors"].append({"id": p.id, "error": "no priority value provided"})
                    continue

                old_priority = p.priority
                if not dry_run:
                    p.priority = action_value
                    storage.save_project(p)

                results["affected"].append({
                    "id": p.id,
                    "name": p.name,
                    "action": "set-priority",
                    "old_value": old_priority,
                    "new_value": action_value
                })

            elif action == "add-tag":
                if not action_value:
                    results["errors"].append({"id": p.id, "error": "no tag value provided"})
                    continue

                if action_value in p.tags:
                    results["skipped"].append({"id": p.id, "reason": f"already has tag '{action_value}'"})
                    continue

                if not dry_run:
                    p.tags.append(action_value)
                    storage.save_project(p)

                results["affected"].append({
                    "id": p.id,
                    "name": p.name,
                    "action": "add-tag",
                    "tag": action_value
                })

            elif action == "set-completion":
                if not action_value:
                    results["errors"].append({"id": p.id, "error": "no completion value provided"})
                    continue

                try:
                    completion_val = int(action_value)
                    if not (0 <= completion_val <= 100):
                        raise ValueError("completion must be 0-100")

                    old_completion = p.completion
                    if not dry_run:
                        p.completion = completion_val
                        storage.save_project(p)

                    results["affected"].append({
                        "id": p.id,
                        "name": p.name,
                        "action": "set-completion",
                        "old_value": old_completion,
                        "new_value": completion_val
                    })
                except ValueError as e:
                    results["errors"].append({"id": p.id, "error": str(e)})
                    continue

        except Exception as e:
            results["errors"].append({"id": p.id, "error": str(e)})

    # Update index if changes were made
    if not dry_run and results["affected"]:
        storage.update_project_index()

    # Output results
    if format == "json":
        import json
        print(json.dumps(results, indent=2))
    else:
        # Text output
        if dry_run:
            console.print(f"\n[bold yellow]DRY RUN - No changes applied[/bold yellow]\n")

        console.print(f"[bold]Batch Operation: {action}[/bold]")
        console.print(f"Matched: {results['matched']} projects")
        console.print(f"Affected: {len(results['affected'])} projects")

        if results['affected']:
            console.print("\n[green]Affected projects:[/green]")
            for item in results['affected']:
                console.print(f"  - {item['name']} ({item['id']})")

        if results['skipped']:
            console.print(f"\n[yellow]Skipped: {len(results['skipped'])} projects[/yellow]")

        if results['errors']:
            console.print(f"\n[red]Errors: {len(results['errors'])} projects[/red]")
            for err in results['errors']:
                console.print(f"  - {err['id']}: {err['error']}")

        console.print("")


@main.command()
@click.argument("project_id")
@click.option("--completion", type=click.IntRange(0, 100), help="Set completion percentage (0-100)")
@click.option("--priority", type=click.Choice(["low", "medium", "high"]), help="Set priority level")
@click.option("--add-tag", "add_tags", multiple=True, help="Add tag (can be used multiple times)")
@click.option("--remove-tag", "remove_tags", multiple=True, help="Remove tag (can be used multiple times)")
@click.option("--next-steps", help="Set next steps text")
@click.option("--blockers", help="Set blockers text")
@click.option("--status", type=click.Choice(["in-progress", "completed", "archived"]), help="Set project status")
@click.option("--format", type=click.Choice(["text", "json"]), default="text", help="Output format (text or json)")
def update(project_id, completion, priority, add_tags, remove_tags, next_steps, blockers, status, format):
    """Update project fields programmatically.

    Usage:
        jnl update myproject --completion 50
        jnl update myproject --priority high
        jnl update myproject --add-tag urgent --add-tag bug
        jnl update myproject --remove-tag old-tag
        jnl update myproject --next-steps "Implement feature X"
        jnl update myproject --blockers "Waiting on API"
        jnl update myproject --status in-progress
        jnl update myproject --completion 75 --priority high --format json
    """
    storage = get_storage()

    project = storage.load_project(project_id)
    if not project:
        if format == "json":
            import json
            print(json.dumps({"error": f"Project '{project_id}' not found", "success": False}, indent=2))
        else:
            print_error(f"Project '{project_id}' not found")
        return

    # Track what changed
    changes = []

    # Update fields
    if completion is not None:
        project.completion = completion
        changes.append(f"completion: {completion}%")

    if priority:
        project.priority = priority
        changes.append(f"priority: {priority}")

    if add_tags:
        for tag in add_tags:
            if tag not in project.tags:
                project.tags.append(tag)
                changes.append(f"added tag: {tag}")

    if remove_tags:
        for tag in remove_tags:
            if tag in project.tags:
                project.tags.remove(tag)
                changes.append(f"removed tag: {tag}")

    if next_steps is not None:
        project.next_steps = next_steps
        changes.append("next_steps updated")

    if blockers is not None:
        project.blockers = blockers
        changes.append("blockers updated")

    if status:
        project.status = status
        changes.append(f"status: {status}")

    # Check if anything changed
    if not changes:
        if format == "json":
            import json
            print(json.dumps({"error": "No fields specified to update", "success": False}, indent=2))
        else:
            print_error("No fields specified to update. Use --help to see available options.")
        return

    # Update last_active
    project.last_active = date.today()

    # Save project
    storage.save_project(project)

    # Output result
    if format == "json":
        import json
        result = {
            "success": True,
            "project_id": project.id,
            "changes": changes,
            "updated_fields": {
                "completion": project.completion,
                "priority": project.priority,
                "tags": project.tags,
                "next_steps": project.next_steps,
                "blockers": project.blockers,
                "status": project.status,
            }
        }
        print(json.dumps(result, indent=2))
    else:
        print_success(f"Updated {project.name}")
        for change in changes:
            console.print(f"  - {change}")


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
@click.argument("url", required=False)
@click.option("--github", is_flag=True, help="Add as GitHub URL")
@click.option("--claude", is_flag=True, help="Add as Claude project URL")
def link(project_id, url, github, claude):
    """Add GitHub or Claude links to a project.

    If no URL is provided, attempts to auto-detect from git repo.
    """
    storage = get_storage()

    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        return

    # Auto-detect if no URL provided
    if not url:
        git_url = detect_git_repo()
        if git_url:
            if click.confirm(f"Detected git repo: {git_url}\nLink to this project?", default=True):
                url = git_url
                github = True
            else:
                print_info("Cancelled")
                return
        else:
            print_error("No URL provided and no git repo detected")
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
@click.argument("project_ids", nargs=-1, required=True)
@click.option("--dormant", is_flag=True, help="Archive all dormant projects")
@click.option("--yes", is_flag=True, help="Skip confirmation (non-interactive mode)")
@click.pass_context
def archive(ctx, project_ids, dormant, yes):
    """Archive projects to clear them from active view.

    Archives are for projects you're shelving (not finishing).
    Use 'done' for completed projects.

    Usage:
        jnl archive my-project
        jnl archive project1 project2 project3
        jnl archive --dormant (archives all dormant projects)
        jnl archive --dormant --yes (non-interactive)
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    config = storage.config

    projects_to_archive = []

    if dormant:
        # Archive all dormant projects
        dormant_days = config.get("dormant_days", 14)
        all_projects = storage.list_projects()
        projects_to_archive = [
            p for p in all_projects
            if p.status == "in-progress" and p.days_since_active() > dormant_days
        ]

        if not projects_to_archive:
            print_info("No dormant projects to archive")
            return

        console.print(f"\n[yellow]Found {len(projects_to_archive)} dormant projects:[/yellow]")
        for p in projects_to_archive:
            console.print(f"  - {p.name} (inactive for {p.days_since_active()} days)")

        if not yes and not click.confirm("\nArchive all these projects?", default=False):
            print_info("Cancelled")
            return
    else:
        # Archive specific projects
        for project_id in project_ids:
            project = storage.load_project(project_id)
            if not project:
                print_error(f"Project '{project_id}' not found")
                continue
            if project.status == "archived":
                print_info(f"{project.name} is already archived")
                continue
            projects_to_archive.append(project)

    # Archive them
    for project in projects_to_archive:
        storage.move_to_archived(project)
        print_success(f"Archived: {project.name}")

    storage.update_project_index()

    if len(projects_to_archive) > 1:
        console.print(f"\n[green]Archived {len(projects_to_archive)} projects[/green]")


@main.command()
@click.argument("project_id")
@click.pass_context
def unarchive(ctx, project_id):
    """Restore an archived project back to active.

    Usage:
        jnl unarchive my-project
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)

    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        return

    if project.status != "archived":
        print_error(f"{project.name} is not archived")
        return

    storage.unarchive_project(project)
    storage.update_project_index()

    print_success(f"Unarchived: {project.name}")
    print_info("Project is now active again")


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

    # Time statistics
    time_stats = storage.get_time_stats(days=30)
    if time_stats["total_hours"] > 0:
        console.print(f"\n[bold]Time Logged (last 30 days):[/bold]")
        console.print(f"  Total: {time_stats['total_hours']:.1f} hours")

        # Top projects by time
        if time_stats["by_project"]:
            sorted_projects = sorted(time_stats["by_project"].items(), key=lambda x: x[1], reverse=True)
            console.print(f"\n  [bold]Top projects:[/bold]")
            for proj_name, hours in sorted_projects[:5]:
                console.print(f"    {proj_name}: {hours:.1f}h")

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
@click.pass_context
def tui(ctx):
    """Launch interactive Terminal UI for browsing projects (EXPERIMENTAL).

    WARNING: This feature is still under development and may have UX issues.
    Navigate with arrow keys or vim keys (j/k).
    Press ? for help.
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)

    try:
        from .tui import run_tui
        run_tui(storage)
    except ImportError:
        print_error("TUI requires 'textual' library")
        print_info("Install with: pip install textual")
        sys.exit(1)


# Session tracking commands

@main.command()
@click.argument("project_id")
@click.argument("task", required=False, default="")
@click.option("--force", "-f", is_flag=True, help="Auto-stop existing session")
@click.pass_context
def start(ctx, project_id, task, force):
    """Start a work session on a project.

    Tracks time and captures context for ADHD-friendly time awareness
    and interruption recovery.

    Usage:
        jnl start myproject                    - Start session on project
        jnl start myproject "Fix bug #123"     - Start with task description
        jnl start myproject --force            - Auto-stop existing session first

    The session will track elapsed time and remind you to take breaks.
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    session_manager = SessionManager.get_instance(storage)

    # Load project
    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        print_info("Use 'jnl list' to see available projects")
        return

    # Start session
    try:
        session = session_manager.start_session(project, task=task, force=force)

        # Import display function (will add this next)
        from .display import print_session_started
        print_session_started(session, project)

    except ValueError as e:
        print_error(str(e))
        print_info("Use 'jnl stop' to end current session, or --force to auto-stop")


@main.command()
@click.argument("notes", required=False, default="")
@click.pass_context
def stop(ctx, notes):
    """End the current work session.

    Saves elapsed time, creates activity log entry, and prompts for
    reflection notes.

    Usage:
        jnl stop                               - End session (interactive)
        jnl stop "Completed feature X"         - End with notes
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    session_manager = SessionManager.get_instance(storage)

    # Check if session exists
    if not session_manager.get_active_session():
        print_error("No active session")
        print_info("Start a session with: jnl start <project>")
        return

    # Get notes if not provided
    if not notes:
        notes = click.prompt(
            "\nWhat did you accomplish? (optional, press Enter to skip)",
            default="",
            show_default=False
        )

    # Stop session
    session = session_manager.stop_session(notes=notes)

    if session:
        from .display import print_session_stopped
        print_session_stopped(session, storage.load_project(session.project_id))


@main.command()
@click.pass_context
def pause(ctx):
    """Pause the current work session.

    Use this when taking a break or handling an interruption.
    Pause time won't count toward your work time.

    Usage:
        jnl pause                              - Pause current session
        jnl continue                           - Resume later
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    session_manager = SessionManager.get_instance(storage)

    try:
        session = session_manager.pause_session()

        if session:
            from .display import print_session_paused
            print_session_paused(session, storage.load_project(session.project_id))
        else:
            print_error("No active session to pause")

    except ValueError as e:
        print_error(str(e))


@main.command(name="continue")
@click.pass_context
def continue_session(ctx):
    """Resume a paused work session.

    Restores context and continues tracking time.

    Usage:
        jnl continue                           - Resume paused session
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    session_manager = SessionManager.get_instance(storage)

    try:
        session = session_manager.resume_session()

        if session:
            from .display import print_session_resumed
            print_session_resumed(session, storage.load_project(session.project_id))
        else:
            print_error("No paused session to resume")

    except ValueError as e:
        print_error(str(e))


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


# ===== AI Provider Setup Commands =====

@main.group(name="setup")
def setup_group():
    """Setup AI provider integration (Claude Code, Gemini CLI, GitHub Copilot, Cursor, etc.)."""
    pass


@setup_group.command(name="claude")
def setup_claude_new():
    """Create/update Claude Code slash command for /journel (interactive).

    Creates or updates .claude/commands/journel.md in the current directory
    with instructions for Claude Code to use JOURNEL's AI integration features.

    This is the human-friendly version with prompts.
    For LLM usage, see: jnl ai-setup claude
    """
    _setup_provider_interactive("claude")


@setup_group.command(name="gemini")
def setup_gemini_new():
    """Create/update Gemini CLI slash command for /journel (interactive).

    Creates or updates .gemini/commands/journel.toml in the current directory
    with instructions for Gemini CLI to use JOURNEL's AI integration features.

    This is the human-friendly version with prompts.
    For LLM usage, see: jnl ai-setup gemini
    """
    _setup_provider_interactive("gemini")


@setup_group.command(name="copilot")
def setup_copilot_new():
    """Create/update GitHub Copilot instructions for /journel (interactive).

    Creates or updates .github/copilot-instructions.md in the current directory
    with instructions for GitHub Copilot to use JOURNEL's AI integration features.

    This is the human-friendly version with prompts.
    For LLM usage, see: jnl ai-setup copilot
    """
    _setup_provider_interactive("copilot")


@setup_group.command(name="cursor")
def setup_cursor_new():
    """Create/update Cursor instructions for /journel (interactive).

    Creates or updates .cursorrules in the current directory
    with instructions for Cursor to use JOURNEL's AI integration features.

    This is the human-friendly version with prompts.
    For LLM usage, see: jnl ai-setup cursor
    """
    _setup_provider_interactive("cursor")


@setup_group.command(name="all")
def setup_all():
    """Create/update instructions for all AI providers (Claude, Gemini, Copilot, Cursor).

    Sets up JOURNEL integration for all supported AI assistants at once.
    You can skip individual providers if you don't use them.
    """
    console.print("\n[bold cyan]Setting up JOURNEL for all AI providers[/bold cyan]")
    console.print("You'll be prompted for each provider. Skip any you don't use.\n")

    providers_updated = []
    providers_skipped = []

    for provider_key in AI_PROVIDERS.keys():
        provider_name = AI_PROVIDERS[provider_key]["name"]
        console.print(f"\n[bold]--- {provider_name} ---[/bold]")

        # Check if already exists and up to date
        command_file = _get_provider_command_path(provider_key)
        if command_file.exists():
            current_version = _parse_version_from_file(command_file)
            if current_version == SLASH_COMMAND_VERSION:
                console.print(f"[green][OK][/green] Already up to date (v{SLASH_COMMAND_VERSION})")
                if not click.confirm("Update anyway?", default=False):
                    providers_skipped.append(provider_name)
                    continue

        if click.confirm(f"Set up {provider_name}?", default=True):
            try:
                _create_slash_command_for_provider(provider_key, command_file)
                console.print(f"[green][OK][/green] {provider_name} configured!")
                providers_updated.append(provider_name)
            except Exception as e:
                console.print(f"[red][ERROR][/red] Failed to set up {provider_name}: {e}")
        else:
            providers_skipped.append(provider_name)

    # Summary
    console.print(f"\n[bold cyan]Summary:[/bold cyan]")
    if providers_updated:
        console.print(f"[green][OK][/green] Updated: {', '.join(providers_updated)}")
    if providers_skipped:
        console.print(f"[dim]Skipped:[/dim] {', '.join(providers_skipped)}")
    console.print(f"\n[dim]All files are at version {SLASH_COMMAND_VERSION}[/dim]")


def _setup_provider_interactive(provider: str):
    """Interactive setup for any AI provider."""
    provider_config = AI_PROVIDERS[provider]
    provider_name = provider_config["name"]
    command_file = _get_provider_command_path(provider)

    if command_file.exists():
        # Check version
        current_version = _parse_version_from_file(command_file)
        console.print(f"\n[cyan]Current version:[/cyan] {current_version}")
        console.print(f"[cyan]Latest version:[/cyan] {SLASH_COMMAND_VERSION}")

        if current_version == SLASH_COMMAND_VERSION:
            console.print(f"\n[green][OK][/green] {provider_name} slash command is up to date!")
            if not click.confirm("\nUpdate anyway?", default=False):
                return
        else:
            console.print(f"\n[yellow]Update available:[/yellow] {current_version} -> {SLASH_COMMAND_VERSION}")
            if not click.confirm(f"Update {provider_name} slash command?", default=True):
                return
    else:
        console.print(f"\n[cyan]{provider_name} slash command not found[/cyan]")
        console.print(f"Will create: {command_file}")
        if not click.confirm("\nCreate slash command?", default=True):
            return

    # Create/update the file
    try:
        _create_slash_command_for_provider(provider, command_file)
        print_success(f"{provider_name} slash command created/updated!")
        console.print(f"\n[dim]Location:[/dim] {command_file}")
        console.print(f"[dim]Version:[/dim] {SLASH_COMMAND_VERSION}")
        console.print(f"\n[cyan]Usage:[/cyan] Type [bold]/journel[/bold] in {provider_name} to load instructions")
    except Exception as e:
        print_error(f"Failed to create slash command: {e}")


@main.group(name="ai-setup")
def ai_setup_group():
    """Update AI provider integration (non-interactive, LLM-friendly)."""
    pass


@ai_setup_group.command(name="claude")
def ai_setup_claude_new():
    """Update Claude Code slash command (non-interactive, LLM-friendly).

    Checks and updates .claude/commands/journel.md without prompts.
    Designed for use by AI assistants (like Claude Code).

    Exit codes:
        0 - Already up to date (no action needed)
        1 - File was created/updated (LLM should re-read)
        2 - Error occurred

    Output format (parseable by LLMs):
        [OK] Instructions current (v1.0.0)
        [OK] Updated to v1.0.1 - Re-reading instructions...
    """
    _ai_setup_provider("claude")


@ai_setup_group.command(name="gemini")
def ai_setup_gemini_new():
    """Update Gemini CLI slash command (non-interactive, LLM-friendly).

    Checks and updates .gemini/commands/journel.toml without prompts.
    Designed for use by AI assistants (like Gemini CLI).

    Exit codes:
        0 - Already up to date (no action needed)
        1 - File was created/updated (LLM should re-read)
        2 - Error occurred

    Output format (parseable by LLMs):
        [OK] Instructions current (v1.0.0)
        [OK] Updated to v1.0.1 - Re-reading instructions...
    """
    _ai_setup_provider("gemini")


@ai_setup_group.command(name="copilot")
def ai_setup_copilot_new():
    """Update GitHub Copilot instructions (non-interactive, LLM-friendly).

    Checks and updates .github/copilot-instructions.md without prompts.
    Designed for use by AI assistants (like GitHub Copilot).

    Exit codes:
        0 - Already up to date (no action needed)
        1 - File was created/updated (LLM should re-read)
        2 - Error occurred

    Output format (parseable by LLMs):
        [OK] Instructions current (v1.0.0)
        [OK] Updated to v1.0.1 - Re-reading instructions...
    """
    _ai_setup_provider("copilot")


@ai_setup_group.command(name="cursor")
def ai_setup_cursor_new():
    """Update Cursor instructions (non-interactive, LLM-friendly).

    Checks and updates .cursorrules without prompts.
    Designed for use by AI assistants (like Cursor).

    Exit codes:
        0 - Already up to date (no action needed)
        1 - File was created/updated (LLM should re-read)
        2 - Error occurred

    Output format (parseable by LLMs):
        [OK] Instructions current (v1.0.0)
        [OK] Updated to v1.0.1 - Re-reading instructions...
    """
    _ai_setup_provider("cursor")


def _ai_setup_provider(provider: str):
    """Non-interactive setup for any AI provider (LLM-friendly)."""
    provider_config = AI_PROVIDERS[provider]
    provider_name = provider_config["name"]
    command_file = _get_provider_command_path(provider)

    try:
        if not command_file.exists():
            # Create new file
            _create_slash_command_for_provider(provider, command_file)
            console.print(f"[green][OK][/green] Created {provider_name} slash command v{SLASH_COMMAND_VERSION}")
            console.print(f"[yellow]>>>[/yellow] Re-read {command_file} for current instructions")
            sys.exit(1)  # Signal update occurred

        # Check version
        current_version = _parse_version_from_file(command_file)

        if current_version == SLASH_COMMAND_VERSION:
            # Already current
            console.print(f"[green][OK][/green] {provider_name} instructions current (v{SLASH_COMMAND_VERSION})")
            sys.exit(0)  # No update needed

        # Update needed
        _create_slash_command_for_provider(provider, command_file)
        console.print(f"[green][OK][/green] {provider_name} updated to v{SLASH_COMMAND_VERSION} (was v{current_version})")
        console.print(f"[yellow]>>>[/yellow] Re-read {command_file} for current instructions")
        sys.exit(1)  # Signal update occurred

    except Exception as e:
        console.print(f"[red][ERROR][/red] {e}")
        sys.exit(2)  # Error occurred


# ===== Deprecated Command Aliases (for backward compatibility) =====

@main.command(name="setup-claude", hidden=True)
def setup_claude_deprecated():
    """Deprecated: Use 'jnl setup claude' instead."""
    console.print("[yellow]Note:[/yellow] 'jnl setup-claude' is deprecated. Use 'jnl setup claude' instead.")
    console.print()
    _setup_provider_interactive("claude")


@main.command(name="ai-setup-claude", hidden=True)
def ai_setup_claude_deprecated():
    """Deprecated: Use 'jnl ai-setup claude' instead."""
    console.print("[yellow]Note:[/yellow] 'jnl ai-setup-claude' is deprecated. Use 'jnl ai-setup claude' instead.")
    console.print()
    _ai_setup_provider("claude")


# ===== AI Integration Commands =====
# These commands allow AI assistants (like Claude Code) to track their contributions
# with clear attribution. Supports pair programming mental model and learning focus.

@main.command(name="ai-log")
@click.argument("project_or_message")
@click.argument("message", required=False)
@click.option("--hours", "-h", type=float, help="Hours spent")
@click.option("--agent", "-a", default="claude-code", help="AI agent name (default: claude-code)")
def ai_log(project_or_message, message, hours, agent):
    """Log AI-assisted work with clear attribution.

    Same as 'jnl log' but marks the entry as AI-assisted.

    Usage:
        jnl ai-log "Fixed bug (2h)"                    - AI work (auto-detect project)
        jnl ai-log journel "Fixed bug (2h)"            - AI work on specific project
        jnl ai-log journel "Feature" --agent cursor    - Specify different AI agent

    This is for Tier 1 (Suggested Actions) - the user must explicitly approve and run
    this command. For Claude Code users, this can be used via slash commands.
    """
    storage = get_storage()

    # Same logic as regular log command
    project_auto_detected = False
    time_parsed = False

    # Determine if first arg is project or message
    project = None
    if message is not None:
        project = project_or_message
        actual_message = message
    else:
        actual_message = project_or_message
        cwd = Path.cwd()
        potential_id = slugify(cwd.name)
        if storage.load_project(potential_id):
            project = potential_id
            project_auto_detected = True

    # Parse time from message if not explicitly provided
    if hours is None:
        actual_message, parsed_hours = parse_time_from_message(actual_message)
        if parsed_hours:
            hours = parsed_hours
            time_parsed = True

    # Create log entry with AI attribution
    entry = LogEntry(
        date=date.today(),
        project=project,
        message=actual_message,
        hours=hours,
        ai_assisted=True,  # Mark as AI-assisted
        agent=agent,       # Track which agent
    )

    storage.add_log_entry(entry)

    # Update project last_active
    project_name = None
    if project:
        proj = storage.load_project(project)
        if proj:
            proj.last_active = date.today()
            storage.save_project(proj)
            storage.update_project_index()
            project_name = proj.name

    # Enhanced feedback with AI marker
    print_success(f"[AI] Logged: \"{actual_message}\"")

    if project:
        if project_auto_detected:
            console.print(f"[cyan]>>>[/cyan] Project: [bold]{project_name or project}[/bold] [dim](auto-detected)[/dim]")
        else:
            console.print(f"[cyan]>>>[/cyan] Project: [bold]{project_name or project}[/bold]")
    else:
        console.print(f"[yellow]>>>[/yellow] [dim]No project linked[/dim]")

    if hours:
        if time_parsed:
            console.print(f"[cyan]>>>[/cyan] Time: [bold]{hours}h[/bold] [dim](parsed)[/dim]")
        else:
            console.print(f"[cyan]>>>[/cyan] Time: [bold]{hours}h[/bold]")

    console.print(f"[magenta]>>>[/magenta] Agent: [bold]{agent}[/bold]")


@main.command(name="ai-start")
@click.argument("project_id")
@click.argument("task", required=False, default="")
@click.option("--force", "-f", is_flag=True, help="Auto-stop existing session")
@click.option("--agent", "-a", default="claude-code", help="AI agent name (default: claude-code)")
@click.pass_context
def ai_start(ctx, project_id, task, force, agent):
    """Start an AI-assisted work session.

    Same as 'jnl start' but marks the session as AI-assisted.

    Usage:
        jnl ai-start myproject                         - Start AI session
        jnl ai-start myproject "Fix bug #123"          - With task description
        jnl ai-start myproject --force                 - Auto-stop existing session
        jnl ai-start myproject --agent cursor          - Different AI agent

    This enables tracking of pair programming sessions with AI assistants.
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    session_manager = SessionManager.get_instance(storage)

    # Load project
    project = storage.load_project(project_id)
    if not project:
        print_error(f"Project '{project_id}' not found")
        print_info("Use 'jnl list' to see available projects")
        return

    # Start AI-assisted session
    try:
        session = session_manager.start_session(project, task=task, force=force)

        # Mark as AI-assisted
        session.ai_assisted = True
        session.agent = agent
        storage.save_active_session(session)

        from .display import print_session_started
        print_session_started(session, project)
        console.print(f"[magenta]>>>[/magenta] AI Agent: [bold]{agent}[/bold]")

    except ValueError as e:
        print_error(str(e))
        print_info("Use 'jnl stop' to end current session, or --force to auto-stop")


@main.command(name="ai-stop")
@click.argument("notes", required=False, default="")
@click.option("--agent", "-a", default=None, help="Override agent name")
@click.pass_context
def ai_stop(ctx, notes, agent):
    """End an AI-assisted work session.

    Same as 'jnl stop' but with AI-focused reflection prompts.

    Usage:
        jnl ai-stop                                    - End AI session (interactive)
        jnl ai-stop "Completed feature X"              - End with notes

    Prompts focus on learning and knowledge transfer from AI collaboration.
    """
    no_emoji = ctx.obj.get('no_emoji', False) if ctx.obj else False
    storage = get_storage(no_emoji)
    session_manager = SessionManager.get_instance(storage)

    # Check if session exists
    active_session = session_manager.get_active_session()
    if not active_session:
        print_error("No active session")
        print_info("Start a session with: jnl ai-start <project>")
        return

    # Get notes with AI-focused prompt if not provided
    if not notes:
        notes = click.prompt(
            "\nWhat did you accomplish with AI assistance? What did you learn? (optional, press Enter to skip)",
            default="",
            show_default=False
        )

    # Override agent if specified
    if agent:
        active_session.agent = agent
        storage.save_active_session(active_session)

    # Stop session (this will create AI-attributed log entry)
    session = session_manager.stop_session(notes=notes)

    if session:
        from .display import print_session_stopped
        print_session_stopped(session, storage.load_project(session.project_id))
        if session.agent:
            console.print(f"[magenta]>>>[/magenta] Agent: [bold]{session.agent}[/bold]")


### ===== GitHub Import Commands =====

@main.group(name="import")
def import_group():
    """Import projects from external sources (GitHub, etc.)."""
    pass


@import_group.command(name="github")
@click.option("--recent", is_flag=True, help="Only show repos active in last 3 months")
@click.option("--resume", is_flag=True, help="Resume previous import session")
@click.option("--preview", is_flag=True, help="Preview what would be imported")
@click.option("--archive-remaining", is_flag=True, help="Bulk archive all unprocessed repos")
@click.option("--include-archived", is_flag=True, help="Include GitHub-archived repos")
@click.option("--include-forks", is_flag=True, help="Include forks with no commits")
@click.option("--ai-mode", is_flag=True, help="AI-friendly mode (plain text I/O)")
@click.option("--json", "json_output", is_flag=True, help="JSON Lines output (implies --ai-mode)")
@click.option("--force-new", is_flag=True, help="Start new session (ignore existing state)")
def import_github(recent, resume, preview, archive_remaining, include_archived, include_forks, ai_mode, json_output, force_new):
    """Import GitHub repos as JOURNEL projects.

    ADHD-friendly batch workflow:
    - Processes 10 repos at a time
    - Default action: archive (press Enter)
    - Easy escape: press 'q' to quit and save
    - Resumable: picks up where you left off

    Usage:
        jnl import github              # Start interactive import
        jnl import github --recent     # Only last 3 months
        jnl import github --resume     # Continue previous session
        jnl import github --preview    # See what would be imported
    """
    from .import_github import import_github_repos

    import_github_repos(
        recent_only=recent,
        resume=resume,
        preview=preview,
        archive_remaining=archive_remaining,
        include_archived=include_archived,
        include_forks=include_forks,
        ai_mode=ai_mode,
        json_output=json_output,
        force_new=force_new,
    )


@import_group.command(name="status")
def import_status():
    """Show GitHub import progress."""
    from .import_github import show_import_status
    show_import_status()


@main.command(name="help")
@click.argument("command", required=False)
@click.option("--all", "show_all", is_flag=True, help="Show all commands (complete reference)")
@click.pass_context
def help_command(ctx, command, show_all):
    """Show help for JOURNEL commands.

    \b
    Usage:
      jnl help              Simplified help (essential commands)
      jnl help --all        Complete command reference
      jnl help <command>    Focused help for a specific command

    \b
    Examples:
      jnl help              Show the basics
      jnl help status       Quick help for 'status' command
      jnl help --all        See all 26+ commands
    """
    from .help_text import get_simplified_help, get_full_help, get_command_help

    # jnl help <command> - Show focused help for specific command
    if command:
        help_text = get_command_help(command)
        if help_text:
            console.print(help_text)
        else:
            # Command doesn't have custom focused help, fall back to --help
            cmd = ctx.parent.command.get_command(ctx, command)
            if cmd is None:
                print_error(f"Unknown command: '{command}'")
                console.print("\n[dim]Run[/dim] [cyan]jnl help[/cyan] [dim]to see available commands.[/dim]\n")
                ctx.exit(1)

            print_info(f"Showing detailed help for '{command}':")
            console.print()
            ctx.invoke(cmd, ["--help"])
        return

    # jnl help --all - Show complete reference
    if show_all:
        console.print(get_full_help())
        return

    # jnl help - Show simplified essentials
    console.print(get_simplified_help())


def tui_main():
    """Entry point for 'tnl' command - direct TUI launcher."""
    storage = get_storage()
    try:
        from .tui import run_tui
        run_tui(storage)
    except ImportError:
        from .display import print_error, print_info
        print_error("TUI requires 'textual' library")
        print_info("Install with: pip install textual")
        sys.exit(1)


if __name__ == "__main__":
    main()
