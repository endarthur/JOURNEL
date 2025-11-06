# JOURNEL - Project Organization System
## Design Document v1.0

---

## 1. Overview

**JOURNEL** is an ADHD-friendly project organization and tracking system designed to help maintain focus, restore context, and celebrate completion rather than endless project-hopping.

**Name Origin:**
- Homage to André Journel (geostatistics pioneer, GSLIB)
- Portmanteau: JOURNEL = Journal (project logging)
- Personal/insider reference that rewards those who get it

**Primary User:** Arthur (developer with ADHD, works across geology/mining software projects)

**Core Problem:** Starting new projects instead of finishing existing ones, losing context between sessions, lack of accountability.

---

## 2. Design Principles

### ADHD-Friendly Features
1. **Zero Friction** - Commands are 2-3 words max (`jnl status`, `jnl log`)
2. **Instant Info** - No waiting, no mode switching, immediate feedback
3. **Forgiving** - No perfect tracking required, can catch up easily
4. **Visual** - Use emoji, colors, clear status indicators
5. **Non-judgmental** - "Dormant" not "abandoned", celebrate any progress
6. **Context-Rich** - Links to conversations, commits, notes automatically
7. **Wins-Focused** - Track and celebrate completions

### Core Philosophy
- **Accountability buddy**, not just organization tool
- **Context restoration system** for picking up where you left off
- **Gentle nudges**, not nagging reminders
- **Completion ritual** to make finishing special

---

## 3. Architecture Decisions

### Storage: Plain Text + Git
- **Location:** `~/.journel/` directory
- **Format:** Markdown files with YAML frontmatter for metadata
- **Version Control:** Git repository for sync across machines
- **Rationale:** Human-readable, grep-able, transparent, no lock-in

### Project Definition
- **Projects = Claude.ai Projects** (simplest approach)
- Can manually add external projects
- Support for **tags/groups** (e.g., `geology-tools`, `games`)
- No complex sub-project hierarchies (keep it simple)

### LLM Integration Strategy
- **No built-in LLMs** in JOURNEL itself (complexity, cost, speed)
- **LLM-readable data format** instead
- User asks Claude separately, shares context via `jnl ctx`
- JOURNEL = filing system, Claude = analyst

### Complexity Level
- **Light to Medium** integration depth
- Track metadata + links, parse git commits, open projects
- NO deep IDE integration, file watchers, auto-logging (too complex)

---

## 4. File Structure

```
~/.journel/
├── README.md                    # System documentation (for humans & LLMs)
├── config.yaml                  # User preferences
├── projects/
│   ├── mica.md                 # One file per project
│   ├── geoprops.md
│   ├── ggr.md
│   ├── sakachi.md
│   └── geo-modeling.md
├── logs/
│   ├── 2025-11.md              # Monthly activity logs
│   └── 2025-10.md
├── completed/
│   ├── finished-project.md     # Graduated projects
│   └── another-done.md
└── .meta/
    ├── projects.json           # Machine-readable index
    └── tags.json               # Tag definitions
```

### Project File Format
```markdown
---
id: mica
name: MICA
full_name: "MICA - Digital Petrography System"
status: in-progress
tags: [geology-tools, microscopy, web]
created: 2025-10-01
last_active: 2025-11-05
completion: 60
priority: high
github: https://github.com/username/mica
claude_project: https://claude.ai/project/uuid
next_steps: "Fix image loading pipeline"
blockers: "Need sample thin section images"
---

# MICA - Digital Petrography System

## Overview
Web-based digital microscopy for thin section analysis.

## Recent Activity
- 2025-11-05: Worked on image pipeline
- 2025-11-03: Fixed zoom controls

## What I Learned
- Canvas performance matters for large images
- Need proper color calibration

## Notes
Random thoughts, links, snippets...
```

### Log File Format
```markdown
# November 2025 Activity Log

## 2025-11-05
- **MICA** (2h): Fixed image loading bug
- **geoprops** (1h): Documentation updates
- Note: Feeling good about progress!

## 2025-11-04
- **Sakachi** (3h): Pixel art improvements
- Won: Finished dam physics!
```

---

## 5. Commands & Features

### Command Aliases
- `journel` or `jnl` (both work)
- `journel` = `journel status` (default command)
- `jnl ctx` = `journel context` (speed alias)

### Core Commands

#### `journel init`
Sets up the system for first time use.
```bash
$ journel init
```
- Creates `~/.journel/` structure
- Generates README and config
- Initializes git repository
- Welcomes user

#### `journel status` (default)
Shows overview of all projects.
```bash
$ journel
$ jnl
$ journel status
```

Output format:
```
🔥 ACTIVE (3)
  MICA                    60%   3 days ago    [Fix image loading]
  geoprops                80%   2 weeks ago   [Nearly done!]
  
💤 DORMANT (2) 
  GGR                     40%   1 month ago
  Sakachi                 50%   3 weeks ago
  
✅ COMPLETED (5)
  [Recently: geological-modeling, aerial-stereo-pairs]

📊 This week: 8 hours logged across 3 projects
💡 Tip: geoprops is 80% done - finish it first?
```

#### `journel new <name>`
Creates a new project (with gentle gate-keeping).
```bash
$ journel new cool-idea
```

Behavior:
1. Checks for unfinished projects
2. Shows warning if >3 active projects
3. Asks "Really start something new?"
4. If yes, creates project file
5. Optionally links to Claude conversation

#### `journel log "<message>"`
Quick activity logging.
```bash
$ jnl log "Fixed RBF interpolation bug"
$ jnl worked-on mica 2h
```

- Appends to today's log
- Associates with current project (if in project directory)
- Optionally includes time spent

#### `journel context` / `jnl ctx`
Exports context for LLM analysis.
```bash
$ jnl ctx
$ jnl ctx --project mica
```

Generates markdown summary:
- Active project statuses
- Recent activity
- Blockers and next steps
- Completion percentages
- Question template

Output to stdout (easy to copy/paste to Claude).

#### `journel ask "<question>"`
Formats a question with auto-gathered context.
```bash
$ jnl ask "what should I work on today?"
```

Creates formatted output:
```markdown
# JOURNEL Context for Claude

## Active Projects
[auto-generated from project files]

## Recent Activity  
[last week's logs]

## Question
what should I work on today?

---
Copy this to Claude for analysis
```

#### `journel done <project>`
Completion ritual!
```bash
$ journel done mica
```

Flow:
1. Marks project as complete
2. Asks: "What did you learn?" (one-liner)
3. Asks: "How do you feel?" (optional)
4. Shows celebration message 🎉
5. Moves to `completed/` directory
6. Updates stats

#### `journel resume <project>`
Context restoration for picking up work.
```bash
$ jnl resume mica
```

Shows:
- Last conversation URL
- Last commit message  
- What you said you'd do next
- Recent notes
- Optionally: cd to project dir, open editor

#### `journel list`
Lists all projects with filters.
```bash
$ jnl list
$ jnl list --active
$ jnl list --tag geology-tools
$ jnl list --dormant
```

#### `journel edit <project>`
Opens project file in $EDITOR.
```bash
$ jnl edit mica
```

#### `journel link <project> <url>`
Add GitHub/Claude links to project.
```bash
$ jnl link mica https://github.com/user/mica
$ jnl link mica --claude https://claude.ai/project/uuid
```

#### `journel note "<text>"`
Quick note capture (goes to current project + today's log).
```bash
$ jnl note "Remember to test with polarized light images"
```

#### `journel wins`
Show completed projects and streak.
```bash
$ jnl wins
```

Output:
```
✅ COMPLETED PROJECTS (5)

Recent completions:
  🎉 geological-modeling    (completed 2 weeks ago)
  🎉 aerial-stereo-pairs    (completed 1 month ago)
  
All time: mica-v1, sakachi-prototype, data-importer...

🔥 Current streak: 2 completions in last month!
```

#### `journel stats`
Overall statistics and insights.
```bash
$ jnl stats
```

Shows:
- Total projects (active/dormant/completed)
- Hours logged this week/month
- Completion rate
- Longest streak
- Most-worked-on projects

### Optional/Future Commands

#### `journel tui`
Interactive terminal UI for browsing (opt-in, not default).
```bash
$ journel tui
$ journel browse
```

#### `journel sync`
Manual git sync (push/pull).
```bash
$ jnl sync
```

---

## 6. Terminal Integration

### Prompt Integration (Optional)
User can add to PowerShell `$PROFILE` or WSL `.bashrc`:
```bash
# Shows active project count in prompt
function journel_prompt() {
    journel status --brief
}
```

### Gentle Context Display
On terminal launch (via profile), optionally show:
```
[JOURNEL: 3 active projects, last: mica (3 days ago)]
```

User decides if they want this (not forced).

---

## 7. Technical Implementation

### Language: Python 3.8+
**Why:** 
- Cross-platform (Windows/WSL/Mac/Linux)
- Rich CLI libraries (Click, Rich for colors)
- Easy to install/distribute
- Fast enough for this use case

### Dependencies (Minimal)
- `click` - CLI framework
- `rich` - Terminal colors/formatting
- `pyyaml` - Config files
- `gitpython` - Git operations
- Standard library for everything else

### Entry Point
```python
# setup.py or pyproject.toml creates:
# - `journel` command
# - `jnl` command (alias)
```

### Project Structure
```
journel/
├── __init__.py
├── cli.py              # Click commands
├── models.py           # Project, Log data classes
├── storage.py          # File I/O, git operations
├── display.py          # Rich formatting
├── utils.py            # Helpers
└── config.py           # Config management
```

### Config File Format
```yaml
# ~/.journel/config.yaml
journel_dir: ~/.journel
editor: code  # or vim, nano, etc.
default_view: status
max_active_projects: 5
completion_celebration: true
auto_git_commit: true
gentle_nudges: true
```

---

## 8. Implementation Priority

### Phase 1: MVP (Build First)
1. ✅ `journel init` - Set up structure
2. ✅ `journel new` - Create projects (with gate-keeping)
3. ✅ `journel status` - Show overview
4. ✅ `journel log` - Quick logging
5. ✅ `journel ctx` - Context export

### Phase 2: Core Features
6. ✅ `journel done` - Completion ritual
7. ✅ `journel resume` - Context restoration
8. ✅ `journel list` - Filtering
9. ✅ `journel edit` - Quick edits
10. ✅ `journel link` - Add URLs

### Phase 3: Nice-to-Have
11. `journel wins` - Celebration
12. `journel stats` - Analytics
13. `journel tui` - Interactive mode
14. Prompt integration
15. Auto-sync on commands

---

## 9. Example Workflow

### Starting a Day
```bash
$ jnl                    # See what's active
🔥 ACTIVE: MICA (60%), geoprops (80%), GGR (40%)
💡 geoprops is almost done - finish it?

$ jnl resume geoprops    # Get context
Last worked: 2 weeks ago
Next: "Write API documentation"
Claude: https://claude.ai/chat/...
Opening ~/code/geoprops...
```

### During Work
```bash
$ jnl log "Finished API docs"
$ jnl note "Need to add usage examples"
$ jnl worked-on geoprops 3h
```

### Finishing Up
```bash
$ jnl done geoprops
What did you learn? > YAML docstrings are great for API docs
How do you feel? > Relieved! This was blocking me

🎉 CONGRATULATIONS! 🎉
geoprops is COMPLETE!

That's your 3rd completion this month!
```

### When Asking for Help
```bash
$ jnl ctx > context.md   # Or just print and copy
# Paste into Claude Code or Claude.ai
```

---

## 10. Success Criteria

JOURNEL succeeds if Arthur:
1. ✅ Finishes more projects than before
2. ✅ Spends less time wondering "what was I doing?"
3. ✅ Feels less guilt about project-hopping
4. ✅ Actually uses it (because it's fast/easy)
5. ✅ Can restore context after weeks away
6. ✅ Celebrates completions rather than just moving on

---

## 11. Non-Goals

What JOURNEL is NOT:
- ❌ Full project management system (no Gantt charts, dependencies)
- ❌ Time tracking tool (just rough logging)
- ❌ Code editor integration (stay simple)
- ❌ Multi-user system (personal tool only)
- ❌ AI-powered anything (data is AI-readable, that's it)

---

## 12. Future Possibilities

Ideas for later (don't build now):
- Weekly/monthly email summaries
- GitHub Actions integration for auto-updates
- Obsidian vault export
- Mobile companion app (view-only)
- Public portfolio generator
- Integration with other tools (Todoist, etc.)

---

## 13. Notes for Implementation

### Windows Compatibility
- Use `pathlib.Path` for cross-platform paths
- Test on both cmd, PowerShell, and WSL
- Handle Windows line endings
- Terminal colors may need fallbacks

### Git Integration
- Auto-commit after major commands (optional)
- Don't force push (let user control sync)
- Handle merge conflicts gracefully
- Work offline (sync is optional)

### Error Handling
- Gentle error messages ("Oops!" not stack traces)
- Suggestions for fixes
- Never lose data (backup before destructive ops)

### Performance
- Keep commands <100ms where possible
- Lazy load project files (don't read all at once)
- Cache computed values (completion %, stats)

---

## Questions for Initial Implementation

1. Should `journel new` auto-detect if we're in a git repo?
2. Should `journel log` auto-detect current project from `pwd`?
3. How many days until a project is "dormant"? (14 days?)
4. Should completion % be manual or computed from tasks?
5. Color scheme preferences?

---

**End of Design Document**

Ready to build! 🚀
