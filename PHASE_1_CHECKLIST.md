# Phase 1 Implementation Checklist
## Session Tracking & Today Mode (Weeks 1-2)

---

## Overview

**Goal:** Add critical ADHD features for time awareness and daily focus

**Duration:** 2 weeks

**Success Criteria:**
- [ ] User can track work sessions with elapsed time
- [ ] User can see active session in status
- [ ] User can plan their day with `jnl today`
- [ ] User sees yesterday's wins for motivation
- [ ] All commands execute in <2 seconds

---

## Week 1: Session Tracking & Time Awareness

### Day 1-2: Session Model & Storage

**Tasks:**
- [ ] Create `Session` dataclass in `models.py`
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
      notes: str = ""
  ```

- [ ] Add session directory to storage structure
  ```python
  # In storage.py init_structure()
  (self.journel_dir / "sessions").mkdir(exist_ok=True)
  ```

- [ ] Create `sessions/active.yaml` save/load methods
  ```python
  def save_active_session(self, session: Session)
  def load_active_session(self) -> Optional[Session]
  def clear_active_session(self)
  ```

- [ ] Create session log append method
  ```python
  def append_session_to_log(self, session: Session)
  # Appends to sessions/YYYY-MM.md
  ```

**Testing:**
- [ ] Create session, save to active.yaml, verify file contents
- [ ] Load session, verify all fields restored
- [ ] Clear session, verify file removed
- [ ] Append to log, verify markdown formatting

**Files Modified:**
- `src/journel/models.py`
- `src/journel/storage.py`

**Files Created:**
- None (using existing files)

---

### Day 3-4: SessionManager Class

**Tasks:**
- [ ] Create `src/journel/session.py`
- [ ] Implement `SessionManager` singleton
  ```python
  class SessionManager:
      _instance = None

      def __init__(self, storage: Storage):
          self.storage = storage
          self.active_session: Optional[Session] = None
          self.load_active_session()

      @classmethod
      def get_instance(cls, storage: Storage):
          if cls._instance is None:
              cls._instance = cls(storage)
          return cls._instance
  ```

- [ ] Implement core session methods:
  ```python
  def start_session(self, project: Project, task: str) -> Session
  def stop_session(self) -> Session
  def pause_session(self) -> Session
  def resume_session(self) -> Session
  def get_active_session(self) -> Optional[Session]
  def get_elapsed_time(self) -> timedelta
  ```

- [ ] Add context snapshot on start
  ```python
  # Save: current git branch, last commit, open files, etc.
  ```

- [ ] Handle edge cases:
  - Start when already active (warn, or force stop previous)
  - Stop when nothing active (graceful error)
  - Pause when not active
  - Resume when not paused

**Testing:**
- [ ] Start session, verify active_session set
- [ ] Get elapsed time, verify accurate
- [ ] Stop session, verify saved to log
- [ ] Pause/resume, verify pause_duration tracked
- [ ] Handle double-start gracefully

**Files Created:**
- `src/journel/session.py`

---

### Day 5-6: Session Commands

**Tasks:**
- [ ] Add `start` command to `cli.py`
  ```python
  @main.command()
  @click.argument("project")
  @click.argument("task", required=False)
  @click.pass_context
  def start(ctx, project, task):
      """Start a work session."""
  ```

- [ ] Add `stop` command
  ```python
  @main.command()
  @click.pass_context
  def stop(ctx):
      """End current work session."""
      # Prompt: "What did you accomplish?" (optional)
  ```

- [ ] Add `pause` command
  ```python
  @main.command()
  @click.pass_context
  def pause(ctx):
      """Pause current session."""
  ```

- [ ] Add `continue` command (or `resume` subcommand)
  ```python
  @main.command()
  @click.pass_context
  def continue_session(ctx):
      """Resume paused session."""
  ```

- [ ] Add `status-now` command
  ```python
  @main.command(name="status-now")
  @click.pass_context
  def status_now(ctx):
      """Show current session status."""
  ```

- [ ] Implement display functions in `display.py`:
  ```python
  def print_session_started(session: Session, project: Project)
  def print_session_stopped(session: Session, project: Project)
  def print_session_paused(session: Session)
  def print_session_resumed(session: Session)
  def print_session_status(session: Session, project: Project)
  ```

**Testing:**
- [ ] Run `jnl start project`, verify session started
- [ ] Run `jnl status-now`, verify shows active session
- [ ] Run `jnl pause`, verify paused
- [ ] Run `jnl continue`, verify resumed
- [ ] Run `jnl stop`, verify saved and cleared

**Files Modified:**
- `src/journel/cli.py`
- `src/journel/display.py`

---

### Day 7: Integrate Sessions with Status

**Tasks:**
- [ ] Modify `status` command to show active session
  ```python
  # In print_status(), add:
  if active_session:
      console.print(f"\n⏱️  Active: {project.name} ({elapsed}) - {session.task}")
  ```

- [ ] Add elapsed time formatting utility
  ```python
  # In utils.py
  def format_duration(td: timedelta) -> str:
      """Format timedelta as '2h 30m' or '45m' or '3h'"""
  ```

- [ ] Update `log` command to link to active session
  ```python
  # If session active, add session_id to log entry
  ```

- [ ] Test end-to-end workflow:
  - Start session
  - Check status (shows active)
  - Log work (links to session)
  - Stop session (saves with logs)

**Testing:**
- [ ] Start session, run `jnl`, verify shows active session
- [ ] Log message, verify linked to session
- [ ] Stop session, verify session log includes messages
- [ ] No active session, verify status doesn't show session line

**Files Modified:**
- `src/journel/cli.py` (status command)
- `src/journel/display.py` (print_status)
- `src/journel/utils.py` (format_duration)

---

## Week 2: Today Mode & Daily Planning

### Day 8-9: DailyPlan Model & Storage

**Tasks:**
- [ ] Create `DailyPlan` dataclass in `models.py`
  ```python
  @dataclass
  class DailyPlan:
      date: date
      focus_items: List[str]  # Max 3
      wins: List[str] = field(default_factory=list)
      reflection: str = ""
      energy_level: Optional[int] = None
      calendar_events: List[dict] = field(default_factory=list)
  ```

- [ ] Add daily directory to storage structure
  ```python
  (self.journel_dir / "daily").mkdir(exist_ok=True)
  ```

- [ ] Add daily plan save/load methods
  ```python
  def save_daily_plan(self, plan: DailyPlan)
  def load_daily_plan(self, date: date) -> Optional[DailyPlan]
  def get_today_plan(self) -> DailyPlan
  def get_yesterday_plan(self) -> Optional[DailyPlan]
  ```

- [ ] Define daily file format
  ```markdown
  ---
  date: 2025-11-06
  focus_items:
    - Finish geoprops API docs
    - Fix MICA deployment
  energy_level: 4
  ---

  ## Focus

  1. Finish geoprops API docs
  2. Fix MICA deployment

  ## Wins

  - Completed API documentation
  - Fixed production bug

  ## Reflection

  Felt great finishing geoprops!
  ```

**Testing:**
- [ ] Create daily plan, save to file
- [ ] Load daily plan, verify all fields
- [ ] Get today's plan (creates if missing)
- [ ] Get yesterday's plan (returns None if doesn't exist)

**Files Modified:**
- `src/journel/models.py`
- `src/journel/storage.py`

---

### Day 10-11: Today Command (Interactive)

**Tasks:**
- [ ] Create `today` command in `cli.py`
  ```python
  @main.command()
  @click.option("--plan", is_flag=True, help="Interactive planning mode")
  @click.pass_context
  def today(ctx, plan):
      """Show today's dashboard and plan."""
  ```

- [ ] Implement today dashboard display
  ```python
  # In display.py
  def print_today_dashboard(
      today_plan: DailyPlan,
      yesterday_plan: Optional[DailyPlan],
      active_projects: List[Project],
      active_session: Optional[Session]
  ):
      # Show:
      # - Yesterday's wins (if any)
      # - Active projects summary
      # - Today's focus items
      # - Calendar events (placeholder for now)
      # - Suggestions
  ```

- [ ] Implement interactive planning flow
  ```python
  # Prompt for focus items (max 3)
  # Suggest based on:
  #   - Projects close to completion
  #   - Projects with deadlines soon
  #   - Projects worked on recently
  ```

- [ ] Add focus item management
  ```python
  # Helper functions:
  def add_focus_item(plan: DailyPlan, item: str) -> bool
      # Returns False if already 3 items
  def remove_focus_item(plan: DailyPlan, index: int)
  def clear_focus_items(plan: DailyPlan)
  ```

**Testing:**
- [ ] Run `jnl today`, verify shows dashboard
- [ ] Run `jnl today --plan`, verify interactive prompts
- [ ] Add 3 focus items, verify saved
- [ ] Try to add 4th, verify warned
- [ ] Check yesterday's wins show up

**Files Modified:**
- `src/journel/cli.py`
- `src/journel/display.py`

**Files Created:**
- None (might create `src/journel/planning.py` if logic gets complex)

---

### Day 12-13: Focus & Wins Commands

**Tasks:**
- [ ] Add `focus` command group
  ```python
  @main.group()
  def focus():
      """Manage today's focus items."""

  @focus.command(name="add")
  @click.argument("item")
  def focus_add(item):
      """Add item to today's focus."""

  @focus.command(name="clear")
  def focus_clear():
      """Clear today's focus items."""

  @focus.command(name="list")
  def focus_list():
      """Show today's focus items."""
  ```

- [ ] Enhance existing `wins` command
  ```python
  # Modify to show TODAY's wins prominently
  # Then show recent completions
  # Pull wins from:
  #   - Today's daily plan
  #   - Today's log entries
  #   - Projects completed today
  ```

- [ ] Add win capture helper
  ```python
  def add_win(storage: Storage, win: str):
      """Add win to today's plan."""
  ```

**Testing:**
- [ ] Run `jnl focus add "item"`, verify added
- [ ] Run `jnl focus list`, verify shows items
- [ ] Run `jnl focus clear`, verify cleared
- [ ] Run `jnl wins`, verify shows today's wins first

**Files Modified:**
- `src/journel/cli.py`
- `src/journel/display.py`

---

### Day 14: Integration & Polish

**Tasks:**
- [ ] Update `log` command to auto-add to wins
  ```python
  # If log message starts with "Completed" or "Finished"
  # Prompt: "Add to today's wins? [Y/n]"
  ```

- [ ] Update `done` command to add to wins
  ```python
  # When project completed, automatically add to today's wins
  ```

- [ ] Add yesterday's wins to morning greeting
  ```python
  # First command of day shows yesterday's wins
  # Use config: show_daily_greeting = true
  ```

- [ ] Performance optimization
  ```python
  # Cache today's plan in memory
  # Only reload from disk if date changed
  ```

- [ ] Error handling polish
  ```python
  # Graceful handling of:
  # - Missing daily files
  # - Corrupted YAML
  # - Invalid date formats
  ```

- [ ] Help text and examples
  ```python
  # Update all new commands with clear help
  # Add usage examples to README
  ```

**Testing:**
- [ ] Complete a task, verify prompts for wins
- [ ] Complete a project, verify auto-adds to wins
- [ ] Run first command of day, verify shows yesterday
- [ ] All commands execute in <2 seconds
- [ ] Help text is clear and helpful

**Files Modified:**
- `src/journel/cli.py`
- `src/journel/display.py`
- `src/journel/config.py`
- `README.md`

---

## Documentation Updates

**After Week 1:**
- [ ] Update README with session commands
- [ ] Add examples of session workflow
- [ ] Document session file format

**After Week 2:**
- [ ] Update README with today mode
- [ ] Add examples of daily planning workflow
- [ ] Document daily file format
- [ ] Create migration guide (if needed)

**Files to Update:**
- `README.md` - User-facing docs
- `CHANGELOG.md` - Version history
- Docstrings in code

---

## Testing Checklist

### Unit Tests
- [ ] Session model serialization
- [ ] DailyPlan model serialization
- [ ] SessionManager session lifecycle
- [ ] Storage save/load methods
- [ ] Duration formatting utility

### Integration Tests
- [ ] Start → Status → Stop workflow
- [ ] Start → Pause → Continue → Stop workflow
- [ ] Today planning → Focus items → Wins workflow
- [ ] Log → Auto-link to session
- [ ] Done → Auto-add to wins

### Manual Testing
- [ ] Start session, leave running overnight, verify duration
- [ ] Multiple pause/resume cycles
- [ ] Force quit during session, verify recovery
- [ ] Corrupted active.yaml, verify graceful handling
- [ ] Today mode with no projects yet

### Performance Testing
- [ ] All commands execute in <2 seconds
- [ ] Status with 20+ projects and active session
- [ ] Load today's plan 100 times (caching test)

---

## Success Criteria Verification

**Before marking Phase 1 complete:**

- [ ] **Session Tracking Works**
  - Start/stop/pause/continue commands functional
  - Elapsed time accurate
  - Sessions saved to monthly logs
  - Active session shows in status

- [ ] **Today Mode Works**
  - Dashboard shows yesterday's wins
  - Can set 1-3 focus items
  - Suggestions are helpful
  - Wins are captured

- [ ] **Integration Complete**
  - Logs link to sessions
  - Completions add to wins
  - Status shows active session
  - Performance acceptable

- [ ] **User Experience Good**
  - Commands are intuitive
  - Help text is clear
  - Error messages are helpful
  - Displays are attractive

- [ ] **Ready for Real Use**
  - Developer (you) can use it daily
  - No major bugs
  - Data doesn't corrupt
  - Easy to understand

---

## Post-Phase 1

### Gather Feedback
- [ ] Use JOURNEL for 1 week yourself
- [ ] Note friction points
- [ ] Track which features get used
- [ ] Identify missing pieces

### Plan Phase 2
- [ ] Prioritize break management vs. energy tracking
- [ ] Design break reminder system
- [ ] Plan context switching improvements

### Documentation
- [ ] Write blog post about Phase 1
- [ ] Create video demo
- [ ] Share with ADHD community for feedback

---

## Quick Reference - New Commands Added

```bash
# Session commands
jnl start <project> [task]    # Start work session
jnl stop                       # End session
jnl pause                      # Pause session
jnl continue                   # Resume session
jnl status-now                 # Show active session

# Today commands
jnl today                      # Daily dashboard
jnl today --plan               # Interactive planning
jnl focus add <item>           # Add to today (max 3)
jnl focus clear                # Clear focus items
jnl focus list                 # Show focus items

# Enhanced existing
jnl wins                       # Shows today's wins first
jnl status                     # Shows active session
jnl log "msg"                  # Links to active session
```

---

## Files Modified/Created Summary

### Created
- `src/journel/session.py` - SessionManager class

### Modified
- `src/journel/models.py` - Add Session, DailyPlan
- `src/journel/storage.py` - Add session/daily storage
- `src/journel/cli.py` - Add all new commands
- `src/journel/display.py` - Add new display functions
- `src/journel/utils.py` - Add format_duration
- `src/journel/config.py` - Add session settings
- `README.md` - Document new features

### Directory Structure Changes
```
~/.journel/
├── sessions/          # NEW
│   ├── 2025-11.md
│   └── active.yaml
└── daily/             # NEW
    └── 2025-11-06.md
```

---

**Ready to start? Begin with Day 1: Session Model & Storage!**

Each day is 2-4 hours of work. Take your time, test thoroughly, and don't rush.

The goal is solid foundations for the rest of the system.
