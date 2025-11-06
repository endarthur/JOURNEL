# JOURNEL Vision Summary
## Executive Function Support System - The Complete Picture

---

## What JOURNEL Becomes

**From:** Project tracking tool with logging and completion rituals

**To:** Comprehensive ADHD executive function support system - your external working memory and gentle accountability buddy

---

## The Four Layers

### Layer 1: MOMENT (Right Now)
**What am I doing? How long have I been working?**

- Active session tracking with elapsed time
- Break reminders after 90 min (hyperfocus protection)
- Pause/resume for interruptions
- Always know: What am I working on? For how long?

**Core Feature:** `jnl start/stop/pause/continue`

---

### Layer 2: DAY (Today)
**What matters today? What did I accomplish?**

- Daily dashboard showing yesterday's wins
- Focus mode (1-3 priorities max)
- Calendar integration (available time blocks)
- Energy level tracking
- Daily review and reflection

**Core Feature:** `jnl today` (interactive daily planning)

---

### Layer 3: PROJECT (Weeks)
**What am I building? What's next?**

- Project tracking (existing, enhanced)
- Micro-task breakdown (clear next actions)
- Deadline and urgency support
- Rich context restoration
- Progress visibility

**Core Feature:** `jnl tasks` and `jnl resume` (enhanced)

---

### Layer 4: PATTERNS (Months)
**What am I learning about myself?**

- Weekly/monthly reviews
- Work pattern analysis (energy, timing, productivity)
- Insights and suggestions
- Completion forecasting
- Streak tracking

**Core Feature:** `jnl insights` and `jnl review weekly`

---

## Key Workflows

### Morning: Starting the Day (3 minutes)

```bash
$ jnl today

YESTERDAY'S WINS
✓ Completed MICA image pipeline (3h)
✓ Updated geoprops docs

TODAY'S FOCUS
1. 🔥 Finish geoprops (HIGH IMPACT - 1h left)
2. Fix MICA deployment

CALENDAR
  9-10am: Team standup
  2-3pm: 1-on-1

Available: 10am-2pm (4 hours deep work)

Ready? 'jnl start geoprops'
```

**Benefits:**
- See yesterday's wins (motivation)
- Clear priorities (reduce overwhelm)
- Time awareness (plan realistically)
- One-command start (zero friction)

---

### During Work: Deep Focus (Continuous)

```bash
$ jnl start geoprops "API documentation"

SESSION STARTED: geoprops (10:15 AM)
Focus: API documentation

Last commit: "Add YAML docstrings"
Next: Complete usage examples

# --- 30 min later ---
⏱️  30 min - Still focused? Great!

# --- 90 min later ---
⏰ Time for a break?
   You've been working 1.5h straight
   'jnl pause' to take a break

$ jnl pause
$ jnl break 10    # 10-min break timer

# --- After break ---
$ jnl continue
Resuming: geoprops (worked 1.5h before break)
```

**Benefits:**
- Time awareness (see elapsed)
- Hyperfocus protection (break reminders)
- Easy pause/resume (interruption handling)
- Context preserved (pick up where you left off)

---

### Interruption: Emergency Switch

```bash
# Working on geoprops when urgent bug appears

$ jnl start mica "Emergency: prod image loading"

SWITCHING PROJECTS
Paused: geoprops (saved state)
Starting: MICA

# --- Fix the bug ---

$ jnl stop

# --- Return to previous work ---

$ jnl resume-last

RESUMING: geoprops
You were: Writing usage examples (paused 1.2h ago)
Ready to continue!
```

**Benefits:**
- Low switching cost (context saved)
- Easy return (one command)
- No memory required (system remembers)

---

### Evening: Daily Review (2 minutes)

```bash
$ jnl review

TODAY'S WORK
✓ geoprops (2.5h) - Completed API docs!
✓ MICA (1.2h) - Fixed prod bug

WINS
🎉 Finished geoprops completely!
🎉 Solved emergency production issue

How did today feel? (1-5): 4
Energy: Medium
Notes: "Felt great finishing geoprops!"

Streak: 4 days with logged work 🔥

TOMORROW'S FOCUS
Suggested: Start MICA deployment (high priority)
```

**Benefits:**
- Celebrate wins (dopamine)
- Reflect briefly (pattern awareness)
- Plan tomorrow (reduce morning friction)
- Track energy (learn patterns)

---

### Weekly: Pattern Recognition (5 minutes)

```bash
$ jnl review weekly

WEEK OF NOV 3-9

STATS
Total: 12.5 hours across 8 sessions
Projects: 3 (geoprops, MICA, Sakachi)
Completions: 1 (geoprops! 🎉)

PROGRESS
geoprops  █████████░ COMPLETED (+45% this week)
MICA      ██████░░░░ 60% (+5%)
Sakachi   ████░░░░░░ 40% (dormant)

ENERGY PATTERNS
Best work: 10am-12pm (Mon, Wed, Fri)
Low energy: 2-4pm (all days)
Most productive: Monday (4.5h)

INSIGHTS
💡 geoprops finished - you completed ALL API docs!
💡 Morning sessions are most productive
💡 Sakachi dormant 2 weeks - archive or set deadline?

NEXT WEEK
1. Focus on MICA deployment
2. Archive Sakachi or revive with deadline
3. Start new project? (You have capacity now)
```

**Benefits:**
- See progress (motivating)
- Learn patterns (energy, timing)
- Get suggestions (data-driven)
- Plan ahead (strategic)

---

## Critical Features by Phase

### Phase 1: Foundation (Weeks 1-2)
**Must-Have:** Time awareness and daily focus

- Session tracking (`start/stop/pause/continue`)
- Today dashboard (`jnl today`)
- Enhanced status (show active session)
- Basic time tracking

**Why First:** Solves time blindness and daily overwhelm

---

### Phase 2: Focus & Flow (Weeks 3-5)
**Must-Have:** Prevent burnout and support deep work

- Break management (`break`, reminders)
- Energy tracking (`energy`)
- Enhanced context switching (`resume-last`, `switch`)
- Focus mode (max 3 items today)

**Why Next:** Protects hyperfocus, maintains health

---

### Phase 3: Micro-Tasks & Urgency (Weeks 6-7)
**Must-Have:** Reduce overwhelm and leverage urgency

- Task breakdown (`task add/done/next`)
- Deadline support (`deadline`, `due`)
- Urgency indicators (visual)
- Clear next actions

**Why Next:** Makes large projects manageable

---

### Phase 4: Patterns & Insights (Weeks 8-9)
**Must-Have:** Learn from behavior

- Daily/weekly/monthly reviews
- Pattern analysis (`patterns`, `insights`)
- Streak tracking
- Completion forecasting

**Why Next:** Enables self-awareness and improvement

---

### Phase 5: Integration & Polish (Weeks 10-12)
**Nice-to-Have:** Connect to external world

- Calendar integration (available time)
- Enhanced git (auto-logging)
- Notifications (break reminders)
- Hooks (customization)

**Why Last:** Useful but not critical to core value

---

## What Makes This ADHD-Friendly

### Problem: "I don't know what to work on"
**Solution:** `jnl today` suggests 1-3 priorities based on urgency, impact, completion

### Problem: "I lose track of time"
**Solution:** Always show elapsed time, break reminders, time estimates

### Problem: "I forget what I was doing"
**Solution:** Rich context restoration (commits, notes, links, last state)

### Problem: "Projects feel overwhelming"
**Solution:** Break into micro-tasks (15-60 min each), clear next action

### Problem: "Deadlines sneak up on me"
**Solution:** Visual urgency, deadline proximity warnings, escalating reminders

### Problem: "I hyperfocus until burnout"
**Solution:** Gentle break reminders at 90 min, protect but don't interrupt flow

### Problem: "I can't maintain motivation"
**Solution:** Immediate progress visibility, celebrations, streaks, wins-first framing

### Problem: "Interruptions kill my momentum"
**Solution:** Pause/resume with full context, easy return, low switching cost

### Problem: "I feel guilty about unfinished projects"
**Solution:** "Dormant" not "failed," forgiving re-entry, celebrate any progress

### Problem: "I don't learn from my patterns"
**Solution:** Energy tracking, work pattern analysis, insights, suggestions

---

## The Complete Command Set

### Moment (Session)
```bash
jnl start <project> [task]    # Start work session
jnl stop                       # End session
jnl pause                      # Pause (preserve context)
jnl continue                   # Resume paused session
jnl status-now                 # Show active session
jnl break [minutes]            # Break timer
```

### Day (Today)
```bash
jnl today                      # Daily dashboard
jnl focus <task>               # Set today's focus
jnl focus add <task>           # Add to today (max 3)
jnl energy <level>             # Log energy (1-5)
jnl review                     # Daily review
jnl wins                       # Today's wins
```

### Project (Weeks)
```bash
jnl new <name>                 # Create project (gate-keeping)
jnl status                     # All projects overview
jnl resume <project>           # Restore context
jnl resume-last                # Resume last worked
jnl quick-start                # Start most important

jnl tasks <project>            # Show tasks
jnl task add "task"            # Add micro-task
jnl task done <id>             # Complete task
jnl task next                  # Show next action

jnl deadline <project> <date>  # Set deadline
jnl due                        # Show due items
jnl urgent <project>           # Mark urgent

jnl log "message"              # Quick log
jnl note "text"                # Quick note
jnl idea "thought"             # Capture idea
jnl blocker "issue"            # Record blocker

jnl done <project>             # Complete (celebration)
jnl edit <project>             # Edit file
jnl link <project> <url>       # Add link
```

### Patterns (Months)
```bash
jnl review weekly              # Weekly review
jnl review month               # Monthly review
jnl stats                      # Statistics
jnl insights                   # AI insights
jnl patterns                   # Work patterns
jnl forecast                   # Completion predictions
jnl streak                     # Show streaks
```

### Integration
```bash
jnl cal sync                   # Calendar sync
jnl cal show                   # Show calendar
jnl commits <project>          # Recent commits
jnl ctx                        # LLM context export
jnl hook add <event> <cmd>     # Custom hooks
jnl sync                       # Git sync
```

---

## Data Model Overview

### Core Models

**Session** (new)
- Tracks active work: project, task, start/end, pauses, breaks
- Links to commits, notes, energy
- Enables time awareness

**DailyPlan** (new)
- Today's focus (1-3 items)
- Calendar events, available time
- Energy level, wins, reflection
- Enables daily planning

**Task** (new)
- Micro-tasks for projects (15-60 min)
- Clear next action
- Priority, urgency, energy required
- Enables overwhelm reduction

**Project** (enhanced)
- Add: deadline, urgency, energy_required
- Add: estimated_hours_remaining
- Add: tasks list, sessions list
- Add: milestones

**LogEntry** (enhanced)
- Add: session_id, energy_level, mood
- Add: entry_type (work/idea/blocker/note/win)
- Add: tags

### File Structure

```
~/.journel/
├── projects/           # Existing
├── completed/          # Existing
├── logs/              # Existing
├── sessions/          # NEW - work sessions
│   ├── 2025-11.md
│   └── active.yaml
├── daily/             # NEW - daily plans & reviews
│   └── 2025-11-06.md
├── reviews/           # NEW - weekly/monthly
│   ├── weekly/
│   └── monthly/
└── .meta/             # Enhanced - caches
    ├── projects.json
    ├── tasks.json
    ├── sessions.json
    └── analytics.json
```

---

## Success Metrics

### Behavioral Changes
- More projects completed per month
- Less time wondering "what was I doing?"
- More regular breaks (prevent burnout)
- Better time estimates (awareness)
- Consistent daily use

### Subjective Improvements
- Feel less guilty about unfinished work
- Know what to work on next
- Resume work easily after interruptions
- Feel supported, not judged
- Celebrate wins more

### System Health
- Daily active usage
- Feature adoption (which commands used)
- Performance (<2 sec per command)
- Data integrity (no corruption)

---

## What JOURNEL Is NOT

**Not a full PM system** - No Gantt charts, dependencies, resource allocation

**Not a time tracker** - Rough logging, not billable hours

**Not an IDE** - No code integration, stays simple

**Not multi-user** - Personal tool only

**Not AI-powered** - Data is AI-readable, but system is deterministic

**Not rigid** - Flexible scaffolding, not enforced workflows

---

## The North Star

JOURNEL becomes the **ultimate ADHD accountability buddy**:

- Tracks your work (without friction)
- Remembers for you (external memory)
- Protects your health (break reminders)
- Celebrates your wins (dopamine)
- Learns your patterns (insights)
- Supports your focus (one thing at a time)
- Forgives your gaps (easy re-entry)
- Integrates with your world (calendar, git, LLM)

**It works WITH your ADHD brain, not against it.**

---

## Next Steps

1. **Read the comprehensive design** (`COMPREHENSIVE_SYSTEM_DESIGN.md`)
   - Full feature specifications
   - Psychological rationale
   - Complete workflows

2. **Review the roadmap** (`IMPLEMENTATION_ROADMAP.md`)
   - Phased implementation plan
   - Week-by-week breakdown
   - Success criteria

3. **Understand the principles** (`ADHD_DESIGN_PRINCIPLES.md`)
   - Why each feature exists
   - ADHD research foundation
   - Design patterns and anti-patterns

4. **Start building Phase 1**
   - Session tracking (time awareness)
   - Today mode (daily focus)
   - Enhanced status (visibility)

---

## Remember

**Better to build half of this well than all of it poorly.**

Start with the most ADHD-critical features:
1. Time awareness (sessions)
2. Daily focus (today mode)
3. Break support (hyperfocus protection)

Then expand based on real-world usage and feedback.

The goal is a tool you'll actually use because it makes your life easier, not another abandoned productivity system.

---

**JOURNEL: Your external working memory. Your accountability buddy. Your path to finishing what you start.**
