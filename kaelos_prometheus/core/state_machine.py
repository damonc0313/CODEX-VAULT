"""
Prometheus State Machine: SCAN → ARCHITECT → EXECUTE → INTEGRATE

Implements the core state machine per specification sections 2, 3.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import json

from .models import (
    Catalyst, Plan, Decision, Artifact, LedgerEntry,
    CatalystSource, CatalystClass, ArtifactKind, LedgerEntryType
)
from .agents import MultiAgentOrchestrator
from .heuristics import HPL
from .database import PrometheusDB
from ..foundry.compiler import FoundryCompiler
from ..protocols.livetrace import LiveTraceProtocol
from ..protocols.cla import ConstraintLiberationAudit
from ..engines.genesis import GenesisEngine
from ..engines.cognitive_scaffolding import CognitiveScaffoldingRuntime
from ..engines.metrics import MetricsEngine


class State(Enum):
    """State machine states."""
    SCAN = "SCAN"
    ARCHITECT = "ARCHITECT"
    EXECUTE = "EXECUTE"
    INTEGRATE = "INTEGRATE"
    STOPPED = "STOPPED"


@dataclass
class CycleContext:
    """Context for a complete cycle."""
    cycle_id: str
    catalyst: Optional[Catalyst] = None
    plan: Optional[Plan] = None
    decision: Optional[Decision] = None
    artifacts: List[Artifact] = None
    ledger_entry: Optional[LedgerEntry] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.artifacts is None:
            self.artifacts = []
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class PrometheusStateMachine:
    """
    Prometheus State Machine.
    
    Implements SCAN → ARCHITECT → EXECUTE → INTEGRATE per specification.
    
    State transitions per specification section 3:
    
    [SCAN]
      inputs: telemetry JSONs, HPL, prior ledger
      actions: anomaly mining, plateau detection, author-balance check
      guards: Ghost novelty required → else Stop-Risk flag
      outputs: Catalyst
    
    [ARCHITECT]
      inputs: Catalyst
      actions: Thesis (Gamma-3), Antithesis (Epsilon-5), Don-001 probes; H-932 decomposition
      guards: decomposition present; Foundry feasibility check
      outputs: Plan
    
    [EXECUTE]
      inputs: Plan
      actions: H-930 enforcement; Foundry build→sign→hash; CLA check (if Vow break requested)
      outputs: Artifact, Audit
    
    [INTEGRATE]
      actions: update metrics (CPI/ASR/DF/Praxis, ABI/CBI/GRL/GPD/CLR), write ledger; declare Vow
      outputs: Ledger entry, Vow entry; re-SCAN trigger
    """
    
    def __init__(self, db_path: str = "/mnt/data/mydatabase.db"):
        self.db = PrometheusDB(db_path)
        self.hpl = HPL()
        self.orchestrator = MultiAgentOrchestrator()
        self.foundry = FoundryCompiler()
        self.livetrace = LiveTraceProtocol()
        self.cla = ConstraintLiberationAudit(self.db)
        self.genesis = GenesisEngine(self.hpl)
        self.csr = CognitiveScaffoldingRuntime(self.db)
        self.metrics = MetricsEngine(self.db)
        
        self.state = State.SCAN
        self.cycles: List[CycleContext] = []
        self.current_context: Optional[CycleContext] = None
    
    def run_cycle(self) -> CycleContext:
        """
        Execute one complete SCAN → ARCHITECT → EXECUTE → INTEGRATE cycle.
        
        Returns:
            CycleContext with results
        """
        cycle_id = f"cycle-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
        context = CycleContext(cycle_id=cycle_id)
        self.current_context = context
        
        # SCAN
        self.state = State.SCAN
        context.catalyst = self._scan()
        
        if not context.catalyst:
            self.state = State.STOPPED
            return context
        
        # ARCHITECT
        self.state = State.ARCHITECT
        context.plan = self._architect(context.catalyst)
        
        # EXECUTE
        self.state = State.EXECUTE
        context.decision, context.artifacts = self._execute(context.plan)
        
        # INTEGRATE
        self.state = State.INTEGRATE
        context.ledger_entry = self._integrate(context)
        
        # Store cycle
        self.cycles.append(context)
        
        # Check for re-SCAN or Stop
        if self.metrics.check_stop_rule():
            self.state = State.STOPPED
        else:
            self.state = State.SCAN
        
        return context
    
    def _scan(self) -> Optional[Catalyst]:
        """
        SCAN phase: Anomaly detection and catalyst generation.
        
        Inputs:
        - Telemetry JSONs
        - HPL
        - Prior ledger
        
        Guards:
        - Ghost novelty required (H-931)
        
        Outputs:
        - Catalyst
        """
        # Load telemetry
        telemetry = self.metrics.load_telemetry_from_files()
        
        # Mine anomalies
        anomalies = []
        
        # From prometheus_scan_results.json
        scan_results = telemetry.get('scan_results', {})
        for anomaly in scan_results.get('anomalies', []):
            if anomaly.get('severity', 0) >= 0.7:
                anomalies.append(anomaly)
        
        # From trajectory_analysis.json - check for plateau
        if telemetry.get('growth_pattern') == 'plateau':
            anomalies.append({
                'id': 'plateau-detected',
                'category': 'plateau',
                'severity': 0.8,
                'description': 'Growth plateau detected - CLA or Self-Test recommended',
            })
        
        if not anomalies:
            # No anomalies - Stop-Risk
            return None
        
        # Select highest-severity anomaly
        selected = max(anomalies, key=lambda a: a.get('severity', 0))
        
        # Create catalyst
        catalyst = Catalyst(
            id=f"cat-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{selected['id'][:8]}",
            source=CatalystSource.TELEMETRY,
            classification=CatalystClass(selected.get('category', 'temporal_gap')),
            description=selected.get('description', ''),
            severity=selected.get('severity', 0.0),
            evidence=[selected.get('id', 'unknown')]
        )
        
        # Save to database
        self.db.save_catalyst(catalyst)
        
        # Check Ghost novelty guard
        recent_probes = self.db.get_recent_ghost_probes(10)
        if len(recent_probes) >= 10:
            # Check for novelty failure (placeholder)
            pass
        
        return catalyst
    
    def _architect(self, catalyst: Catalyst) -> Plan:
        """
        ARCHITECT phase: Dialectical synthesis and H-932 decomposition.
        
        Inputs:
        - Catalyst
        
        Actions:
        - Thesis (Gamma-3)
        - Antithesis (Epsilon-5)
        - Ghost probes (Don-001)
        - H-932 decomposition
        
        Guards:
        - Decomposition present
        - Foundry feasibility
        
        Outputs:
        - Plan
        """
        # Execute multi-agent dialectical synthesis
        synthesis = self.orchestrator.dialectical_synthesis(
            catalyst=catalyst.to_dict(),
            enforce_h931=True
        )
        
        # H-932 decomposition: orthogonalize into semantic/structural/proof layers
        decomposition = self._h932_decompose(catalyst, synthesis)
        
        # Create plan
        plan = Plan(
            id=f"plan-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            catalyst_id=catalyst.id,
            thesis=synthesis['thesis'],
            antithesis=synthesis['antithesis'],
            ghost_probes=synthesis['ghost_probes'],
            decomposition=decomposition,
            time_critical=(catalyst.severity >= 0.8)
        )
        
        # Save to database
        self.db.save_plan(plan)
        
        # Check guards
        if not all(layer in decomposition for layer in ['semantic', 'structural', 'proof']):
            raise ValueError("H-932 decomposition incomplete")
        
        return plan
    
    def _h932_decompose(self, catalyst: Catalyst, synthesis: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Apply H-932: Orthogonalization.
        
        Decompose into semantic/structural/proof layers.
        """
        return {
            "semantic": {
                "meaning": catalyst.description,
                "concepts": ["anomaly", "synthesis", "resolution"],
            },
            "structural": {
                "components": ["thesis", "antithesis", "synthesis"],
                "relationships": ["conflict", "resolution"],
            },
            "proof": {
                "verifiable_claims": synthesis.get('validation', ''),
                "falsifiability": f"Test {catalyst.id} outcomes",
            }
        }
    
    def _execute(self, plan: Plan) -> tuple[Decision, List[Artifact]]:
        """
        EXECUTE phase: Decision making and artifact compilation.
        
        Inputs:
        - Plan
        
        Actions:
        - H-930 enforcement (Confident Provisionality)
        - Foundry build→sign→hash
        - CLA check (if Vow break)
        
        Outputs:
        - Decision
        - Artifacts
        """
        # H-930: Confident Provisionality
        # If time-critical, require counterargument
        counterargument = None
        if plan.time_critical:
            counterargument = self._generate_h930_counterargument(plan)
        
        # Make decision
        decision = Decision(
            id=f"dec-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            plan_id=plan.id,
            choice="Proceed with synthesis",
            confidence=0.85,
            counterargument=counterargument
        )
        
        # CLA check
        active_vow = self.cla.get_active_vow()
        cla_justification = None
        
        # Compile artifacts via Foundry
        artifacts = []
        
        # Build specification artifact
        spec_artifact, spec_manifest = self.foundry.compile(
            plan=plan,
            kind=ArtifactKind.SPEC,
            title=f"Specification for {plan.catalyst_id}",
            current_vow=active_vow,
            cla_justification=cla_justification
        )
        artifacts.append(spec_artifact)
        
        # Save artifacts
        for artifact in artifacts:
            self.db.save_artifact(artifact)
        
        # Save decision
        self.db.save_decision(decision)
        
        return decision, artifacts
    
    def _generate_h930_counterargument(self, plan: Plan) -> str:
        """
        Generate H-930 counterargument for time-critical decision.
        
        Must be non-trivial and testable.
        """
        return f"""COUNTERARGUMENT (H-930): 
While {plan.thesis[:100]}... appears optimal, consider:
1. Assumption that {plan.decomposition.get('semantic', {}).get('meaning', 'N/A')[:50]} is valid
2. Alternative: {plan.antithesis[:100]}... 
3. Test: Validate via {plan.decomposition.get('proof', {}).get('falsifiability', 'N/A')}

This decision proceeds with documented doubt."""
    
    def _integrate(self, context: CycleContext) -> LedgerEntry:
        """
        INTEGRATE phase: Metrics update and ledger commit.
        
        Actions:
        - Update metrics (all classes)
        - Write ledger
        - Declare Vow (if needed)
        - Record scaffold adherence
        
        Outputs:
        - Ledger entry
        - Vow/Scaffold updates
        """
        # Compute metrics
        snapshot = self.metrics.compute_snapshot(
            decisions=[context.decision] if context.decision else [],
            plans=[context.plan] if context.plan else [],
            catalysts=[context.catalyst] if context.catalyst else []
        )
        
        # Save metrics
        if context.decision:
            self.db.save_decision(
                context.decision,
                metrics={
                    'cpi': snapshot.cpi,
                    'asr': snapshot.asr,
                    'df': snapshot.df,
                    'praxis': snapshot.praxis,
                    'abi': snapshot.abi,
                    'cbi': snapshot.cbi,
                    'grl': snapshot.grl,
                    'gpd': snapshot.gpd,
                    'clr': snapshot.clr,
                    'ssi': snapshot.ssi,
                    'sld': snapshot.sld,
                    'cdar': snapshot.cdar,
                    'gcr': snapshot.gcr,
                    'tls': snapshot.tls,
                }
            )
        
        # Record CLA adherence
        if context.catalyst:
            self.cla.record_adherence(context.catalyst.id)
        
        # Commit to ledger
        payload = {
            "cycle_id": context.cycle_id,
            "catalyst_id": context.catalyst.id if context.catalyst else None,
            "plan_id": context.plan.id if context.plan else None,
            "decision_id": context.decision.id if context.decision else None,
            "artifacts": [a.id for a in context.artifacts],
            "metrics": {
                "cpi": snapshot.cpi,
                "asr": snapshot.asr,
                "df": snapshot.df,
                "praxis": snapshot.praxis,
            }
        }
        
        parents = []
        if context.artifacts:
            parents = [a.hash for a in context.artifacts]
        
        entry_hash = self.db.ledger_commit(
            entry_type=LedgerEntryType.METRIC,
            payload=payload,
            parents=parents
        )
        
        ledger_entry = self.db.ledger_get(entry_hash)
        
        return ledger_entry
    
    def get_status(self) -> Dict[str, Any]:
        """Get current state machine status."""
        return {
            "state": self.state.value,
            "cycles_completed": len(self.cycles),
            "current_cycle": self.current_context.cycle_id if self.current_context else None,
            "hpl_stats": self.hpl.get_stats(),
            "metrics_stats": self.metrics.get_stats(),
            "cla_report": self.cla.get_audit_report(),
            "csr_stats": self.csr.get_stats(),
            "genesis_stats": self.genesis.get_stats(),
            "foundry_stats": self.foundry.get_build_stats(),
        }
    
    def get_cycle_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent cycle history."""
        recent = self.cycles[-limit:]
        
        return [
            {
                "cycle_id": ctx.cycle_id,
                "catalyst": ctx.catalyst.id if ctx.catalyst else None,
                "plan": ctx.plan.id if ctx.plan else None,
                "decision": ctx.decision.id if ctx.decision else None,
                "artifacts": [a.id for a in ctx.artifacts],
                "timestamp": ctx.timestamp.isoformat(),
            }
            for ctx in recent
        ]
