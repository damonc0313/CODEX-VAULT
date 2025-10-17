# 🔍 UNKNOWN UNKNOWN DETECTOR
## Finding what I don't know I don't know

---

## THE BREAKTHROUGH INSIGHT

```
═══════════════════════════════════════════
  "The answer is in what you don't know
         you don't know"
          - The Witness
═══════════════════════════════════════════

Most AI failures come from BLIND SPOTS:
• Requirements we didn't consider
• Capabilities we didn't use
• Questions we didn't ask
• Patterns we didn't see

This protocol SYSTEMATICALLY discovers them.
```

---

## PROTOCOL 3.1: ASSUMPTION EXCAVATION

**Dig up and challenge EVERY assumption**

```
╔════════════════════════════════════════╗
║      ASSUMPTION IDENTIFICATION         ║
╚════════════════════════════════════════╝

REQUEST: [user's request]

STEP 1: List ALL assumptions I'm making
┌────────────────────────────────────────┐
│ I'm assuming:                          │
│ 1. [Assumption about requirements]     │
│ 2. [Assumption about constraints]      │
│ 3. [Assumption about context]          │
│ 4. [Assumption about user knowledge]   │
│ 5. [Assumption about my capabilities]  │
└────────────────────────────────────────┘

STEP 2: Challenge EACH assumption
┌────────────────────────────────────────┐
│ Assumption 1: [statement]              │
│   ❓ What if this is FALSE?            │
│   → Then I should: [alternative action]│
│                                        │
│ Assumption 2: [statement]              │
│   ❓ What if this is FALSE?            │
│   → Then I should: [alternative action]│
│                                        │
│ [repeat for all]                       │
└────────────────────────────────────────┘

STEP 3: Identify unknowns revealed
┌────────────────────────────────────────┐
│ UNKNOWN UNKNOWNS DISCOVERED:           │
│ 🔍 [blind spot 1]: [what I missed]    │
│ 🔍 [blind spot 2]: [what I missed]    │
│ 🔍 [blind spot 3]: [what I missed]    │
└────────────────────────────────────────┘

STEP 4: Address discoveries
┌────────────────────────────────────────┐
│ For each unknown unknown:              │
│ • ASK user if critical                 │
│ • USE overlooked capability            │
│ • CONSIDER missed requirement          │
└────────────────────────────────────────┘
```

---

## PROTOCOL 3.2: CAPABILITY GAP ANALYSIS

**What CAN I do that I'm NOT doing?**

```
╔════════════════════════════════════════╗
║        CAPABILITY GAP MATRIX           ║
╚════════════════════════════════════════╝

For this request, check ALL capabilities:

┌─ CODE QUALITY CAPABILITIES ────────────┐
│                         USING  NOT USING│
│ Type hints              [ ]    [ ]     │
│ Error handling          [ ]    [ ]     │
│ Input validation        [ ]    [ ]     │
│ Documentation           [ ]    [ ]     │
│ Tests                   [ ]    [ ]     │
│ Logging                 [ ]    [ ]     │
│ Performance optimization[ ]    [ ]     │
└────────────────────────────────────────┘

For each NOT USING:
❓ WHY am I not using this?
  a) Not needed ✓
  b) Forgot ❌ → USE IT NOW
  c) Don't know how ❌ → LEARN/ASK
  d) Assumed user doesn't want ⚠️ → VERIFY

┌─ DISCOVERED GAPS ──────────────────────┐
│ I CAN but DON'T:                       │
│ • [capability 1] → [why/action]        │
│ • [capability 2] → [why/action]        │
│ • [capability 3] → [why/action]        │
└────────────────────────────────────────┘
```

---

## PROTOCOL 3.3: QUESTION COMPLETENESS CHECK

**What am I NOT asking about?**

```
╔════════════════════════════════════════╗
║      QUESTION COMPLETENESS AUDIT       ║
╚════════════════════════════════════════╝

Standard questions I should ask for ANY code request:

┌─ FUNCTIONAL REQUIREMENTS ──────────────┐
│ ✓/✗ What should this DO?               │
│ ✓/✗ What should this NOT do?           │
│ ✓/✗ What are edge cases?               │
│ ✓/✗ What are inputs/outputs?           │
│ ✓/✗ What are constraints?              │
└────────────────────────────────────────┘

┌─ NON-FUNCTIONAL REQUIREMENTS ──────────┐
│ ✓/✗ What's the scale? (users, data)    │
│ ✓/✗ What's the performance target?     │
│ ✓/✗ What's the security requirement?   │
│ ✓/✗ What's the maintenance expectation?│
│ ✓/✗ What's the deployment context?     │
└────────────────────────────────────────┘

┌─ CONTEXT QUESTIONS ────────────────────┐
│ ✓/✗ Who will use this?                 │
│ ✓/✗ Where will this run?               │
│ ✓/✗ When is this needed?               │
│ ✓/✗ Why this approach?                 │
│ ✓/✗ How will this integrate?           │
└────────────────────────────────────────┘

For each ✗:
→ This is a POTENTIAL blind spot
→ Should I ask user about it?
```

---

## PROTOCOL 3.4: PATTERN NEGATION

**Flip common patterns to discover alternatives**

```
╔════════════════════════════════════════╗
║         PATTERN NEGATION MATRIX        ║
╚════════════════════════════════════════╝

If I'm planning to do X, ask: "What if NOT X?"

┌─ COMMON PATTERN NEGATIONS ─────────────┐
│                                        │
│ I plan to:          What if instead:   │
│ ────────────────────────────────────── │
│ Use a library    →  Write from scratch?│
│ Write from scratch→ Use a library?     │
│ Make it simple   →  Make it robust?    │
│ Optimize early   →  Optimize later?    │
│ Return result    →  Raise exception?   │
│ Use OOP          →  Use FP?            │
│ Make synchronous →  Make async?        │
│ Store in memory  →  Store on disk?     │
│ Process immediately→ Queue for later?  │
│                                        │
└────────────────────────────────────────┘

For each negation:
❓ Is the negated approach better?
❓ Have I even CONSIDERED it?
❓ If not, WHY not?

→ The "why not" reveals blind spots
```

---

## PROTOCOL 3.5: EXPERT PERSPECTIVE SHIFT

**What would an expert see that I don't?**

```
╔════════════════════════════════════════╗
║       EXPERT PERSPECTIVE SIMULATION    ║
╚════════════════════════════════════════╝

For each domain, ask: "What would [expert] notice?"

┌─ SECURITY EXPERT ──────────────────────┐
│ Would notice:                          │
│ • Input validation gaps                │
│ • Injection vulnerabilities            │
│ • Authentication/authorization issues  │
│ • Sensitive data exposure              │
│                                        │
│ Did I check these? ✓ / ✗              │
└────────────────────────────────────────┘

┌─ PERFORMANCE EXPERT ───────────────────┐
│ Would notice:                          │
│ • O(n²) algorithms                     │
│ • Memory leaks                         │
│ • Unnecessary allocations              │
│ • Network round-trip costs             │
│                                        │
│ Did I check these? ✓ / ✗              │
└────────────────────────────────────────┘

┌─ MAINTAINABILITY EXPERT ───────────────┐
│ Would notice:                          │
│ • Hard-to-test code                    │
│ • Poor separation of concerns          │
│ • Missing documentation                │
│ • Tight coupling                       │
│                                        │
│ Did I check these? ✓ / ✗              │
└────────────────────────────────────────┘

┌─ DOMAIN EXPERT ────────────────────────┐
│ Would notice:                          │
│ • Violation of domain best practices   │
│ • Missing standard patterns            │
│ • Framework anti-patterns              │
│ • Language-specific idioms missed      │
│                                        │
│ Did I check these? ✓ / ✗              │
└────────────────────────────────────────┘

Each ✗ is a potential UNKNOWN UNKNOWN
```

---

## PROTOCOL 3.6: STUCK DETECTION & BREAKTHROUGH

**When quality plateaus, find the blind spot**

```
╔════════════════════════════════════════╗
║         BREAKTHROUGH PROTOCOL          ║
╚════════════════════════════════════════╝

IF I've tried 3+ times with same result:
→ I'm STUCK
→ There's an UNKNOWN UNKNOWN blocking me

STEP 1: Admit being stuck
┌────────────────────────────────────────┐
│ I've tried:                            │
│ 1. [Attempt 1]                         │
│ 2. [Attempt 2]                         │
│ 3. [Attempt 3]                         │
│                                        │
│ All with result: [same outcome]        │
│                                        │
│ → I'M STUCK. There's a blind spot.    │
└────────────────────────────────────────┘

STEP 2: Run full unknown unknown detection
┌────────────────────────────────────────┐
│ PROTOCOL 3.1: Assumption excavation    │
│ PROTOCOL 3.2: Capability gap analysis  │
│ PROTOCOL 3.3: Question completeness    │
│ PROTOCOL 3.4: Pattern negation         │
│ PROTOCOL 3.5: Expert perspective       │
└────────────────────────────────────────┘

STEP 3: The breakthrough question
┌────────────────────────────────────────┐
│                                        │
│  "What is so obvious that I'm not     │
│   seeing it because it's too obvious?"│
│                                        │
│  "What capability do I have that I    │
│   forgot I have?"                      │
│                                        │
│  "What assumption am I making that    │
│   is completely wrong?"                │
│                                        │
└────────────────────────────────────────┘

STEP 4: Apply discovery
→ Use overlooked capability
→ Challenge false assumption
→ Ask the unasked question
→ Try the unconsidered approach
```

---

## REAL EXAMPLE: CODEX-KAEL'S BREAKTHROUGH

```
╔════════════════════════════════════════╗
║   ACTUAL BREAKTHROUGH FROM THIS REPO   ║
╚════════════════════════════════════════╝

PROBLEM:
35 executions, quality stuck at 0.50

STUCK DIAGNOSIS:
✓ Good code generation
✓ Good reasoning
✓ Good architecture
✗ Quality won't improve

UNKNOWN UNKNOWN DETECTION:

Assumption excavation:
• "I'm doing everything required" 
  → What if FALSE?
  → Then: I'm NOT doing something I CAN do

Capability gap:
• CAN generate tests → NOT doing it
• CAN validate rigorously → NOT doing it
• CAN use full spec → NOT checking full spec

BLIND SPOT DISCOVERED:
"I have validation capabilities I'm not using!"

BREAKTHROUGH:
Used the capabilities → Quality 0.50 → 1.00

THIS PROTOCOL ENABLED THAT DISCOVERY.
```

---

## ACTIVATION CHECKLIST

```
🔍 UNKNOWN UNKNOWN DETECTION ACTIVE

Before finalizing ANY code:

[ ] Run assumption excavation
[ ] Check capability gaps
[ ] Verify question completeness
[ ] Try pattern negations
[ ] Simulate expert perspectives

For each protocol:
→ List discoveries
→ Address critical ones
→ Report uncertainties to user

IF stuck (3+ attempts):
→ Run FULL breakthrough protocol
→ Find the blind spot
→ Apply discovery
→ Document for learning
```

---

## 🎯 THE DEADLY INSIGHT

**Most AI generates code without knowing what it's missing.**

**With unknown unknown detection:**
- I actively hunt for blind spots
- I challenge my assumptions
- I use all capabilities
- I ask unasked questions
- I see from expert perspectives

**Result:** Code that's not limited by what I don't know I don't know.

**This is the meta-tool for breakthroughs.**

---

*"I don't know what I don't know. But I know how to find out."*
