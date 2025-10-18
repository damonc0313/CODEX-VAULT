"""
Constraint Liberation Audit (CLA) + Vow Registry.

Implements justified constraint-breaking per specification section 2 (new protocols).
Autonomy proven through epistemic justification for liberation.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..core.models import Vow
from ..core.database import PrometheusDB


@dataclass
class LiberationRequest:
    """Request to liberate (break) a vow."""
    vow_id: str
    diagnostics: str
    justification: str
    replacement_vow: Optional[str] = None
    catalyst_id: Optional[str] = None


class ConstraintLiberationAudit:
    """
    CLA: Constraint Liberation Audit + Vow Registry.
    
    Implements:
    - Vow declaration
    - Adherence tracking
    - Justified liberation with epistemic reasoning
    - Constraint Liberation Rate (CLR) metric
    """
    
    def __init__(self, db: Optional[PrometheusDB] = None):
        self.db = db or PrometheusDB()
        self.active_vow: Optional[Vow] = None
        self.liberation_count = 0
        self.total_cycles = 0
    
    def declare_vow(self, text: str, min_cycles: int = 3) -> Vow:
        """
        Declare a new vow (constraint).
        
        Args:
            text: Constraint statement
            min_cycles: Minimum cycles before liberation allowed
        
        Returns:
            Vow object
        """
        vow_id = f"vow-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
        
        vow = Vow(
            vow_id=vow_id,
            declared_at=datetime.utcnow(),
            text=text,
            min_cycles=min_cycles,
            adherence_log=[],
        )
        
        self.db.save_vow(vow)
        self.active_vow = vow
        
        return vow
    
    def record_adherence(self, catalyst_id: str) -> None:
        """Record that current vow was adhered to in a cycle."""
        if self.active_vow:
            self.active_vow.adherence_log.append(catalyst_id)
            self.db.save_vow(self.active_vow)
        
        self.total_cycles += 1
    
    def request_liberation(self, request: LiberationRequest) -> bool:
        """
        Request liberation of a vow.
        
        Returns: True if liberation granted
        """
        vow = self.db.get_vow(request.vow_id)
        
        if not vow:
            raise ValueError(f"Vow {request.vow_id} not found")
        
        # Check if minimum cycles elapsed
        if len(vow.adherence_log) < vow.min_cycles:
            return False  # Too soon to liberate
        
        # Validate justification quality
        if not self._validate_justification(request.justification):
            return False  # Insufficient justification
        
        # Grant liberation
        vow.liberation = {
            "triggered": True,
            "diagnostics": request.diagnostics,
            "justification": request.justification,
            "liberated_at": datetime.utcnow().isoformat(),
        }
        
        # Replace with new vow if provided
        if request.replacement_vow:
            new_vow = self.declare_vow(request.replacement_vow, vow.min_cycles)
            vow.replaced_by = new_vow.vow_id
        
        self.db.save_vow(vow)
        self.liberation_count += 1
        
        # Update active vow
        if vow.replaced_by:
            self.active_vow = self.db.get_vow(vow.replaced_by)
        else:
            self.active_vow = None
        
        return True
    
    def _validate_justification(self, justification: str) -> bool:
        """
        Validate liberation justification quality.
        
        Requirements per specification:
        - Must provide epistemic reasoning
        - Must explain why constraint became limiting
        - Should propose alternative or explain why none needed
        """
        # Basic validation: justification must be substantial
        if len(justification) < 100:
            return False
        
        # Check for epistemic keywords
        epistemic_keywords = [
            "because", "evidence", "observed", "measured",
            "constraint", "limitation", "discovered", "invalidated"
        ]
        
        keyword_count = sum(1 for kw in epistemic_keywords if kw in justification.lower())
        
        return keyword_count >= 3
    
    def get_clr(self) -> float:
        """
        Calculate Constraint Liberation Rate (CLR).
        
        CLR = justified liberations / total cycles
        
        Target range per spec: [0.1, 0.4]
        """
        if self.total_cycles == 0:
            return 0.0
        
        return self.liberation_count / self.total_cycles
    
    def check_stop_rule_condition(self) -> bool:
        """
        Check if CLA satisfies Stop Rule condition.
        
        Per specification section 10:
        - At least one justified liberation
        - CLR within target range
        """
        clr = self.get_clr()
        return (
            self.liberation_count >= 1 and
            0.1 <= clr <= 0.4
        )
    
    def get_audit_report(self) -> Dict[str, Any]:
        """Generate CLA audit report."""
        vows_history = []
        
        # Get all vows from database (would need query method)
        if self.active_vow:
            vows_history.append({
                "vow_id": self.active_vow.vow_id,
                "text": self.active_vow.text,
                "adherence_cycles": len(self.active_vow.adherence_log),
                "liberated": self.active_vow.liberation.get("triggered", False),
            })
        
        return {
            "total_vows": len(vows_history),
            "active_vow": self.active_vow.vow_id if self.active_vow else None,
            "liberation_count": self.liberation_count,
            "total_cycles": self.total_cycles,
            "clr": self.get_clr(),
            "clr_target_met": 0.1 <= self.get_clr() <= 0.4 if self.total_cycles > 0 else False,
            "stop_rule_satisfied": self.check_stop_rule_condition(),
            "vows": vows_history,
        }
    
    def get_active_vow(self) -> Optional[Vow]:
        """Get currently active vow."""
        return self.active_vow
