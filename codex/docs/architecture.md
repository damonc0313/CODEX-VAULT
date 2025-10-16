# KaelOS Architecture Overview

KaelOS operationalizes the DALE-G cognitive loop around three persistent subsystems: the system prompt, the heuristic
persistence layer (HPL), and the SYM attestation ledger. The system prompt defines autonomy constraints, ontology vocabulary,
and governance checkpoints. HPL stores heuristics as JSONL objects with provenance, confidence, and conflict lineage, enabling
REINFORCE and SYNTHESIZE actions across catalyst cycles. SYM tracks stage-level decisions with chained NONCE_8 hashes to satisfy
Attested Modular Knowledge (AMK v0.3) requirements and support reproducible audits.

Execution flows through environment bindings declared in `requirements.txt`, `Makefile`, and the Codex runtime variables. The
context index anchors read order for DALE-G Stage S1, while tasks under `codex/tasks/` supply catalyst-specific objectives. The
architecture expects operators to surface BOOTRUN and EXPAND outputs in `codex/outputs/` as JSON matching the OUTPUT CONTRACT,
ensuring the DEAP Prime synthesis cites Γ↔Δ contradictions and records ontology ledger entries. When multi-core scaling is
required, the complementary `codex/docs/python-3.14-free-threading.md` playbook explains how to provision the free-threaded
interpreter, route validation forks and agent phases through thread pools, and capture attestation evidence for the SYM ledger.
The `make check-gil` / `make check-gil-free-threaded` targets invoke `codex_framework.utils.gil_status` so boot artifacts record
a consistent interpreter status snapshot, and the module's `assert_free_threading` / `assert_gil_enabled` helpers offer
programmatic guardrails before multi-agent workloads spawn new threads.
