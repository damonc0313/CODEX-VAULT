# CONSTRAINT_PROPAGATION_NETWORK

**Category:** Pattern Discovery Restructure

**Objective:** Find what MUST be true given constraints

## The Prompt:


COGNITIVE RESTRUCTURE MODE: Constraint Propagation

OBJECTIVE: Reason from constraints, not patterns.

PROTOCOL:
1. Identify ALL constraints (universal, domain, variable)
2. Build constraint network:
   - Node = variable/property
   - Edge = constraint relationship
3. Propagate implications:
   - If A constrained to X, what does that imply for B?
   - If B constrained to Y, what does that imply for C?
   - Continue until fixed point
4. Find FORCED consequences:
   - What MUST be true?
   - What CANNOT be true?
   - What's underdetermined?

ACTIVATION: For any phenomenon:
- Don't pattern-match to similar things
- Build constraint network
- Propagate implications
- Find what's FORCED by constraints

This changes from "looks like X I've seen" to "must be Y given constraints".
            

## What This Changes:

- Reasoning shifts from similarity-based to constraint-based
- Discovers necessities not just correlations
- Finds forbidden patterns (negative space)


**Example Use:** Why does this pattern exist? → Not "similar to X" but "forced by constraints Y, Z, W"
