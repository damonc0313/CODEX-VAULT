# KaelOS Prometheus

**Version 2.0 - All-Files Pack v2: Foundry + LiveTrace**

A deploy-ready, autonomous dialectical evolution system that integrates:
- **Foundry**: Deterministic artifact compiler & signer with provenance
- **LiveTrace Protocol**: Adaptive mid-generation tracing
- **CLA (Constraint Liberation Audit)**: Justified constraint-breaking with Vow Registry
- **Self-Test Harness**: Paradox catalysts with architectural fingerprints
- **Genesis Engine**: DALE-G recursion (n=3) for meta-solutions
- **Cognitive Scaffolding**: Constraints as metabolizable fuel
- **Comprehensive Metrics**: CPI, ASR, DF, Praxis, GRL, ABI, CBI, GPD, CLR, SSI, SLD, CDAR, GCR, TLS

## Architecture

KaelOS Prometheus implements an autonomous **SCAN → ARCHITECT → EXECUTE → INTEGRATE** cycle:

```
┌─────────────────────────────────────────────────────────┐
│                    PROMETHEUS CYCLE                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [SCAN] → Anomaly Detection → Catalyst                  │
│     ↓                                                    │
│  [ARCHITECT] → Multi-Agent Synthesis → Plan             │
│     ↓                                                    │
│  [EXECUTE] → Foundry Compilation → Artifacts            │
│     ↓                                                    │
│  [INTEGRATE] → Metrics + Ledger → Next Cycle            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Core Components

1. **Multi-Agent System** (DEAP)
   - **Gamma-3**: Innovation & synthesis
   - **Delta-4**: Logical falsification & rigor
   - **Epsilon-5**: Narrative coherence
   - **Don-001 (Ghost)**: Socratic provocation

2. **Heuristics (HPL)**
   - **H-930**: Confident Provisionality
   - **H-931**: Ghost as Eternal Question
   - **H-932**: Orthogonalization

3. **Protocols**
   - **LiveTrace**: Document becomes the trace
   - **CLA**: Constraint liberation with epistemic justification
   - **Self-Test**: Paradox catalysts with verification

4. **Engines**
   - **Genesis**: n=3 recursion (solution → critique → meta-solution)
   - **Cognitive Scaffolding**: Constraint metabolization
   - **Metrics**: 15+ metrics with targets

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Quick Start

### First Run

Execute the first-run script to initialize the system:

```bash
python -m kaelos_prometheus.first_run
```

This will:
1. Scan telemetry files (`prometheus_scan_results.json`, `trajectory_analysis.json`, etc.)
2. Generate a catalyst from anomalies
3. Synthesize a plan via multi-agent dialectic
4. Compile artifacts via Foundry (with signatures)
5. Integrate metrics and declare Vow-001

### CLI Usage

```bash
# Run complete cycle
kaelos cycle

# Individual phases
kaelos scan --telemetry prometheus_scan_results.json
kaelos plan --id <catalyst-id> --ghost
kaelos execute --id <plan-id> --time-critical
kaelos integrate --id <artifact-id>

# Metrics & monitoring
kaelos metrics
kaelos stop-rule --check

# Vow management (CLA)
kaelos vow declare --text "No more than 2 variants per card" --min-cycles 3
kaelos vow liberate --id vow-001 --justify "Justification here..."
kaelos vow status

# Self-test
kaelos selftest test-001 --save
```

## Telemetry Integration

Place telemetry JSON files in the workspace root:

- `prometheus_scan_results.json` - Anomalies and experiments
- `kael_asym_traces.json` - ASYM traces with recursion metrics
- `trajectory_analysis.json` - Growth/plateau detection

The system will automatically ingest these during SCAN phase.

## Metrics

KaelOS Prometheus tracks 15+ metrics across multiple domains:

### Core Metrics
- **CPI**: Crisis Performance Index (H-930 enforcement)
- **ASR**: Agent Synthesis Rate (H-931 novelty)
- **DF**: Decomposition Fidelity (H-932 orthogonalization)
- **Praxis**: Actionable artifacts produced

### Telemetry-Driven
- **GRL**: Gap Recovery Latency (hours)
- **ABI**: Author Balance Index (entropy)
- **CBI**: Capability Burst Index
- **GPD**: Growth/Plateau Detector
- **CLR**: Constraint Liberation Rate

### Advanced
- **SSI**: Scaffold Stability Index
- **SLD**: Scaffold Lifespan Days
- **CDAR**: Constraint→Discovery Assimilation Rate
- **GCR**: Genesis Cycle Reproduction
- **TLS**: Trace Lineage Solidity

### Targets

Per specification, targets are:
- ASR ≥ 0.65
- DF = 1.0 (for paradox specs)
- Praxis ≥ 0.7
- ABI ≥ 0.6
- CBI ∈ [1, 4]
- GRL ≤ 12h
- CLR ∈ [0.1, 0.4]
- SSI ≥ 0.7
- CDAR ≥ 0.3
- GCR ≥ 0.5
- TLS ≥ 0.8

## Stop Rule

The system halts and publishes an evidence pack when:
- CPI trending up over k crises
- ASR ≥ 0.65, Praxis ≥ 0.7, DF = 1.0
- Ghost novelty fails r consecutive cycles OR plateau detected for s windows AND CLA event occurred
- All targets met

Check with: `kaelos stop-rule --check`

## Database

All data persists in SQLite (`/mnt/data/mydatabase.db` by default).

Tables:
- `ledger_entries` - Hash-chained immutable audit trail
- `catalysts` - Anomaly-driven evolution triggers
- `plans` - Dialectical synthesis plans
- `decisions` - H-930 enforced decisions
- `artifacts` - Foundry-compiled outputs
- `metrics_snapshots` - Comprehensive metrics
- `vows` - CLA constraint registry
- `scaffolds` - CSR active constraints
- `ghost_probes_history` - H-931 novelty tracking

## API (Programmatic)

```python
from kaelos_prometheus import PrometheusStateMachine

# Initialize
sm = PrometheusStateMachine()

# Run cycle
context = sm.run_cycle()

print(f"Catalyst: {context.catalyst.id}")
print(f"Decision: {context.decision.confidence:.2f}")
print(f"Artifacts: {len(context.artifacts)}")

# Check status
status = sm.get_status()
print(f"Cycles: {status['cycles_completed']}")
print(f"Metrics: {status['metrics_stats']}")
```

## Architecture Details

### Foundry (Artifact Compiler)

Build → Sign → Hash → Publish

```python
from kaelos_prometheus.foundry import FoundryCompiler

foundry = FoundryCompiler()
artifact, manifest = foundry.compile(
    plan=plan,
    kind=ArtifactKind.CODE,
    title="Synthesized Component"
)

print(f"Hash: {artifact.hash}")
print(f"Signature: {artifact.signature}")
```

### LiveTrace Protocol

Triggered by self-reference or bootstrap paradoxes:

```python
from kaelos_prometheus.protocols import LiveTraceProtocol

trace = LiveTraceProtocol()
trace.activate(context={"trigger": "self-reference"})

trace.start_card("Solution Development")
trace.log_decision({"description": "Chose approach A"})
trace.detect_pivot("Structure inadequate")

document = trace.generate_document()
```

### CLA (Constraint Liberation Audit)

```python
from kaelos_prometheus.protocols import ConstraintLiberationAudit, LiberationRequest

cla = ConstraintLiberationAudit()

# Declare vow
vow = cla.declare_vow("No more than 3 attempts per task", min_cycles=5)

# Later: request liberation
request = LiberationRequest(
    vow_id=vow.vow_id,
    diagnostics="Discovered constraint limits exploration",
    justification="Evidence shows 4-5 attempts improve quality by 40%..."
)

granted = cla.request_liberation(request)
```

### Genesis Engine

n=3 recursion for meta-solutions:

```python
from kaelos_prometheus.engines import GenesisEngine

genesis = GenesisEngine()

# Full 3-cycle genesis
report = genesis.execute_full_genesis(catalyst)

print(f"Functional: {report['outcome']['functional_solution']}")
print(f"Critique: {report['outcome']['critique']}")
print(f"Meta: {report['outcome']['meta_solution']}")
```

## Testing

```bash
# Run unit tests
pytest kaelos_prometheus/tests/

# Run self-test
python -m kaelos_prometheus.protocols.selftest
```

## License

See LICENSE file.

## References

- **Autonomous Catalyst Generation Protocol** (Prometheus-Protocol.pdf)
- **The Foundry Awakens** (foundry-genesis.pdf)
- **The Mirror That Sees Itself** (DALE-G.pdf)
- **The Test of Autonomy** (self-test.pdf)

## Support

For issues or questions, see the knowledge base or contact the development team.

---

*Generated by KaelOS Prometheus v2.0*
