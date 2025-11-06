# JOURNEL Implementation Roadmap
## From Project Tracker to Executive Function Support System

---

## Current State Assessment

### What JOURNEL Has Today (v0.2.0)

**Core Features:**
- ✅ Project creation with gate-keeping
- ✅ Status overview (active/dormant/completed)
- ✅ Quick logging (`jnl log`)
- ✅ Context export for LLM (`jnl ctx`)
- ✅ Project completion ritual (`jnl done`)
- ✅ Resume with context (`jnl resume`)
- ✅ Git integration (auto-commit)
- ✅ Interactive TUI mode
- ✅ Plain text storage (Markdown + YAML)

**Data Model:**
- Project (with metadata, tags, notes)
- LogEntry (date, project, message, hours)
- Storage layer (file I/O, git)
- Config management

**What Works Well:**
- Simple commands (2-3 words)
- Plain text storage
- Gate-keeping (prevents overcommitment)
- Completion celebration
- LLM integration

### Critical Gaps for ADHD Support

**Missing Time Awareness:**
- ❌ No session tracking (how long am I working?)
- ❌ No break reminders (hyperfocus protection)
- ❌ No "elapsed time" visibility
- ❌ No deadline/urgency support

**Missing Daily Focus:**
- ❌ No "today" mode (what matters right now?)
- ❌ No daily planning workflow
- ❌ No focus item selection (1-3 priorities)
- ❌ No daily review/reflection

**Missing Context Restoration:**
- ❌ No session pause/resume
- ❌ No "where was I?" after interruption
- ❌ Limited resume context (just next_steps)

**Missing Overwhelm Prevention:**
- ❌ No micro-task breakdown
- ❌ Projects feel too big
- ❌ No clear "next action"
- ❌ No energy-aware suggestions

**Missing Pattern Learning:**
- ❌ No energy tracking
- ❌ No work pattern analysis
- ❌ No insights/suggestions
- ❌ No weekly/monthly reviews

**Missing Integration:**
- ❌ No calendar awareness
- ❌ No system notifications
- ❌ No external tool hooks

---

## Phased Implementation Plan

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Add critical ADHD features to existing system

#### Week 1: Session Tracking & Time Awareness

**New Commands:**
```bash
jnl start <project> [task]    # Start work session
jnl stop                       # End session
jnl status-now                 # Show active session
jnl pause                      # Pause current session
jnl continue                   # Resume paused session
```

**Implementation Tasks:**
1. Create `Session` model
   ```python
   @dataclass
   class Session:
       id: str
       project_id: str
       task: str
       start_time: datetime
       end_time: Optional[datetime]
       paused_at: Optional[datetime]
       pause_duration: timedelta
   ```

2. Create `SessionManager` class
   - Track active session (singleton)
   - Save to `sessions/active.yaml`
   - Append to `sessions/YYYY-MM.md` on completion

3. Add session display to `status` command
   ```
   ⏱️  Active: geoprops (2h 18m) - Writing API docs
   ```

4. Update `log` command to link to active session

**Files to Modify:**
- `src/journel/models.py` - Add Session class
- `src/journel/storage.py` - Add session storage methods
- `src/journel/cli.py` - Add start/stop/pause commands
- `src/journel/display.py` - Add session display

**Files to Create:**
- `src/journel/session.py` - SessionManager class

**Testing:**
- Start session, verify saved to `sessions/active.yaml`
- Stop session, verify appended to monthly log
- Pause/resume, verify duration tracking
- Multiple starts without stop, verify warning

#### Week 2: Today Mode & Daily Planning

**New Commands:**
```bash
jnl today                      # Daily dashboard (default in morning)
jnl focus <task>               # Set today's focus
jnl focus add <task>           # Add to today (max 3)
jnl focus clear                # Clear today's list
jnl wins                       # Today's wins (enhanced)
```

**Implementation Tasks:**
1. Create `DailyPlan` model
   ```python
   @dataclass
   class DailyPlan:
       date: date
       focus_items: List[str]  # Max 3
       wins: List[str]
       reflection: str
       energy_level: Optional[int]
   ```

2. Create `jnl today` command (interactive)
   - Show yesterday's wins
   - Show active projects
   - Prompt for today's focus (max 3)
   - Show calendar (if integrated)
   - Suggest priorities

3. Enhance `jnl wins` to show today's completions

4. Add daily file: `daily/YYYY-MM-DD.md`

**Files to Modify:**
- `src/journel/models.py` - Add DailyPlan class
- `src/journel/storage.py` - Add daily plan storage
- `src/journel/cli.py` - Add today/focus commands
- `src/journel/display.py` - Add today dashboard

**Testing:**
- Run `jnl today`, verify creates daily file
- Set focus items, verify saved
- Exceed 3 items, verify warning
- Show wins, verify today's logs displayed

**Deliverable:**
- User can start/stop work sessions
- User can see elapsed time
- User can plan their day (1-3 focus items)
- User sees yesterday's wins for motivation

---

### Phase 2: Focus & Flow (Weeks 3-5)
**Goal:** Support deep work and prevent burnout

#### Week 3: Break Management

**New Commands:**
```bash
jnl break [minutes]            # Start break timer
jnl remind-breaks [interval]   # Set reminder frequency
```

**Implementation Tasks:**
1. Add break tracking to Session
   ```python
   breaks: List[Break] = field(default_factory=list)

   @dataclass
   class Break:
       start: datetime
       duration: timedelta
       type: str  # stretch, walk, water, etc.
   ```

2. Background break reminders
   - Check session duration every 30 sec
   - Show gentle reminder at configurable interval (default 90 min)
   - Don't interrupt if user is typing

3. Break timer with progress bar
   ```
   ⏱️  Break timer: 10 minutes
      [████░░░░░░░░] 3 min remaining
   ```

4. Add to config:
   ```yaml
   session:
     break_reminder_interval: 90  # minutes
     auto_pause_inactive: 30  # minutes
   ```

**Files to Modify:**
- `src/journel/models.py` - Add Break class
- `src/journel/session.py` - Add break tracking
- `src/journel/cli.py` - Add break commands
- `src/journel/config.py` - Add session settings

**Testing:**
- Start session, wait 90 min, verify reminder
- Take break, verify tracked
- Multiple breaks, verify cumulative duration
- Auto-pause on inactivity

#### Week 4: Enhanced Context & Switching

**New Commands:**
```bash
jnl resume-last                # Resume last worked project
jnl switch <project>           # Switch project (save context)
jnl quick-start                # Start most important project
```

**Implementation Tasks:**
1. Enhanced resume context
   - Show last 3 commits (not just 1)
   - Show active Claude conversations
   - Show recent notes/blockers
   - Show related files changed
   - Estimate time to milestone

2. Context preservation on switch
   - Save current state when switching
   - Restore full context on resume
   - Track context switches

3. Smart suggestions
   - Analyze urgency, completion %, last worked
   - Suggest "best" project to start
   - Explain reasoning

**Files to Modify:**
- `src/journel/cli.py` - Add resume-last, switch, quick-start
- `src/journel/display.py` - Enhanced resume display
- `src/journel/storage.py` - Git integration improvements
- `src/journel/utils.py` - Add suggestion logic

**Testing:**
- Resume project, verify shows multiple commits
- Switch projects, verify context saved
- Resume-last, verify returns to previous
- Quick-start, verify suggests correct project

#### Week 5: Energy Tracking

**New Commands:**
```bash
jnl energy <level>             # Log energy (1-5)
jnl energy-check               # Quick check-in
jnl patterns                   # Show energy patterns
```

**Implementation Tasks:**
1. Add energy tracking
   - Prompt at session start/end (optional)
   - Log with session data
   - Store in daily plan

2. Energy pattern analysis
   - Best work times by energy level
   - Energy trends over week
   - Correlate with productivity

3. Energy-aware suggestions
   - "Low energy → try documentation tasks"
   - "High energy mornings → tackle hard problems"

**Files to Modify:**
- `src/journel/models.py` - Add energy to Session, DailyPlan
- `src/journel/cli.py` - Add energy commands
- `src/journel/display.py` - Show energy patterns

**Files to Create:**
- `src/journel/analytics.py` - Pattern analysis

**Testing:**
- Log energy, verify stored
- View patterns, verify analysis
- Suggestions based on energy

**Deliverable:**
- User takes regular breaks
- User tracks energy levels
- User gets smart project suggestions
- User can switch contexts easily

---

### Phase 3: Micro-Tasks & Urgency (Weeks 6-7)
**Goal:** Reduce overwhelm, leverage urgency

#### Week 6: Task Management

**New Commands:**
```bash
jnl tasks <project>            # Show project tasks
jnl task add <project> "task"  # Add micro-task
jnl task done <id>             # Complete task
jnl task next <project>        # Show next action
```

**Implementation Tasks:**
1. Create `Task` model
   ```python
   @dataclass
   class Task:
       id: str
       project_id: str
       description: str
       created: date
       completed: Optional[date]
       estimated_minutes: Optional[int]
       priority: int  # 1-5
       next_action: bool  # Is this THE next thing?
   ```

2. Task storage
   - Store in project frontmatter
   - Also cache in `.meta/tasks.json`

3. Auto-generate tasks from next_steps
   - Parse next_steps on project load
   - Suggest breaking into tasks

4. Task completion → project progress
   - Update completion % automatically
   - Celebrate task completion

**Files to Modify:**
- `src/journel/models.py` - Add Task class
- `src/journel/storage.py` - Task storage
- `src/journel/cli.py` - Add task commands

**Testing:**
- Add tasks, verify stored
- Complete task, verify marked
- Show next action, verify correct priority
- Task completion updates project %

#### Week 7: Deadlines & Urgency

**New Commands:**
```bash
jnl deadline <project> <date>  # Set deadline
jnl due                        # Show items due soon
jnl urgent <project>           # Mark urgent
```

**Implementation Tasks:**
1. Add deadline support
   ```python
   deadline: Optional[date] = None
   urgency: int = 1  # 1-5, auto-calculated from deadline
   ```

2. Visual urgency indicators
   - 🔴 Due today
   - 🟡 Due this week
   - 🔵 Due later
   - 🔥 User-marked urgent

3. Deadline-aware suggestions
   - Auto-prioritize approaching deadlines
   - Warn if deadline approaching
   - Escalating urgency as deadline nears

4. `jnl due` view
   - Show all upcoming deadlines
   - Sort by proximity
   - Estimate if achievable

**Files to Modify:**
- `src/journel/models.py` - Add deadline, urgency
- `src/journel/cli.py` - Add deadline commands
- `src/journel/display.py` - Urgency indicators
- `src/journel/utils.py` - Urgency calculation

**Testing:**
- Set deadline, verify stored
- Approaching deadline, verify urgency increases
- Due today, verify highlighted
- Overdue, verify visual warning

**Deliverable:**
- Projects broken into clear tasks
- Deadlines visible and motivating
- Task initiation easier (clear next action)
- Urgency leveraged positively

---

### Phase 4: Patterns & Insights (Weeks 8-9)
**Goal:** Learn from behavior, provide guidance

#### Week 8: Review System

**New Commands:**
```bash
jnl review                     # Daily review (interactive)
jnl review weekly              # Weekly review
jnl review month               # Monthly review
```

**Implementation Tasks:**
1. Daily review flow
   - What did I accomplish?
   - What did I learn?
   - How did I feel? (energy)
   - What matters tomorrow?

2. Weekly review
   - Progress by project
   - Time distribution
   - Completions
   - Energy patterns
   - Insights

3. Monthly review
   - Completions this month
   - Long-term trends
   - Goal alignment
   - System adjustments

4. Store reviews in `reviews/` directory

**Files to Create:**
- `src/journel/review.py` - Review workflows

**Files to Modify:**
- `src/journel/cli.py` - Add review commands
- `src/journel/display.py` - Review displays

**Testing:**
- Run daily review, verify prompts
- Run weekly review, verify stats
- Run monthly review, verify trends

#### Week 9: Analytics & Insights

**New Commands:**
```bash
jnl insights                   # AI-generated insights
jnl patterns                   # Work pattern analysis
jnl forecast                   # Completion predictions
jnl streak                     # Show streaks
```

**Implementation Tasks:**
1. Pattern detection
   - Best work times
   - Most productive days
   - Session length patterns
   - Energy correlations
   - Completion velocity

2. Insight generation
   - Rule-based initially
   - Personalized tips
   - Pattern-based suggestions
   - Transparent reasoning

3. Completion forecasting
   - Based on velocity
   - Account for energy patterns
   - Show confidence level

4. Streak tracking
   - Daily logging
   - Work sessions
   - Completions
   - Reviews

**Files to Modify:**
- `src/journel/analytics.py` - Enhanced analytics
- `src/journel/cli.py` - Add insight commands
- `src/journel/display.py` - Insight displays

**Testing:**
- Generate insights, verify relevant
- Forecast completion, verify reasonable
- Show patterns, verify accurate
- Track streaks, verify counting

**Deliverable:**
- User does regular reviews
- User sees patterns in work
- User gets actionable insights
- User adjusts behavior based on data

---

### Phase 5: Integration & Polish (Weeks 10-12)
**Goal:** Connect to external world, refine UX

#### Week 10: Calendar Integration

**New Commands:**
```bash
jnl cal sync                   # Sync with calendar
jnl cal show                   # Show today's calendar
jnl cal block <project> <time> # Block focus time
```

**Implementation Tasks:**
1. Calendar provider abstraction
   - Google Calendar API
   - Outlook/Exchange
   - iCal file

2. Read calendar events
   - Show in `jnl today`
   - Calculate available time
   - Suggest work around meetings

3. Optional: Write to calendar
   - Block focus time
   - Add project deadlines

**Files to Create:**
- `src/journel/integrations/calendar.py`

**Files to Modify:**
- `src/journel/config.py` - Calendar settings
- `src/journel/cli.py` - Cal commands

**Testing:**
- Sync calendar, verify events loaded
- Show today, verify includes calendar
- Block time, verify event created

#### Week 11: Enhanced Git & Notifications

**New Commands:**
```bash
jnl commits <project>          # Recent commits
jnl commit-log                 # Auto-log from commits
jnl notify <message>           # System notification
```

**Implementation Tasks:**
1. Enhanced git integration
   - Parse commits for auto-logging
   - Detect active development
   - Link commits to sessions

2. System notifications
   - Break reminders
   - Deadline warnings
   - Completion celebrations
   - Session milestones

3. Cross-platform notification support
   - Windows: win10toast
   - macOS: osascript
   - Linux: notify-send

**Files to Create:**
- `src/journel/integrations/git.py`
- `src/journel/integrations/notifications.py`

**Files to Modify:**
- `src/journel/cli.py` - Git commands
- `src/journel/session.py` - Notification hooks

**Testing:**
- Auto-log commits, verify parsing
- Show commits, verify display
- Send notification, verify cross-platform

#### Week 12: Hooks & Polish

**New Commands:**
```bash
jnl hook add <event> <command> # Custom hooks
jnl export <format>            # Export data
jnl profile <name>             # Load config profile
```

**Implementation Tasks:**
1. Webhook system
   - Events: session_start, session_end, break_reminder, completion
   - Execute shell commands
   - Pass event data

2. Export formats
   - JSON (full data)
   - CSV (logs, sessions)
   - Markdown (reports)

3. Configuration profiles
   - Presets: deep-work, chaotic, creative
   - User-defined profiles
   - Quick switching

4. UX polish
   - Consistent error messages
   - Help text improvements
   - Loading indicators
   - Progress bars

**Files to Create:**
- `src/journel/hooks.py`
- `src/journel/export.py`
- `src/journel/profiles.py`

**Files to Modify:**
- All display functions (polish)
- All commands (consistent UX)

**Testing:**
- Add hook, verify executes
- Export data, verify formats
- Switch profile, verify config changes

**Deliverable:**
- Calendar shows available time
- Git commits enhance context
- System notifications work
- Hooks enable customization
- UX is polished and consistent

---

## Post-Launch: Phase 6+ (Ongoing)

### Intelligence & Optimization

**Smart Features:**
- ML-based pattern detection (optional)
- Automatic task breakdown suggestions
- Burnout detection/prevention
- Personalized tip generation
- Habit formation tracking

**Advanced Integrations:**
- Todoist/Things/OmniFocus
- Obsidian vault sync
- GitHub Actions
- Slack/Discord webhooks
- Email summaries

**Mobile & Web:**
- Mobile companion (view-only)
- Web dashboard (optional)
- Voice capture
- Quick entry widgets

---

## Implementation Guidelines

### For Each Phase

**Before Starting:**
1. Review ADHD design principles
2. Identify core user benefit
3. Design minimal viable version
4. Plan testing approach

**During Development:**
1. Build simplest version first
2. Test with real ADHD users
3. Measure time-to-action
4. Iterate based on feedback

**Before Releasing:**
1. Documentation updated
2. Examples added
3. Tests passing
4. Performance acceptable (<2 sec/command)
5. Works offline

### Code Quality Standards

**Every Feature:**
- Solves specific ADHD challenge (document which)
- <2 second command execution
- Graceful degradation if offline
- Comprehensive error handling
- Undo/recovery support

**Every Command:**
- Simple syntax (2-3 words)
- Immediate feedback
- Consistent with existing commands
- Help text with examples
- Tab completion support

### Testing Strategy

**Unit Tests:**
- Models (serialization, validation)
- Storage (read/write, git)
- Analytics (calculations)
- Utilities (parsing, formatting)

**Integration Tests:**
- Command workflows
- Data persistence
- Git operations
- File structure

**User Testing:**
- Real ADHD users
- Common workflows
- Error scenarios
- Performance under load

---

## Risk Mitigation

### Technical Risks

**Risk:** Session tracking breaks if process killed
- **Mitigation:** Save session state every 30 seconds
- **Recovery:** Detect orphaned sessions on next start

**Risk:** Git conflicts on sync
- **Mitigation:** Clear conflict resolution UI
- **Recovery:** Keep local backup before sync

**Risk:** Performance degrades with many projects
- **Mitigation:** Lazy loading, caching
- **Recovery:** Archive old projects

**Risk:** Calendar integration complexity
- **Mitigation:** Make optional, support multiple providers
- **Recovery:** Graceful fallback if unavailable

### User Experience Risks

**Risk:** Too many features, overwhelming
- **Mitigation:** Progressive disclosure, good defaults
- **Recovery:** Simple/advanced modes

**Risk:** Users abandon after initial enthusiasm
- **Mitigation:** Gentle re-engagement, easy re-entry
- **Recovery:** "Welcome back" flow

**Risk:** Breaks existing workflows
- **Mitigation:** Backwards compatibility, migration guide
- **Recovery:** Version pinning, rollback support

---

## Success Criteria

### Phase 1 Success
- [ ] User can track work sessions
- [ ] User sees time elapsed while working
- [ ] User can plan their day (1-3 items)
- [ ] User sees yesterday's wins
- [ ] Commands remain <2 seconds

### Phase 2 Success
- [ ] User takes regular breaks
- [ ] User tracks energy patterns
- [ ] User switches contexts easily
- [ ] User gets smart suggestions
- [ ] Break reminders are helpful, not annoying

### Phase 3 Success
- [ ] Projects broken into tasks
- [ ] Task initiation friction reduced
- [ ] Deadlines visible and motivating
- [ ] Urgency leveraged positively
- [ ] User completes more micro-tasks

### Phase 4 Success
- [ ] User does daily reviews
- [ ] User sees work patterns
- [ ] User gets actionable insights
- [ ] User adjusts behavior from data
- [ ] Reviews take <5 minutes

### Phase 5 Success
- [ ] Calendar integration works
- [ ] Notifications are helpful
- [ ] Hooks enable customization
- [ ] UX feels polished
- [ ] System integrates with workflow

---

## Resources Needed

### Development
- Python 3.8+ environment
- Test suite infrastructure
- CI/CD pipeline
- Documentation platform

### Design
- ADHD user research
- Usability testing
- Accessibility review
- Visual design (terminal UI)

### External
- Calendar API access (Google, Outlook)
- Notification library testing
- Cross-platform testing environments
- Beta user group

---

## Next Immediate Steps

1. **Review design document** with stakeholders
2. **Set up Phase 1 development environment**
3. **Create Session model** (first implementation task)
4. **Build `jnl start/stop` commands**
5. **Add session display to status**
6. **Test with real usage**
7. **Iterate based on feedback**

---

**Remember:** Build iteratively, test continuously, prioritize ADHD-critical features, keep it simple.

The goal is not to build everything at once, but to build the most impactful features well, learning and adjusting as we go.
