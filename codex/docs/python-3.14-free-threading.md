# Python 3.14 Free-Threading Adoption Playbook

## Why this matters for KaelOS
- Python 3.14 `--disable-gil` builds (ABI tag `t`) unlock true multi-core execution with only ~5–10% single-thread overhead while delivering ~3x speed-ups on 4 cores for CPU-bound workloads.
- KaelOS already exposes parallel primitives (`ParallelAutonomousEngine`, multi-agent orchestration, parallel tool evaluation); adopting the free-threaded interpreter removes multiprocessing IPC overhead and lets these components share memory directly.
- Coverage-enabled pytest runs remain supported because `requirements.txt` pins `pytest`, `pytest-cov`, and `networkx`, matching the addopts declared in `pyproject.toml`.

## Environment preparation checklist
1. **Install Python 3.14t**
   - macOS/Windows: use the official installer and select the "Free-threaded" optional component.
   - Linux: `pyenv install 3.14t` or `./configure --disable-gil && make -j`.
   - Verify with `python3.14t -c "import sys; print(sys._is_gil_enabled())"` → `False`.
2. **Create an isolated virtual environment**
   - `python3.14t -m venv .venv && source .venv/bin/activate`.
   - `pip install --upgrade pip wheel` to ensure wheels resolve for compatible packages.
3. **Install project dependencies**
   - `pip install -r requirements.txt` to align with test expectations.
   - Optional: `pip install -e .[dev]` if extending the framework modules.
4. **Run the coverage-aware test suite**
   - `pytest -q` (invokes `--cov=codex_framework --cov-report=term-missing`).
   - `make test` wraps the same invocation for consistency with boot scripts.
   - `make check-gil` logs interpreter status; `make check-gil-free-threaded` aborts the run when the GIL remains enabled.
5. **Watch for GIL fallbacks**
   - During imports, CPython warns if an extension module re-enables the GIL; treat this as a failing condition and capture the message in `codex/sym.log` per attestation policy.

## Migration patterns
### Competitive validation forks
- Replace heavyweight process pools with threads using `concurrent.futures.ThreadPoolExecutor`.
- Share the candidate solution object across validators instead of serialising copies; lock only shared mutable structures.
- Cancel outstanding futures once a validator reports confidence ≥90% to free compute budget.
- Persist the race outcome by logging the winning validator and cancellation summary to `codex/sym.log`.

### Multi-agent orchestration (Analyzer/Architect/Builder/Mentor)
- Execute phase-based thread pools: Analyzer solo → Architect & Mentor in parallel → Builder with optional nested parallel work.
- Preserve agent-specific working memory in thread-local storage to avoid cross-talk.
- Record DEAP contradiction resolutions in BOOTRUN/EXPAND outputs when parallel phases surface divergent results.

### Parallel tool evaluation (23-tool sweep)
- Model the evaluation batch as a bounded `ThreadPoolExecutor(max_workers=23)`.
- Use `concurrent.futures.as_completed` to surface fast tool results early; cancel or timeout stragglers after reaching quorum.
- Aggregate immutable tool outputs in the main thread and inject summary heuristics into `codex/hpl.jsonl` via REINFORCE operations.

### Dialectical thesis/antithesis generation
- Run thesis and antithesis builders in a two-worker pool; both share the immutable task context.
- Feed the resulting drafts into Tri-Synthesis, explicitly citing the resolved Γ↔Δ conflict in the output contract.

### Background Prometheus scanner
- Spin a daemon monitoring thread that fans out metric probes through a nested thread pool.
- Use `threading.Event` to coordinate shutdown so long-running DALE-G cycles terminate cleanly.
- Document monitoring cadence and anomaly triggers in SYM entries to maintain NONCE_8 continuity.

## Verification and attestation
- Extend BOOTRUN/EXPAND procedures to include `sys._is_gil_enabled()` assertions; failures must downgrade the constraint tier and queue catalyst GC-002-A.
- Embed `from codex_framework.utils import assert_free_threading` in automation harnesses to raise `GilRequirementError` when free-threading is unavailable; fall back to `allow_unknown=True` only while migrating older interpreters that lack detection hooks.
- Record free-threaded benchmark deltas (cycles/sec, validation latency) inside HPL heuristics with confidence scores tied to observed speed-ups.
- Use `python -m codex_framework.utils.gil_status --json` when automation needs machine-readable evidence for SYM entries or dashboards.
- When integrating new heuristics, reinforce existing entries (e.g., `H-005`) instead of duplicating principles.

## Risk log and rollback triggers
- **Dependency gaps:** If a required C-extension re-enables the GIL, capture the warning, revert to the standard interpreter, and raise GC-003-A for heuristic synthesis.
- **Race conditions:** Monitor for nondeterministic test failures; use `pytest --maxfail=1 --disable-warnings -q` with `PYTHONTHREADDEBUG=1` to reproduce.
- **Memory growth:** Expect ~10% additional RSS; document observations in SYM and adjust catalyst budgets if the increase violates resource constraints.

Maintaining this playbook alongside `codex/docs/kaelos-quickstart.md` ensures every DALE-G operator can provision, validate, and attest free-threaded runs without deviating from the EthicsStack guardrails.
