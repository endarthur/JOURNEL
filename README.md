# JOURNEL

**JOURNEL** is an ADHD-friendly project organization and tracking system designed to help maintain focus, restore context, and celebrate completion.

## Name Origin

Homage to André Journel (geostatistics pioneer, GSLIB) + Journal (project logging)

## Features

- Zero friction CLI commands (`jnl status`, `jnl log`)
- Plain text storage (Markdown + YAML)
- Context restoration for picking up where you left off
- Gentle gate-keeping to prevent project-hopping
- Completion rituals to celebrate finishing projects
- LLM-friendly data format for AI analysis

## Installation

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

## Quick Start

```bash
# Initialize JOURNEL
journel init

# Create a new project
journel new my-project

# Check status
journel
jnl status

# Log work
jnl log "Fixed the bug"

# Get context for AI
jnl ctx

# Complete a project
jnl done my-project
```

## Commands

- `journel init` - Set up JOURNEL for first use
- `journel status` - Show all projects (default command)
- `journel new <name>` - Create a new project
- `journel log "<message>"` - Quick activity logging
- `journel ctx` - Export context for LLM analysis
- `journel done <project>` - Mark project as complete
- `journel resume <project>` - Restore context for a project
- `journel list` - List all projects with filters
- `journel edit <project>` - Edit project file
- `journel link <project> <url>` - Add links to project
- `journel note "<text>"` - Quick note capture

## Philosophy

JOURNEL is an accountability buddy, not just an organization tool. It helps you:
- Track progress without perfect tracking
- Restore context when returning to projects
- Get gentle nudges without nagging
- Celebrate completions, not just start new things

## Author

Arthur Endlein (endarthur@gmail.com)

## License

MIT
