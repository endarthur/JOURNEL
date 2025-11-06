# JOURNEL - Comprehensive ADHD Executive Function Support System
## Design Document v2.0 - The Complete Vision

---

## Executive Summary

JOURNEL will evolve from a project tracker into a **comprehensive executive function support system** - a digital accountability buddy that handles the cognitive load of organization, planning, context management, and time awareness. This system works WITH the ADHD brain rather than against it.

**Core Metaphor:** JOURNEL is your external working memory and gentle accountability partner.

---

## 1. Organizational Philosophy

### Evidence-Based ADHD Principles

#### The Executive Function Challenges We Address:
1. **Working Memory Deficits** → External memory systems
2. **Task Initiation Difficulty** → Friction reduction & clear next actions
3. **Time Blindness** → Visual time awareness & session tracking
4. **Sustained Attention Issues** → Focus modes & break reminders
5. **Transition Difficulty** → Context restoration & session boundaries
6. **Overwhelm & Decision Paralysis** → Micro-tasks & daily planning
7. **Motivation/Reward System Dysregulation** → Progress visibility & celebrations
8. **Object Permanence (Out of Sight/Mind)** → Visual cues & status displays
9. **Hyperfocus Management** → Break detection & time tracking
10. **Context Switching Costs** → Resumption cues & state preservation

### Core Design Principles

1. **ZERO FRICTION** - Every command <3 words, <5 seconds thought-to-capture
2. **EXTERNAL MEMORY** - Never rely on remembering, always show state
3. **VISUAL EVERYTHING** - Status, progress, time must be visible at a glance
4. **DOPAMINE-FRIENDLY** - Immediate feedback, progress bars, celebrations
5. **FORGIVING DESIGN** - System works even when abandoned for weeks
6. **TIME AWARENESS** - Always show time context (how long, when, deadline proximity)
7. **GENTLE ACCOUNTABILITY** - Nudges not nags, suggestions not demands
8. **ONE THING AT A TIME** - Support hyperfocus on single task/project
9. **EASY RE-ENTRY** - Restore context instantly after any interruption
10. **CELEBRATE EVERYTHING** - Make wins visible, track progress automatically

### Psychological Foundations

**From Research:**
- **External scaffolding** compensates for executive function deficits (Barkley, 2015)
- **Immediacy** crucial for ADHD motivation (temporal myopia)
- **Visual cues** overcome working memory limitations
- **Structured flexibility** better than rigid systems
- **Positive reinforcement** more effective than punishment/guilt

**ADHD-Specific Patterns We Support:**
- Interest-based nervous system (work on what's engaging NOW)
- Variable attention span (short sessions, easy breaks)
- Urgency-driven motivation (deadlines help, but need to be visible)
- Pattern recognition strength (show trends, insights)
- Hyperfocus potential (protect deep work, but add safety rails)

---

## 2. The Complete System Architecture

### Mental Model: Four Layers of Organization

```
┌─────────────────────────────────────────────────────────┐
│ LAYER 1: MOMENT (Right Now - What am I doing?)         │
│ - Active session tracking                               │
│ - Current task/focus                                    │
│ - Time elapsed                                          │
│ - Break reminders                                       │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 2: DAY (Today - What matters today?)             │
│ - Today's 1-3 focus items                              │
│ - Energy level tracking                                 │
│ - Time blocks/availability                              │
│ - Daily wins capture                                    │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 3: PROJECT (Weeks - What am I building?)         │
│ - Project tracking (current implementation)             │
│ - Next actions & blockers                               │
│ - Progress & completion                                 │
│ - Context links                                         │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 4: PATTERNS (Months - What am I learning?)       │
│ - Weekly/monthly reviews                                │
│ - Progress insights                                     │
│ - Energy patterns                                       │
│ - Success analysis                                      │
└─────────────────────────────────────────────────────────┘
```

### System Components Map

```
JOURNEL ECOSYSTEM
├── CAPTURE (Instant input, defer organization)
│   ├── Quick log
│   ├── Quick note
│   ├── Idea capture
│   └── Voice-to-text support
│
├── PLAN (Decide what matters)
│   ├── Daily planning (today mode)
│   ├── Project planning (next actions)
│   ├── Time blocking
│   └── Priority triage
│
├── WORK (Execute with support)
│   ├── Session tracking (start/stop/break)
│   ├── Focus mode (hide distractions)
│   ├── Timer/Pomodoro
│   ├── Break reminders
│   └── Context preservation
│
├── RESTORE (Resume after interruption)
│   ├── Quick status check
│   ├── Project resume
│   ├── Session resume
│   └── "Where was I?" recovery
│
├── REVIEW (Reflect & celebrate)
│   ├── Daily review (wins)
│   ├── Weekly review (patterns)
│   ├── Project completion ritual
│   └── Insights & analytics
│
└── INTEGRATE (Connect to world)
    ├── Git integration
    ├── Calendar sync
    ├── LLM context export
    └── External tool hooks
```

---

## 3. Core Workflows - The Daily ADHD Experience

### Morning: Starting the Day (3-5 minutes)

```bash
# Check in - what's my context?
$ jnl today

╔════════════════════════════════════════════════════════╗
║ WEDNESDAY, NOVEMBER 6, 2025                           ║
║ Good morning! Let's make today count.                 ║
╚════════════════════════════════════════════════════════╝

YESTERDAY'S WINS
✓ Completed MICA image pipeline (3h)
✓ Updated geoprops documentation

ACTIVE PROJECTS (3)
  MICA                  60%  [Fix deployment issues]
  geoprops              80%  [Almost done - just API docs!]
  Sakachi               45%  [Dormant 12 days]

TODAY'S FOCUS (not set)
What matters today? [Pick 1-3 things]

OPTIONS:
1. Finish geoprops (1-2h estimated) - HIGHEST IMPACT
2. Continue MICA deployment
3. Something else

> 1

TODAY'S PLAN
🎯 PRIMARY: Finish geoprops API documentation
   Estimated: 1-2 hours
   Energy needed: Medium

CALENDAR
  9:00 - 10:00  Team standup
  2:00 - 3:00   1-on-1 with manager

Available deep work: 10am-2pm (4 hours)

Ready to start? Try: jnl start geoprops
```

**Psychological Benefits:**
- External memory: Don't need to remember what you were doing
- Decision support: System suggests highest-impact work
- Time awareness: See available time blocks
- Motivation: Yesterday's wins provide positive momentum
- Reduced overwhelm: Focus on 1-3 things, not everything

### During Work: Active Session (Continuous Support)

```bash
# Start working on something
$ jnl start geoprops "Writing API documentation"

╔════════════════════════════════════════════════════════╗
║ SESSION STARTED: geoprops                              ║
║ Focus: Writing API documentation                       ║
║ Started: 10:15 AM                                      ║
╚════════════════════════════════════════════════════════╝

CONTEXT RESTORED
Last commit: "Add YAML docstrings for endpoints"
Next: Complete usage examples section
Links: [GitHub] [Claude Chat]

Press Ctrl+C to end session, or let it run.
Use 'jnl pause' to take a break.

---

# 30 minutes later (automatic check-in)
⏰ 30 minutes elapsed
   Still focused? You're doing great!

# 90 minutes later (gentle nudge)
⏰ 90 minutes - Time for a break?
   You've been hyperfocused! Consider:
   - Stretch (2 min)
   - Water/snack (5 min)
   - Short walk (10 min)

   'jnl pause' to take a break
   'jnl continue' if you're in flow

---

# User takes break
$ jnl pause

SESSION PAUSED
Worked: 1.5 hours
Take your break! Track with 'jnl break 10' for 10-min timer.

$ jnl break 10
⏱️  Break timer: 10 minutes
   [████░░░░░░░░] 3 min remaining

🔔 Break complete! Ready to continue?
$ jnl continue

RESUMING: geoprops
Paused at: Writing usage examples
Time before break: 1.5h
Let's finish this!

---

# User completes the work
$ jnl done-task "API documentation complete"

TASK COMPLETED!
Total session: 2.3 hours
Great work!

Updated: geoprops → 95% complete
Want to finish the whole project? Try: jnl done geoprops
```

**Psychological Benefits:**
- Context restoration: Links, last commit, next steps shown immediately
- Time awareness: Automatic check-ins show elapsed time
- Hyperfocus protection: Break reminders after 90 min
- Positive reinforcement: Encouragement messages, progress updates
- State preservation: Can pause/resume without losing context
- Progress visibility: See project completion increase

### Interruption: Emergency Context Switch

```bash
# You're working on geoprops when urgent bug report comes in

$ jnl start mica "Emergency: Fix production image loading"

╔════════════════════════════════════════════════════════╗
║ SWITCHING PROJECTS                                     ║
╚════════════════════════════════════════════════════════╝

Pausing: geoprops (was working 0.5h)
  Saved state: "Writing usage examples"

Starting: MICA
  Focus: Emergency - Fix production image loading
  Last worked: 2 days ago

MICA CONTEXT
Last commit: "Add image caching layer"
Quick resume: cd ~/code/mica && code .

# Work on emergency...
$ jnl log "Fixed image loading race condition"
$ jnl stop

SESSION ENDED: MICA
Total time: 1.2 hours
Well done!

# Return to previous work
$ jnl resume-last

RESUMING: geoprops
You were: Writing usage examples (paused 1.2h ago)
Time invested today: 0.5h
Continue where you left off!
```

**Psychological Benefits:**
- Low switching cost: Old context saved automatically
- Easy return: One command to get back
- No memory required: System remembers everything
- Guilt-free switching: Interruptions happen, system handles it

### Evening: Daily Review (2-3 minutes)

```bash
$ jnl review

╔════════════════════════════════════════════════════════╗
║ DAILY REVIEW - WEDNESDAY, NOVEMBER 6                  ║
╚════════════════════════════════════════════════════════╝

TODAY'S WORK
✓ geoprops (0.5h) - API documentation in progress
✓ MICA (1.2h) - Fixed production bug
Total: 1.7 hours logged

WINS TODAY
🎉 Fixed emergency production issue
🎉 Made progress on geoprops (now 95%!)

TOMORROW'S FOCUS
Based on today, suggested priorities:
1. Finish geoprops documentation (15 min left!)
2. Continue MICA improvements

How did today feel? (1-5): 4
Energy level: [███░░] Medium
Notes: "Felt good solving that bug quickly"

Streak: 3 days with logged work! 🔥
```

**Psychological Benefits:**
- Celebration: Highlights wins, not failures
- Pattern awareness: Energy tracking over time
- Motivation: Streaks provide positive reinforcement
- Planning: Seeds tomorrow's plan
- Reflection: Brief, not overwhelming

### Weekly: Pattern Recognition (5-10 minutes)

```bash
$ jnl weekly

╔════════════════════════════════════════════════════════╗
║ WEEKLY REVIEW - Week of Nov 3-9, 2025                 ║
╚════════════════════════════════════════════════════════╝

THIS WEEK'S STATS
Total work time: 12.5 hours
Sessions: 8
Projects touched: 3
Completions: 0 (but geoprops is 95%!)

PROGRESS BY PROJECT
geoprops    █████████░ 95% (+15% this week) ⚡
MICA        ██████░░░░ 60% (+5% this week)
Sakachi     ████░░░░░░ 40% (dormant)

ENERGY PATTERNS
Best work times: 10am-12pm (Mon, Wed, Fri)
Lowest energy: 2-4pm
Most productive day: Monday (4.5h)

INSIGHTS
💡 You're CLOSE on geoprops - finish it this week!
💡 Morning sessions are most productive
💡 Sakachi hasn't been touched in 2 weeks - archive it?

NEXT WEEK SUGGESTIONS
1. Complete geoprops (finally!)
2. Focus on MICA deployment
3. Consider: Archive Sakachi or set deadline

How was this week overall? (1-5):
```

**Psychological Benefits:**
- Pattern recognition: See what works for you
- Data-driven insights: Not based on feeling/memory
- Motivation: Progress visualization
- Decision support: Clear suggestions
- Self-awareness: Energy patterns help planning

---

## 4. Complete Feature Set

### Layer 1: Moment/Session Features

#### Session Tracking
```bash
jnl start <project> [task]    # Start work session
jnl stop                       # End current session
jnl pause                      # Pause session (preserve context)
jnl continue                   # Resume paused session
jnl status-now                 # Show current session
jnl switch <project>           # Switch project (save context)
```

**Data Tracked:**
- Session start/end times
- Project + specific task/focus
- Interruptions/pauses
- Context at pause (for resumption)
- Total focused time
- Break frequency

#### Break Management
```bash
jnl break [minutes]            # Start break timer
jnl remind-breaks [interval]   # Set break reminder frequency
```

**Features:**
- Pomodoro-style intervals (default 25/5)
- Custom break lengths
- Gentle reminders (not intrusive)
- Break tracking (hydration, movement, etc.)

#### Quick Capture
```bash
jnl log [project] "message"    # Quick activity log (existing)
jnl note "text"                # Quick note (existing)
jnl idea "thought"             # Capture idea for later
jnl blocker "issue"            # Record blocker immediately
```

**Design:**
- Instant capture (<5 sec)
- No required fields
- Defer organization
- Process later in batch

### Layer 2: Day/Focus Features

#### Today Mode
```bash
jnl today                      # Daily dashboard (interactive)
jnl focus <task>               # Set today's primary focus
jnl focus add <task>           # Add to today (max 3)
jnl focus clear                # Clear today's list
jnl wins                       # Show today's wins (enhanced)
```

**Today Dashboard Shows:**
- Yesterday's wins (motivation)
- Active projects status
- Today's focus items (1-3 max)
- Calendar integration (appointments)
- Available time blocks
- Energy level
- Suggestions for what to work on

**Psychological Design:**
- Start with wins (positive framing)
- Limit to 3 items (prevent overwhelm)
- Show available time (time awareness)
- Suggest priorities (reduce decision fatigue)

#### Energy Tracking
```bash
jnl energy <level>             # Log current energy (1-5)
jnl energy-check               # Quick check-in
```

**Features:**
- 5-point scale (very low → very high)
- Track alongside work logs
- Pattern analysis over time
- Suggest work based on energy

#### Daily Planning
```bash
jnl plan                       # Interactive daily planning
jnl plan tomorrow              # Plan next day
jnl schedule <task> <time>     # Time-block a task
```

**Planning Flow:**
1. Review yesterday's wins
2. Check calendar/appointments
3. Estimate available focus time
4. Choose 1-3 priorities
5. Assign to time blocks (optional)
6. Set reminders/nudges

### Layer 3: Project Features (Enhanced)

#### Micro-Task Management
```bash
jnl tasks <project>            # Show project tasks
jnl task add <project> "task"  # Add micro-task
jnl task done <id>             # Complete task
jnl task next <project>        # Show next actionable task
```

**Task Properties:**
- Very small (15-60 min each)
- Clear completion criteria
- No dependencies (can do independently)
- Sorted by priority/urgency
- Auto-generated from next_steps

**Psychological Design:**
- Break large projects into tiny pieces
- Reduce initiation friction
- Clear "done" definition
- Progress visibility

#### Urgency Support
```bash
jnl urgent <project>           # Mark as urgent
jnl deadline <project> <date>  # Set deadline
jnl due                        # Show items due soon
```

**Features:**
- Visual urgency indicators
- Deadline proximity warnings
- Automatic priority boost near deadline
- "Due today" / "Due this week" views

**Psychological Design:**
- Leverage urgency-based motivation
- Make deadlines visible (time blindness)
- Gentle escalation (not panic)

#### Enhanced Resume
```bash
jnl resume <project>           # Restore context (existing, enhanced)
jnl resume-last                # Resume last worked project
jnl quick-start                # Start most important project
```

**Enhanced Context Shows:**
- Last 3 commits (not just 1)
- Open Claude conversations
- Active tasks (not just next_steps)
- Recent notes/blockers
- Related files changed recently
- Estimated time to next milestone

### Layer 4: Pattern/Review Features

#### Review System
```bash
jnl review                     # Daily review (interactive)
jnl review weekly              # Weekly review
jnl review month               # Monthly review
jnl reflect                    # Guided reflection prompts
```

**Daily Review:**
- What did I accomplish?
- What did I learn?
- How did I feel?
- What's important tomorrow?
- Energy level pattern

**Weekly Review:**
- Progress on each project
- Time distribution
- Completion rate
- Energy patterns
- Insights/suggestions

**Monthly Review:**
- Completions this month
- Long-term progress trends
- Goal alignment check
- System usage patterns
- Adjustments needed?

#### Analytics & Insights
```bash
jnl stats                      # Statistics (existing, enhanced)
jnl insights                   # AI-generated insights
jnl patterns                   # Work pattern analysis
jnl forecast                   # Project completion predictions
```

**Enhanced Stats:**
- Work time by project/day/week
- Session length distribution
- Break frequency
- Energy correlations
- Completion velocity
- Focus time trends
- Context switch frequency

**Insights Examples:**
- "You complete 80% of projects started on Mondays"
- "Your best work happens 10am-12pm"
- "Projects with daily sessions finish 3x faster"
- "Low energy afternoons → switch to documentation tasks"

#### Streak & Motivation
```bash
jnl streak                     # Show current streaks
jnl wins                       # Celebration view (enhanced)
jnl progress <project>         # Visual progress over time
```

**Streak Types:**
- Daily logging streak
- Work session streak
- Project completion streak
- Weekly review streak

**Celebration Triggers:**
- Complete a task
- Complete a project
- Reach milestone (25%, 50%, 75%)
- Hit a streak milestone
- First work of the day
- Finish before deadline

### Integration Features

#### Calendar Integration
```bash
jnl cal sync                   # Sync with system calendar
jnl cal show                   # Show today's calendar
jnl cal block <project> <time> # Block time for project
```

**Features:**
- Read calendar to show available time
- Detect conflicts
- Suggest work times around meetings
- Optional: Create calendar events for focus blocks

#### Git Integration (Enhanced)
```bash
jnl commits <project>          # Show recent commits
jnl commit-log                 # Auto-log from git commits
jnl repo-status                # Check all project repos
```

**Features:**
- Parse git commits for automatic logging
- Detect active development
- Link commits to sessions
- Show uncommitted changes (reminder)

#### LLM Integration (Enhanced)
```bash
jnl ctx [project]              # Export context (existing)
jnl ask "question"             # Format question (existing)
jnl prompt <template>          # Use saved prompt templates
jnl claude                     # Quick Claude context export
```

**Enhanced Context Export:**
- Current session context
- Today's focus and progress
- Recent wins
- Active blockers
- Energy level
- Specific questions/requests
- Formatted for Claude Code or Claude.ai

#### External Tool Hooks
```bash
jnl hook add <event> <command> # Add custom hook
jnl notify <message>           # System notification
```

**Hook Events:**
- on_session_start
- on_session_end
- on_break_reminder
- on_project_complete
- on_deadline_approaching

**Use Cases:**
- Start Spotify focus playlist on session start
- Send notification after 90 min work
- Update external task manager
- Post to Discord/Slack on completion

---

## 5. Data Model Extensions

### New Data Structures Needed

#### Session (new)
```python
@dataclass
class Session:
    id: str
    project_id: str
    task: str
    start_time: datetime
    end_time: Optional[datetime]
    paused_at: Optional[datetime]
    pause_duration: timedelta = timedelta(0)
    interruptions: List[str] = field(default_factory=list)
    context_snapshot: dict = field(default_factory=dict)
    energy_start: Optional[int] = None
    energy_end: Optional[int] = None
    notes: str = ""
```

#### DailyPlan (new)
```python
@dataclass
class DailyPlan:
    date: date
    focus_items: List[str]  # Max 3
    time_blocks: List[TimeBlock] = field(default_factory=list)
    energy_level: Optional[int] = None
    wins: List[str] = field(default_factory=list)
    reflection: str = ""
    calendar_events: List[CalendarEvent] = field(default_factory=list)
```

#### Task (new)
```python
@dataclass
class Task:
    id: str
    project_id: str
    description: str
    created: date
    completed: Optional[date] = None
    estimated_minutes: Optional[int] = None
    priority: int = 1  # 1-5
    urgency: int = 1   # 1-5
    energy_required: str = "medium"  # low, medium, high
    next_action: bool = False  # Is this the next thing to do?
```

#### Project (enhanced)
```python
@dataclass
class Project:
    # Existing fields...

    # New fields:
    deadline: Optional[date] = None
    urgency: int = 1  # 1-5 scale
    energy_required: str = "medium"
    estimated_hours_remaining: Optional[float] = None
    tasks: List[Task] = field(default_factory=list)
    sessions: List[str] = field(default_factory=list)  # Session IDs
    milestones: List[Milestone] = field(default_factory=list)
```

#### LogEntry (enhanced)
```python
@dataclass
class LogEntry:
    # Existing fields...

    # New fields:
    session_id: Optional[str] = None
    energy_level: Optional[int] = None
    mood: Optional[str] = None
    entry_type: str = "work"  # work, idea, blocker, note, win
    tags: List[str] = field(default_factory=list)
```

### File Structure Extensions

```
~/.journel/
├── README.md
├── config.yaml
├── projects/           # Existing
├── completed/          # Existing
├── logs/              # Existing
├── sessions/          # NEW
│   ├── 2025-11.md     # Monthly session logs
│   └── active.yaml    # Currently active session
├── daily/             # NEW
│   ├── 2025-11-06.md  # Daily plans & reviews
│   └── 2025-11-05.md
├── reviews/           # NEW
│   ├── weekly/
│   │   └── 2025-W45.md
│   └── monthly/
│       └── 2025-11.md
├── .meta/             # Existing, enhanced
│   ├── projects.json
│   ├── tasks.json     # NEW
│   ├── sessions.json  # NEW
│   └── analytics.json # NEW
└── .git/
```

---

## 6. User Interface Design

### Terminal UI Principles

1. **Glanceable Status** - Core info in 1 screen
2. **Progressive Disclosure** - Details on demand
3. **Color Coding** - Consistent meaning
4. **Emoji Support** - Optional, meaningful icons
5. **Responsive** - Works in small/large terminals

### Color & Symbol System

```
Status Colors:
🟢 Green  - Active, good, on-track
🟡 Yellow - Warning, needs attention
🔴 Red    - Urgent, overdue, blocked
🔵 Blue   - Info, neutral
⚪ Gray   - Inactive, dormant

Priority:
🔥 High priority / urgent
⚡ Medium priority
💭 Low priority / someday

Progress:
█████░░░░░ Progress bars (always visible)
25% | 50% | 75% | 95% (key milestones highlighted)

Time:
⏱️  Active timer / session
⏰ Reminder / deadline
📅 Calendar / scheduled
🕐 Duration / time spent

Emotions:
🎉 Celebration / completion
💪 Motivation / encouragement
😊 Positive feedback
🤔 Reflection prompt
💡 Insight / suggestion
```

### Interactive vs Non-Interactive Modes

**Interactive Commands** (multi-step):
- `jnl today` → Shows dashboard → Prompts for focus selection
- `jnl plan` → Guided planning flow
- `jnl review` → Guided reflection
- `jnl new` → Gate-keeping → Project creation

**Quick Commands** (one-shot):
- `jnl log "message"` → Instant capture
- `jnl start project` → Begin session
- `jnl status` → Show overview
- `jnl wins` → Display wins

**Flag Overrides:**
- `--no-emoji` - ASCII only
- `--brief` - Minimal output
- `--verbose` - Full details
- `--json` - Machine-readable
- `--interactive` / `--yes` - Force mode

### Status Display Layouts

#### Compact Status (Default)
```
🔥 ACTIVE (3)  💤 DORMANT (1)  ✅ DONE (5)

MICA          ██████░░░░ 60%  2d ago  [Fix deployment]
geoprops      █████████░ 95%  4h ago  [API docs] ⚡ CLOSE!
Sakachi       ████░░░░░░ 40%  12d ago

📊 This week: 12.5h across 3 projects
⏱️  Active: geoprops (2.3h) - Writing API docs
💡 Finish geoprops today - you're SO close!
```

#### Detailed Status
```
╔════════════════════════════════════════════════════════╗
║ JOURNEL STATUS - Wednesday, November 6, 2025          ║
╚════════════════════════════════════════════════════════╝

ACTIVE PROJECTS (3)

🔥 MICA - Digital Petrography System        60% ██████░░░░
   Last: 2 days ago (Nov 4)
   Next: Fix deployment issues
   Sessions: 8 (18.5h total)
   Deadline: None

⚡ geoprops - Geological Properties Library  95% █████████░
   Last: 4 hours ago (today!)
   Next: Complete API documentation
   Sessions: 3 (4.5h total)
   Deadline: None
   ⚠️  ALMOST DONE - Finish this first!

💭 Sakachi - Pixel Art Game                 40% ████░░░░░░
   Last: 12 days ago (Oct 25)
   Status: DORMANT
   Next: Implement water physics
   Sessions: 6 (12h total)

...
[More details, stats, suggestions]
```

### Session UI

#### Active Session Display
```
╔════════════════════════════════════════════════════════╗
║ 🟢 ACTIVE SESSION                                      ║
╚════════════════════════════════════════════════════════╝

Project: geoprops
Task: Writing API documentation
Started: 10:15 AM (2h 18m ago)

Progress: ████░░░░░░░░
Completed: "Added endpoint examples"

[Updated every 30 seconds in terminal status line]
```

#### Session Complete Summary
```
╔════════════════════════════════════════════════════════╗
║ ✅ SESSION COMPLETE                                    ║
╚════════════════════════════════════════════════════════╝

Project: geoprops
Duration: 2h 18m
Breaks: 1 (10 min)
Deep focus: 2h 8m

Completed: API documentation
Project progress: 85% → 95% (+10%)

Great work! 🎉

Next time: Final review and publishing
```

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Current → Enhanced) - 2 weeks

**Goals:** Solidify core, add critical ADHD features

**Features:**
1. ✅ Enhanced `status` command (richer display)
2. ✅ Enhanced `resume` (more context, better suggestions)
3. 🆕 `jnl today` - Daily dashboard (MVP version)
4. 🆕 Session tracking basics (`start`, `stop`, `status-now`)
5. 🆕 Quick capture improvements (`idea`, `blocker`)
6. 🆕 Enhanced `wins` (today + recent)
7. 🆕 Basic time tracking in logs

**Data Model:**
- Add Session model
- Add DailyPlan model (simplified)
- Extend LogEntry with energy/type
- Add sessions/ directory

**Success Criteria:**
- User can track work sessions
- User can see "today" dashboard
- User gets better context restoration
- Time awareness improved

### Phase 2: Focus & Flow - 3 weeks

**Goals:** Support deep work and prevent burnout

**Features:**
1. 🆕 Break management (`pause`, `break`, `continue`)
2. 🆕 Break reminders (configurable intervals)
3. 🆕 Focus mode (today's 1-3 items)
4. 🆕 `jnl plan` - Interactive daily planning
5. 🆕 Energy tracking (`energy`, `energy-check`)
6. 🆕 Enhanced project switching (save/restore context)
7. 🆕 `resume-last` command
8. 🆕 Session analytics (duration, patterns)

**Data Model:**
- Add pause/resume to Session
- Add energy_level to DailyPlan and LogEntry
- Track context snapshots in Session

**Success Criteria:**
- User takes more breaks
- User plans their day
- User tracks energy levels
- Hyperfocus is protected but not destructive

### Phase 3: Micro-Tasks & Urgency - 2 weeks

**Goals:** Reduce overwhelm and leverage urgency

**Features:**
1. 🆕 Task management (`task add/done/next`)
2. 🆕 Break projects into micro-tasks
3. 🆕 Deadline support (`deadline`, `due`)
4. 🆕 Urgency indicators (visual)
5. 🆕 `quick-start` (start most important thing)
6. 🆕 Priority suggestions based on urgency
7. 🆕 Task energy labeling

**Data Model:**
- Add Task model
- Add deadline, urgency to Project
- Add estimated_hours_remaining
- Add task.energy_required

**Success Criteria:**
- Projects broken into clear next actions
- Deadlines visible and motivating
- Task initiation easier (clear next step)
- Urgency leveraged positively

### Phase 4: Patterns & Insights - 2 weeks

**Goals:** Learn from behavior, provide guidance

**Features:**
1. 🆕 Daily review (`review`)
2. 🆕 Weekly review (`review weekly`)
3. 🆕 Monthly review (`review month`)
4. 🆕 Enhanced `stats` with patterns
5. 🆕 `insights` - AI-generated observations
6. 🆕 `patterns` - Work pattern analysis
7. 🆕 Streak tracking (multiple types)
8. 🆕 `forecast` - Completion predictions

**Data Model:**
- Add Review model
- Add analytics.json cache
- Track pattern metadata

**Success Criteria:**
- User does regular reviews
- User sees patterns in their work
- User gets actionable insights
- User adjusts behavior based on data

### Phase 5: Integration & Polish - 3 weeks

**Goals:** Connect to external world, refine UX

**Features:**
1. 🆕 Calendar integration (`cal sync/show/block`)
2. 🆕 Enhanced git integration (`commits`, `commit-log`)
3. 🆕 Webhook system (`hook add`)
4. 🆕 System notifications
5. 🆕 Template system for prompts
6. 🆕 Export formats (JSON, CSV, Markdown)
7. 🆕 TUI improvements (if needed)
8. 🆕 Shell prompt integration helpers

**Infrastructure:**
- Plugin architecture for integrations
- Configuration presets/profiles
- Migration system for data changes
- Comprehensive test suite

**Success Criteria:**
- Calendar shows available time
- Git commits auto-logged (optional)
- External tools can hook in
- System feels polished

### Phase 6: Intelligence & Optimization - Ongoing

**Goals:** Smart features that learn from user

**Features:**
1. 🆕 Smart project suggestions (based on time, energy, patterns)
2. 🆕 Automatic task breakdown suggestions
3. 🆕 Completion time predictions
4. 🆕 Energy-aware scheduling
5. 🆕 Context switch cost analysis
6. 🆕 Personalized tips/nudges
7. 🆕 Habit formation tracking
8. 🆕 Burnout detection/prevention

**Approach:**
- Rule-based initially (not ML)
- Learn user patterns over time
- Suggest, never force
- Transparent recommendations

---

## 8. Configuration & Personalization

### Config File Evolution

```yaml
# ~/.journel/config.yaml

# Existing settings
editor: code
max_active_projects: 5
completion_celebration: true
auto_git_commit: true
gentle_nudges: true
dormant_days: 14
use_emojis: true

# NEW: Session settings
session:
  break_reminder_interval: 90  # minutes
  default_pomodoro: 25  # minutes
  auto_pause_inactive: 30  # minutes no input = pause
  show_timer_in_prompt: true

# NEW: Daily planning
daily:
  max_focus_items: 3
  auto_plan_morning: true  # Show 'jnl today' on first command
  review_reminder_time: "17:00"
  weekend_mode: relaxed  # Different defaults on weekends

# NEW: Energy tracking
energy:
  track_automatically: true  # Prompt for energy at session start/end
  show_patterns: true
  suggest_tasks_by_energy: true

# NEW: Urgency & deadlines
urgency:
  warn_days_before: [7, 3, 1]  # Escalating warnings
  auto_prioritize_urgent: true
  deadline_buffer_days: 2  # Treat as urgent N days before

# NEW: Integration
integrations:
  calendar:
    enabled: false
    provider: "google"  # google, outlook, ical
    sync_interval: 60  # minutes
  git:
    auto_log_commits: true
    watch_repos: true
  notifications:
    enabled: true
    provider: "system"  # system, custom

# NEW: Analytics
analytics:
  track_sessions: true
  track_energy: true
  weekly_report: true
  share_anonymous_stats: false

# NEW: Display preferences
display:
  compact_status: false
  color_scheme: "auto"  # auto, light, dark, custom
  table_style: "rounded"
  progress_bar_width: 10

# NEW: Hooks
hooks:
  on_session_start: []
  on_session_end: []
  on_break_reminder: []
  on_project_complete: []
```

### User Profiles/Presets

```bash
# Different config profiles for different modes
jnl profile use deep-work    # Max focus, minimal interruptions
jnl profile use chaotic      # More flexible, frequent check-ins
jnl profile use creative     # Longer sessions, energy-based
jnl profile create custom    # Build your own
```

**Preset Examples:**

**deep-work profile:**
- 2-hour sessions
- Break reminders at 90 min only
- No auto-pausing
- Minimal notifications

**chaotic profile:**
- 25-min Pomodoros
- Frequent check-ins
- Auto-pause at 10 min idle
- More reminders

**creative profile:**
- No time limits
- Energy-based suggestions
- Mood tracking emphasized
- Flexible planning

---

## 9. Technical Architecture Details

### Storage Layer

**Hybrid Approach:**
- **Human-readable:** Markdown files (projects, reviews, daily logs)
- **Machine-readable:** JSON caches (.meta/) for fast queries
- **Version control:** Git for sync and history

**Performance Strategy:**
- Lazy loading (only load what's needed)
- In-memory caching for active session
- Periodic cache refresh (every 5 min or on write)
- Index files for fast filtering

**Data Consistency:**
- Write markdown immediately (source of truth)
- Update JSON cache asynchronously
- Validate on read, repair if needed
- Git commits batch multiple writes

### Command Architecture

**Click Command Structure:**
```python
@main.group()
├── init
├── status (default)
├── today (new)
├── start/stop/pause/continue (new)
├── new
├── log/note/idea/blocker
├── task (new group)
│   ├── add
│   ├── done
│   └── next
├── plan (new)
├── review (new group)
│   ├── daily
│   ├── weekly
│   └── monthly
├── resume/resume-last
├── done
├── list
├── edit
├── link
├── wins
├── stats
├── insights (new)
├── patterns (new)
└── integrations (new group)
    ├── cal
    ├── git
    └── hook
```

**Shared State:**
- Session manager (singleton)
- Config (cached)
- Storage (connection pool)
- Display (theme/settings)

### Session Management

**Active Session Tracking:**
```python
class SessionManager:
    def __init__(self):
        self.active_session: Optional[Session] = None
        self.load_active_session()

    def start_session(self, project_id: str, task: str):
        # Save previous session if exists
        # Create new session
        # Save context snapshot
        # Start timer

    def pause_session(self):
        # Mark pause time
        # Save current context
        # Keep session active

    def resume_session(self):
        # Restore context
        # Resume timer

    def end_session(self):
        # Calculate duration
        # Save final state
        # Prompt for reflection
        # Update project
```

**Background Processes:**
- Timer updates (every 30 sec)
- Break reminders (configurable)
- Auto-save (every 5 min)
- Notification queue

### Display System

**Rich Terminal UI:**
```python
class Display:
    def __init__(self, config: Config):
        self.use_emoji = config.use_emojis
        self.color_scheme = config.display.color_scheme
        self.console = Console()

    def render_status(self, projects: List[Project]):
        # Generate rich table or compact view

    def render_today(self, plan: DailyPlan):
        # Interactive dashboard

    def render_session_active(self, session: Session):
        # Live session status
```

**Status Line Integration:**
- Optional: Update terminal title
- Optional: Status in PS1 prompt
- Always: Available via `jnl status-now`

### Analytics Engine

**Pattern Detection:**
```python
class Analytics:
    def calculate_energy_patterns(self) -> Dict:
        # Analyze energy by time/day
        # Return best work times

    def predict_completion(self, project: Project) -> date:
        # Based on velocity, estimate finish

    def suggest_next_task(self, context: Context) -> Task:
        # Based on time, energy, priorities

    def detect_burnout_risk(self) -> float:
        # Long sessions, no breaks, declining energy
```

**Privacy-First:**
- All analytics run locally
- No cloud processing
- Optional anonymous telemetry
- User owns all data

---

## 10. Gap Analysis - What We're Missing

### Critical Gaps in Current JOURNEL

1. **No time awareness** - Can't see how long you've worked
2. **No daily planning** - Jump straight to project work
3. **No session tracking** - Can't measure focused time
4. **No break support** - Hyperfocus until burnout
5. **No urgency/deadlines** - Everything feels equal priority
6. **No micro-tasks** - Projects feel too big
7. **No energy tracking** - Work against natural rhythms
8. **No pattern insights** - Can't learn from behavior
9. **No calendar integration** - Plan work without context
10. **No gentle accountability** - Easy to ignore for weeks

### Gaps in ADHD Support Generally

**Most ADHD tools miss:**

1. **Context Restoration** - They track, but don't help you resume
   - JOURNEL fix: Rich resume command with links, commits, notes

2. **Overwhelm Prevention** - Too many features, complex UIs
   - JOURNEL fix: Progressive disclosure, simple commands

3. **Time Blindness** - Show time logged, not time awareness
   - JOURNEL fix: Always show "elapsed", "remaining", "deadline proximity"

4. **Motivation** - Focus on productivity, not celebration
   - JOURNEL fix: Wins-first, celebrations, streaks, positive framing

5. **Flexibility** - Rigid structures that break when abandoned
   - JOURNEL fix: Forgiving design, easy re-entry, no punishment

6. **Energy Management** - Assume consistent energy all day
   - JOURNEL fix: Track energy, suggest tasks by energy level

7. **Hyperfocus Protection** - Either block it or ignore it
   - JOURNEL fix: Gentle reminders, but respect flow state

8. **Real-World Integration** - Live in isolation
   - JOURNEL fix: Calendar, git, LLM, hooks to other tools

9. **Learning** - No pattern recognition or insights
   - JOURNEL fix: Analytics, insights, personalized suggestions

10. **Gentle Accountability** - Either nagging or nothing
    - JOURNEL fix: Suggestions not demands, celebrate any progress

---

## 11. Success Metrics

### How We Know JOURNEL Works

#### Behavioral Metrics
- **More completions:** Projects completed per month
- **Less context loss:** Time to resume work after interruption
- **Better time awareness:** Accuracy of time estimates
- **Healthier work:** Break frequency, session duration
- **Consistent use:** Daily engagement with system
- **Reduced overwhelm:** Active project count
- **Better planning:** Daily review completion rate

#### Subjective Metrics (User Survey)
- "I feel less guilty about unfinished projects" (1-5)
- "I know what to work on next" (1-5)
- "I can resume work easily after breaks" (1-5)
- "The system helps, not hinders" (1-5)
- "I celebrate my wins more" (1-5)
- "I'm aware of time when working" (1-5)
- "I feel supported, not judged" (1-5)

#### System Health Metrics
- Command usage frequency
- Average time per command
- Error rates
- Feature adoption rates
- Data integrity issues

---

## 12. Future Possibilities (Beyond Scope)

### Phase 7+ Ideas

**AI-Powered Features:**
- Automatic task breakdown from project description
- Natural language command interface
- Intelligent scheduling optimization
- Burnout prediction and prevention

**Mobile Companion:**
- View-only status checking
- Quick capture on mobile
- Notifications for deadlines
- Voice logging

**Team Features:**
- Share project status (opt-in)
- Accountability partners
- Shared celebration when team completes
- Anonymous ADHD peer support

**Extended Integrations:**
- Todoist/Things/OmniFocus import
- Obsidian vault sync
- GitHub Actions auto-updates
- Slack/Discord webhooks
- Email summaries

**Advanced Analytics:**
- ML-based pattern detection
- Predictive project risk analysis
- Optimal work time recommendations
- Collaboration pattern analysis

**Gamification:**
- Achievement system
- Leveling up
- Challenges/quests
- Public portfolio showcase

---

## 13. Philosophical Foundations

### Why JOURNEL is Different

**Traditional Productivity Tools:**
- Assume neurotypical executive function
- Optimize for efficiency
- Punish "failure" (red overdue tasks, guilt)
- Require consistent discipline
- Force rigid structures

**JOURNEL Philosophy:**
- Design for executive function deficits
- Optimize for **completion** and **well-being**
- Celebrate any progress
- Work with variable motivation/energy
- Provide flexible scaffolding

### The ADHD-First Design Approach

**Start with the hardest challenges:**
1. Task initiation ("I don't know where to start")
2. Context restoration ("What was I doing?")
3. Time blindness ("Where did the day go?")
4. Overwhelm ("Too many things!")
5. Motivation ("Why does this matter?")

**Then build systems that:**
- Make starting easy (clear next action)
- Make resuming easy (rich context)
- Make time visible (always show elapsed/remaining)
- Make choices manageable (max 3 today)
- Make wins visible (celebrations, progress)

### Evidence-Based ADHD Interventions

**What Research Shows Works:**

1. **External Cues** - Put reminders in environment
   - JOURNEL: Visual status, notifications, prompts

2. **Immediate Feedback** - Reward quickly, not delayed
   - JOURNEL: Instant progress updates, celebrations

3. **Reduce Working Memory Load** - Offload to external systems
   - JOURNEL: Everything written down, nothing memorized

4. **Structure + Flexibility** - Scaffolding, not cages
   - JOURNEL: Suggested workflows, but customizable

5. **Point-of-Performance Support** - Help at moment of need
   - JOURNEL: Context at start, break reminders during work

6. **Interest-Based Engagement** - Leverage natural motivation
   - JOURNEL: Work on what's engaging, track patterns

7. **Accountability** - External commitment helps
   - JOURNEL: Gentle nudges, streak tracking, reviews

**What Doesn't Work:**
- Complex hierarchies (too much cognitive load)
- Rigid schedules (break when life happens)
- Shame-based motivation (demotivating)
- Willpower-dependent systems (executive function deficit)
- Hidden progress (need visible wins)

---

## 14. Implementation Principles

### Development Philosophy

**Build in This Order:**
1. **Most ADHD-critical features first** (time awareness, context)
2. **Most friction-reducing features second** (quick capture, easy start)
3. **Nice-to-haves last** (analytics, integrations)

**Always:**
- Keep commands simple (2-3 words max)
- Test on real ADHD users (not just developers)
- Measure time-to-action (should be <5 seconds)
- Prioritize reliability over features
- Make errors gentle and helpful

**Never:**
- Add complexity without clear ADHD benefit
- Require configuration to use
- Punish or shame user behavior
- Assume consistent usage patterns
- Hide important information

### Quality Standards

**Every Feature Must:**
1. Solve a specific ADHD challenge (which one?)
2. Reduce friction (how much time saved?)
3. Be simple to use (can you explain in one sentence?)
4. Fail gracefully (what if abandoned for weeks?)
5. Provide immediate value (not "pay off later")

**Every Command Must:**
1. Complete in <2 seconds (performance)
2. Provide clear feedback (what happened?)
3. Be forgiving of mistakes (undo/edit)
4. Work offline (no cloud dependency)
5. Respect user's context (don't interrupt)

---

## 15. Documentation Strategy

### User-Facing Docs

**Quick Start:**
- 5-minute tutorial
- Core workflow (today → start → log → stop → review)
- No theory, just practice

**Command Reference:**
- Every command with examples
- Common patterns
- Troubleshooting

**ADHD-Specific Guide:**
- "Why JOURNEL is different"
- Strategies for common ADHD challenges
- Customization for your brain
- Habit formation tips

**Video Tutorials:**
- Screen recordings of real usage
- "Day in the life with JOURNEL"
- Tips and tricks

### Developer Docs

**Architecture:**
- System design overview
- Data models and relationships
- Command flow diagrams
- Integration points

**Contributing:**
- ADHD-first design principles
- Code style (simplicity > cleverness)
- Testing requirements
- Review process

**API Documentation:**
- For plugin/integration developers
- Hook system
- Data export formats

---

## Conclusion

JOURNEL evolves from a project tracker into a **comprehensive executive function support system**. It doesn't just track work - it actively helps you:

- **Plan** what matters (without overwhelm)
- **Start** work (without friction)
- **Maintain focus** (with break support)
- **Resume** after interruption (with full context)
- **Complete** projects (with celebration)
- **Learn** from patterns (with insights)
- **Improve** over time (with gentle accountability)

The system respects ADHD neurology, working **with** the brain's natural patterns rather than fighting them. It reduces cognitive load, provides external memory, makes time visible, and celebrates progress.

**This is the north star.** Build toward this vision, one ADHD-friendly feature at a time.

---

**Next Steps:**
1. Review this design with ADHD users
2. Prioritize Phase 1 features
3. Build and test iteratively
4. Gather feedback continuously
5. Evolve based on real-world usage

**Remember:** Better to build half of this well than all of it poorly. Start with the most critical ADHD features (time awareness, session tracking, today mode) and expand from there.

---

*JOURNEL: Your external working memory. Your accountability buddy. Your path to finishing what you start.*
