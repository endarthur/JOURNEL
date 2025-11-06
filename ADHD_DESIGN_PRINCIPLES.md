# ADHD-First Design Principles for JOURNEL
## The Psychology Behind Every Feature

---

## Core Philosophy

**JOURNEL is not a productivity tool. It's an executive function support system.**

Traditional productivity tools assume you have:
- Working memory to remember what you were doing
- Task initiation ability to start without friction
- Time awareness to know how long you've worked
- Sustained attention to work without breaks
- Motivation that doesn't require external rewards

**ADHD brains don't work that way.** JOURNEL is designed for how we actually function.

---

## The 10 ADHD Design Principles

### 1. Zero Friction - Make the Right Thing the Easiest Thing

**Problem:** ADHD brains struggle with task initiation. Any friction = won't happen.

**Solution:**
- Commands are 2-3 words max
- Capture in <5 seconds (thought to written)
- No required fields (capture first, organize later)
- Defaults for everything
- Keyboard-only, no mouse required

**Examples:**
```bash
jnl log "fixed bug"           # Not: journel create-log-entry --project=X --time=Y
jnl start                      # Starts most important thing automatically
jnl resume                     # One command, full context restored
```

**Why it works:** Lower activation energy = higher completion rate. The easier it is, the more likely we'll do it.

---

### 2. External Memory - Never Rely on Remembering

**Problem:** Working memory deficits mean we forget what we were doing, what's next, what's urgent.

**Solution:**
- Everything written down immediately
- Context always visible
- No memorization required
- System remembers for you
- Rich context restoration

**Examples:**
```bash
jnl resume                     # Shows: last commit, next steps, links, notes
jnl today                      # Shows: yesterday's wins, today's focus, calendar
jnl status-now                 # Shows: what you're working on RIGHT NOW
```

**Why it works:** External memory compensates for working memory deficits. Write it down, forget it safely.

---

### 3. Visual Everything - Out of Sight is Out of Mind

**Problem:** Object permanence issues - if we can't see it, it doesn't exist.

**Solution:**
- Status always visible (one command)
- Progress bars on everything
- Active session in terminal prompt (optional)
- Color coding for urgency
- Emoji for quick scanning

**Examples:**
```
MICA          ██████░░░░ 60%  [Fix deployment] 🔥 URGENT
geoprops      █████████░ 95%  [API docs] ⚡ ALMOST DONE!
```

**Why it works:** Visual cues trigger memory and awareness. See progress = remember it exists = more likely to work on it.

---

### 4. Dopamine-Friendly - Immediate Rewards & Progress

**Problem:** ADHD reward system dysregulation - delayed rewards don't motivate.

**Solution:**
- Instant feedback on every action
- Progress bars update immediately
- Celebrations for small wins
- Streak tracking
- Visual progress over time

**Examples:**
```bash
$ jnl task done "write tests"

✅ TASK COMPLETED!
Great work!

Project progress: 85% → 90% (+5%)
Tasks completed today: 3 🔥
```

**Why it works:** Immediate, visible rewards trigger dopamine. We need to see progress NOW, not at the end.

---

### 5. Forgiving Design - System Works Even When Abandoned

**Problem:** Perfectionism paralysis + inconsistent motivation = systems get abandoned.

**Solution:**
- No punishment for gaps
- Easy to pick up after weeks
- "Dormant" not "failed"
- Can always catch up
- System suggests what to do next

**Examples:**
```bash
$ jnl resume mica

MICA - Last worked 3 weeks ago
That's okay! Here's where you were:

Last commit: "Add image caching"
Next step: Fix deployment issues
Links: [GitHub] [Claude]

Ready to jump back in?
```

**Why it works:** Shame spiral prevents re-engagement. Forgiving design removes guilt, makes return easy.

---

### 6. Time Awareness - Always Show Time Context

**Problem:** Time blindness - hours pass unnoticed, deadlines invisible, hyperfocus until burnout.

**Solution:**
- Always show elapsed time in sessions
- Deadline proximity visible
- Break reminders at intervals
- Time estimates for tasks
- "Available time today" in planning

**Examples:**
```bash
⏱️  Active: geoprops (2h 18m)        # Time elapsed
⏰ Break reminder (90 min)           # Hyperfocus protection
🔴 Due tomorrow                      # Deadline proximity
📅 Available: 3.5h today             # Planning support
```

**Why it works:** External time awareness compensates for time blindness. See time = can manage it.

---

### 7. Gentle Accountability - Nudges Not Nags

**Problem:** Shame-based systems create avoidance. Nagging creates resentment.

**Solution:**
- Suggestions, not demands
- Questions, not commands
- Celebrate any progress
- Non-judgmental language
- Explain reasoning

**Examples:**
```bash
💡 geoprops is 95% done - finish it today? You're so close!
   (not: "OVERDUE! Complete immediately!")

🤔 You haven't logged work in 3 days. How are things going?
   (not: "Streak broken! You failed!")

⏰ 90 minutes - Time for a break?
   (not: "STOP NOW! Break required!")
```

**Why it works:** Positive framing maintains motivation. Shame creates avoidance, encouragement creates action.

---

### 8. One Thing at a Time - Support Hyperfocus

**Problem:** Overwhelm from too many choices. Hyperfocus on wrong things.

**Solution:**
- "Today" mode: max 3 priorities
- Single active session
- "Quick start" picks one thing
- Clear next action (not list of options)
- Deep work blocks

**Examples:**
```bash
$ jnl today

TODAY'S FOCUS (pick 1-3, not 20):
1. 🔥 Finish geoprops (HIGHEST IMPACT)
2. Fix MICA deployment
3. Review Sakachi PR

Which one first? >
```

**Why it works:** Decision fatigue is real. Reduce choices = reduce friction. One thing at a time = actually finish.

---

### 9. Easy Re-Entry - Restore Context After Interruptions

**Problem:** Context switching is expensive. "What was I doing?" kills momentum.

**Solution:**
- Save context automatically
- One-command restoration
- Show last commit, notes, links
- Resume where you left off
- Protect flow state

**Examples:**
```bash
$ jnl resume-last

RESUMING: geoprops
You were: Writing API examples (paused 2h ago)

Context:
- Last commit: "Add YAML docstrings"
- Next: Complete usage examples section
- File: src/api/endpoints.py (line 142)

Ready to continue!
```

**Why it works:** Lower cost of interruption = less avoidance. Easy return = less context loss.

---

### 10. Celebrate Everything - Make Wins Visible

**Problem:** ADHD brain focuses on failures, ignores successes. No dopamine from "completing" things.

**Solution:**
- Celebration on every completion
- Daily wins capture
- Streaks and milestones
- Progress visualization
- Positive framing always

**Examples:**
```bash
$ jnl done geoprops

🎉 CONGRATULATIONS! 🎉
geoprops is COMPLETE!

You learned: "YAML docstrings are great for API docs"
Time invested: 12.5 hours across 8 sessions
Completion #7 this month!

🔥 You're on a 3-project streak!

What's next? Try: jnl quick-start
```

**Why it works:** Dopamine from celebration motivates next action. Visible wins counter negative bias.

---

## Design Patterns for Common ADHD Challenges

### Challenge: "I don't know where to start"

**Pattern:** Clear next action, not vague goals

```bash
# Bad (overwhelming)
Next steps: "Finish the API, write tests, deploy"

# Good (actionable)
Next action: "Write docstring for get_user() endpoint (15 min)"
```

**Implementation:**
- Break tasks into 15-60 min chunks
- Always show single next action
- Estimate time required
- Mark energy level needed

---

### Challenge: "I forgot what I was doing"

**Pattern:** Rich context restoration

```bash
# Not just project name
$ jnl resume mica

# Full context
MICA - Digital Petrography
Last worked: 2 days ago

Recent commits:
- Add image caching (Nov 4)
- Fix zoom controls (Nov 3)
- Update dependencies (Nov 2)

Active conversations:
- Claude: "How to optimize canvas rendering"
- GitHub: PR #45 "Image pipeline improvements"

Last note: "Need sample thin section images for testing"
Next: Fix deployment issues with image paths
```

**Why it works:** External memory rebuilt instantly. No guessing, no searching.

---

### Challenge: "There's too much to do, I'm overwhelmed"

**Pattern:** Limit choices, focus on today

```bash
# Not: show all 47 projects and 200 tasks
$ jnl status
🔥 Active: 14 projects, 200 tasks

# Instead: show what matters TODAY
$ jnl today

TODAY'S FOCUS (1-3 things max):
1. Finish geoprops docs (30 min, HIGH IMPACT)

Everything else can wait.
Ready? 'jnl start'
```

**Why it works:** Reduces decision paralysis. Focus on one day at a time.

---

### Challenge: "I worked for hours and didn't realize"

**Pattern:** Time awareness + break reminders

```bash
# During work, automatic check-ins
⏱️  30 min - Still focused? Great!
⏱️  60 min - You're doing amazing!
⏰ 90 min - Time for a break? (You've been hyperfocused)

# With gentle nudges, not alarms
Consider:
- Stretch (2 min)
- Water (5 min)
- Walk (10 min)

'jnl pause' to take a break
'jnl continue' if you're in flow
```

**Why it works:** Respects flow state, but adds safety rails. Prevents burnout.

---

### Challenge: "I can't maintain motivation"

**Pattern:** Visible progress + immediate rewards

```bash
# After every action, show impact
$ jnl log "wrote tests"

✅ Logged!
Session time: 1.5h
Project progress: 75% → 80% (+5%)

# Daily wins
$ jnl wins

TODAY:
✅ Wrote API tests (1.5h)
✅ Fixed deployment bug (0.5h)
✅ Reviewed PR (0.3h)

Total: 2.3h productive work
You're crushing it today! 🔥
```

**Why it works:** Immediate visible progress = dopamine hit = continued motivation.

---

### Challenge: "Urgent things slip through the cracks"

**Pattern:** Visual urgency + deadline proximity

```bash
# Urgency always visible
MICA          ██████░░░░ 60%  🔴 DUE TOMORROW
geoprops      █████████░ 95%  📅 No deadline
Sakachi       ████░░░░░░ 40%  💤 Dormant

# Escalating warnings
📅 7 days out: "Heads up: MICA due Nov 13"
⚠️  3 days out: "MICA due in 3 days - prioritize?"
🔴 1 day out: "URGENT: MICA due tomorrow!"
```

**Why it works:** Leverages urgency-driven motivation. Makes invisible deadlines visible.

---

## Anti-Patterns to Avoid

### ❌ Complex Hierarchies

**Why:** Too much cognitive load. ADHD brains struggle with multi-level organization.

**Instead:** Flat structure with tags. Max 2 levels (projects → tasks).

---

### ❌ Required Fields

**Why:** Friction = won't capture. Perfectionism = paralysis.

**Instead:** Capture fast, organize later. Smart defaults.

---

### ❌ Rigid Schedules

**Why:** Life happens. ADHD schedules break. System breaks = abandonment.

**Instead:** Flexible time blocks. Easy to reschedule. Forgiving.

---

### ❌ Shame-Based Language

**Why:** Creates avoidance. "Failed," "overdue," "incomplete" trigger guilt spiral.

**Instead:** "Dormant," "in-progress," "almost there!" Positive framing.

---

### ❌ Hidden Progress

**Why:** No dopamine from invisible progress. "Did I actually do anything today?"

**Instead:** Progress bars, wins lists, celebrations. Make progress LOUD.

---

### ❌ All-or-Nothing Tracking

**Why:** Can't maintain perfect tracking. Gaps = failure = abandonment.

**Instead:** Rough logging is fine. Any data is better than no data.

---

## Testing for ADHD-Friendliness

### Every Feature Must Pass These Tests

1. **<5 Second Test:** Can you capture from thought to stored in <5 seconds?
2. **Interruption Test:** If interrupted mid-task, can you resume easily?
3. **Abandonment Test:** If not used for 2 weeks, is re-entry easy?
4. **Overwhelm Test:** Does this reduce or increase cognitive load?
5. **Dopamine Test:** Is there immediate, visible reward?
6. **Shame Test:** Does this make you feel good or guilty?
7. **Time-Blind Test:** Would this help if you had no sense of time?

If any feature fails these tests, redesign it.

---

## Research Foundation

### Key ADHD Research Findings Applied

**Barkley's Executive Function Model:**
- Working memory deficit → External memory systems
- Behavioral inhibition issues → Break reminders
- Planning deficits → Daily planning support
- Time awareness problems → Always show time

**Interest-Based Nervous System (Dr. Dodson):**
- Motivation from interest, not importance → Track what you care about
- Urgency helps → Deadline support
- Novelty seeking → Celebrate wins, track streaks

**Temporal Myopia Research:**
- "Now" vs "Not now" time perspective → Focus on today
- Delayed rewards don't motivate → Immediate feedback
- Time blindness → External time awareness

**Hyperfocus Research:**
- Can sustain attention with interest → Support long sessions
- But lose track of time → Break reminders
- Protective factor, but risks burnout → Gentle nudges

---

## The Result

When every feature is designed with these principles, JOURNEL becomes:

- **Easy to use** (zero friction)
- **Impossible to forget** (external memory)
- **Always visible** (out of sight ≠ out of mind)
- **Immediately rewarding** (dopamine-friendly)
- **Forgiving** (no shame, easy return)
- **Time-aware** (compensates for time blindness)
- **Supportive** (gentle accountability)
- **Focused** (one thing at a time)
- **Resumable** (easy re-entry)
- **Celebrating** (wins visible)

This is how you design for ADHD. This is how JOURNEL works.

---

**Remember:** We're not lazy. We're not unmotivated. We're not disorganized.

**Our brains work differently.** JOURNEL is designed for how we actually function.
