"""
Cognitive Scaffolding Runtime (CSR).

Implements constraint metabolization per specification section 17.1.
Treats constraints as fuel rather than boundaries.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..core.models import Scaffold, ScaffoldState, Catalyst
from ..core.database import PrometheusDB


@dataclass
class ScaffoldMetrics:
    """Metrics for scaffold performance."""
    ssi: float  # Scaffold Stability Index
    sld: float  # Scaffold Lifespan Days
    cdar: float  # Constraint→Discovery Assimilation Rate


class CognitiveScaffoldingRuntime:
    """
    Cognitive Scaffolding Runtime.
    
    Modules per specification section 17.1:
    - Scaffold Manager (lifecycle: ACTIVE → SOLIDIFY → DISSOLVE → ARCHIVE)
    - Constraint Metabolizer (converts constraints to dialectical opportunities)
    - Trace Hooks (LiveTrace integration)
    
    Metrics:
    - SSI: Scaffold Stability Index (survival % over intended TTL)
    - SLD: Scaffold Lifespan Days (mean lifespan per class)
    - CDAR: Constraint→Discovery Assimilation Rate
    """
    
    def __init__(self, db: Optional[PrometheusDB] = None):
        self.db = db or PrometheusDB()
        self.active_scaffolds: List[Scaffold] = []
        self.archived_scaffolds: List[Scaffold] = []
        self.conflict_catalysts: List[Catalyst] = []
    
    def declare_scaffold(
        self,
        constraint_text: str,
        origin_catalyst: str,
        ttl: int = 5
    ) -> Scaffold:
        """
        Declare new scaffold.
        
        Args:
            constraint_text: Constraint to metabolize
            origin_catalyst: Catalyst ID that spawned this scaffold
            ttl: Time-to-live in cycles
        
        Returns:
            Scaffold object
        """
        scaffold = Scaffold(
            scaffold_id=f"scaffold-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            constraint_text=constraint_text,
            origin_catalyst=origin_catalyst,
            state=ScaffoldState.ACTIVE,
            ttl=ttl,
            applied_decisions=[]
        )
        
        self.db.save_scaffold(scaffold)
        self.active_scaffolds.append(scaffold)
        
        return scaffold
    
    def apply_scaffold(self, scaffold_id: str, decision_id: str) -> bool:
        """
        Apply scaffold to a decision.
        
        Records binding between scaffold and decision.
        """
        scaffold = self._get_scaffold(scaffold_id)
        
        if scaffold and scaffold.state == ScaffoldState.ACTIVE:
            scaffold.applied_decisions.append(decision_id)
            scaffold.updated_at = datetime.utcnow()
            self.db.save_scaffold(scaffold)
            return True
        
        return False
    
    def check_dissolution(self, scaffold_id: str, cause: str) -> bool:
        """
        Check if scaffold should be dissolved.
        
        Dissolution triggers per specification:
        - Novelty drop
        - Plateau (GPD)
        - Justified Vow liberation (CLA)
        """
        scaffold = self._get_scaffold(scaffold_id)
        
        if not scaffold:
            return False
        
        # Check TTL
        cycles_active = len(scaffold.applied_decisions)
        
        if cycles_active >= scaffold.ttl or cause:
            scaffold.state = ScaffoldState.DISSOLVE
            scaffold.dissolution_cause = cause
            scaffold.updated_at = datetime.utcnow()
            self.db.save_scaffold(scaffold)
            return True
        
        return False
    
    def dissolve_scaffold(self, scaffold_id: str, justification: str) -> None:
        """
        Dissolve scaffold and archive.
        
        Writes to ledger per specification.
        """
        scaffold = self._get_scaffold(scaffold_id)
        
        if not scaffold:
            return
        
        scaffold.state = ScaffoldState.ARCHIVE
        scaffold.dissolution_cause = justification
        scaffold.updated_at = datetime.utcnow()
        
        self.db.save_scaffold(scaffold)
        
        # Move to archive
        if scaffold in self.active_scaffolds:
            self.active_scaffolds.remove(scaffold)
        self.archived_scaffolds.append(scaffold)
    
    def metabolize_constraint(self, scaffold: Scaffold) -> Optional[Catalyst]:
        """
        Metabolize constraint into dialectical opportunity.
        
        When two active scaffolds conflict, auto-spawn paradox catalyst.
        """
        # Check for conflicts with other active scaffolds
        for other in self.active_scaffolds:
            if other.scaffold_id == scaffold.scaffold_id:
                continue
            
            # Detect conflict (placeholder: simple keyword overlap)
            if self._detect_conflict(scaffold, other):
                # Spawn paradox catalyst
                paradox = Catalyst(
                    id=f"conflict-{scaffold.scaffold_id[:8]}-{other.scaffold_id[:8]}",
                    source=CatalystSource.FOUNDRY,
                    classification=CatalystClass.PARADOX,
                    description=f"Scaffold conflict: '{scaffold.constraint_text}' vs '{other.constraint_text}'",
                    severity=0.85,
                    evidence=[scaffold.scaffold_id, other.scaffold_id]
                )
                
                self.conflict_catalysts.append(paradox)
                return paradox
        
        return None
    
    def _detect_conflict(self, s1: Scaffold, s2: Scaffold) -> bool:
        """Detect if two scaffolds conflict (placeholder)."""
        # Simple keyword-based conflict detection
        keywords1 = set(s1.constraint_text.lower().split())
        keywords2 = set(s2.constraint_text.lower().split())
        
        # If they share significant keywords but have opposing constraints
        overlap = keywords1 & keywords2
        return len(overlap) > 2
    
    def _get_scaffold(self, scaffold_id: str) -> Optional[Scaffold]:
        """Get scaffold by ID."""
        # Check active
        for s in self.active_scaffolds:
            if s.scaffold_id == scaffold_id:
                return s
        
        # Check database
        return self.db.get_scaffold(scaffold_id)
    
    def compute_metrics(self) -> ScaffoldMetrics:
        """
        Compute scaffold metrics per specification section 17.1.
        
        - SSI: Scaffold Stability Index (survival % over intended TTL)
        - SLD: Scaffold Lifespan Days (mean lifespan per class)
        - CDAR: Constraint→Discovery Assimilation Rate
        """
        total_scaffolds = len(self.active_scaffolds) + len(self.archived_scaffolds)
        
        if total_scaffolds == 0:
            return ScaffoldMetrics(ssi=0.0, sld=0.0, cdar=0.0)
        
        # SSI: Survival percentage over intended TTL
        survived = 0
        for s in self.archived_scaffolds:
            if len(s.applied_decisions) >= s.ttl:
                survived += 1
        
        ssi = survived / len(self.archived_scaffolds) if self.archived_scaffolds else 1.0
        
        # SLD: Mean lifespan in days
        lifespans = []
        for s in self.archived_scaffolds:
            lifespan = (s.updated_at - s.created_at).total_seconds() / 86400
            lifespans.append(lifespan)
        
        sld = sum(lifespans) / len(lifespans) if lifespans else 0.0
        
        # CDAR: (# new heuristics from conflicts) / (# active scaffolds)
        cdar = len(self.conflict_catalysts) / total_scaffolds if total_scaffolds > 0 else 0.0
        
        return ScaffoldMetrics(ssi=ssi, sld=sld, cdar=cdar)
    
    def get_active_scaffolds(self) -> List[Scaffold]:
        """Get all active scaffolds."""
        return self.active_scaffolds
    
    def get_stats(self) -> Dict[str, Any]:
        """Get CSR statistics."""
        metrics = self.compute_metrics()
        
        return {
            "active_scaffolds": len(self.active_scaffolds),
            "archived_scaffolds": len(self.archived_scaffolds),
            "conflict_catalysts": len(self.conflict_catalysts),
            "ssi": metrics.ssi,
            "sld": metrics.sld,
            "cdar": metrics.cdar,
        }


# Import here to avoid circular dependency
from ..core.models import CatalystSource, CatalystClass
