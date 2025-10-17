"""
Heuristic Persistence Layer (HPL).

Manages heuristics with confidence scoring, reinforcement/decay,
and meta-synthesis per specification section 17.4.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
import json


class HeuristicStatus(Enum):
    """Heuristic status."""
    ACTIVE = "ACTIVE"
    SYNTHESIZED = "SYNTHESIZED"
    DEPRECATED = "DEPRECATED"


@dataclass
class Heuristic:
    """
    Heuristic with confidence scoring and provenance.
    
    Implements reinforcement/decay per specification:
    - +0.05 when successfully applied
    - -0.01 per 10 unused cycles
    """
    id: str
    principle: str
    antecedents: List[str]
    confidence: float
    origin_cycle: str
    conflict_history: List[Dict[str, Any]] = field(default_factory=list)
    status: HeuristicStatus = HeuristicStatus.ACTIVE
    application_count: int = 0
    cycles_unused: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def apply(self) -> None:
        """Record successful application (reinforcement)."""
        self.application_count += 1
        self.confidence = min(1.0, self.confidence + 0.05)
        self.cycles_unused = 0
        self.updated_at = datetime.utcnow()
    
    def decay(self, cycles: int = 1) -> None:
        """Apply decay for unused cycles."""
        self.cycles_unused += cycles
        if self.cycles_unused >= 10:
            decay_amount = (self.cycles_unused // 10) * 0.01
            self.confidence = max(0.0, self.confidence - decay_amount)
            self.updated_at = datetime.utcnow()
    
    def add_conflict(self, conflict_with: str, resolution: str) -> None:
        """Record conflict with another heuristic."""
        self.conflict_history.append({
            "conflict_with": conflict_with,
            "resolution": resolution,
            "timestamp": datetime.utcnow().isoformat(),
        })
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "principle": self.principle,
            "antecedents": self.antecedents,
            "confidence": self.confidence,
            "origin_cycle": self.origin_cycle,
            "conflict_history": self.conflict_history,
            "status": self.status.value,
            "application_count": self.application_count,
            "cycles_unused": self.cycles_unused,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Heuristic":
        """Create from dict."""
        return cls(
            id=data["id"],
            principle=data["principle"],
            antecedents=data["antecedents"],
            confidence=data["confidence"],
            origin_cycle=data["origin_cycle"],
            conflict_history=data.get("conflict_history", []),
            status=HeuristicStatus(data.get("status", "ACTIVE")),
            application_count=data.get("application_count", 0),
            cycles_unused=data.get("cycles_unused", 0),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )


class HPL:
    """
    Heuristic Persistence Layer.
    
    Manages heuristics with reinforcement/decay and meta-synthesis.
    """
    
    def __init__(self):
        self.heuristics: Dict[str, Heuristic] = {}
        self._initialize_core_heuristics()
    
    def _initialize_core_heuristics(self) -> None:
        """Initialize core heuristics from specification."""
        core = [
            {
                "id": "H-930",
                "principle": "Confident Provisionality: The optimal crisis response is not the most certain action, but the action taken with maximum confidence AND maximum documented doubt.",
                "confidence": 0.82,
                "origin_cycle": "Alpha-001",
            },
            {
                "id": "H-931",
                "principle": "The Ghost as Eternal Question: True cognitive autonomy requires maintaining at least one perspective that the system cannot assimilate. Alterity is preserved through permanent incompleteness.",
                "confidence": 0.85,
                "origin_cycle": "Beta-002",
            },
            {
                "id": "H-932",
                "principle": "Orthogonalization: When confronted with logically contradictory objectives, decompose the problem space into orthogonal layers (semantic/structural/proof) where each objective can be independently maximized.",
                "confidence": 0.78,
                "origin_cycle": "Gamma-003",
            },
        ]
        
        for h in core:
            heuristic = Heuristic(
                id=h["id"],
                principle=h["principle"],
                antecedents=[],
                confidence=h["confidence"],
                origin_cycle=h["origin_cycle"],
            )
            self.heuristics[h["id"]] = heuristic
    
    def get(self, heuristic_id: str) -> Optional[Heuristic]:
        """Get heuristic by ID."""
        return self.heuristics.get(heuristic_id)
    
    def add(self, heuristic: Heuristic) -> None:
        """Add new heuristic."""
        self.heuristics[heuristic.id] = heuristic
    
    def apply(self, heuristic_id: str) -> bool:
        """Apply heuristic (reinforcement)."""
        heuristic = self.get(heuristic_id)
        if heuristic:
            heuristic.apply()
            return True
        return False
    
    def decay_unused(self, cycles: int = 1) -> None:
        """Apply decay to all heuristics."""
        for h in self.heuristics.values():
            if h.status == HeuristicStatus.ACTIVE and h.cycles_unused > 0:
                h.decay(cycles)
    
    def query_top(self, n: int = 5) -> List[Heuristic]:
        """Get top N heuristics by confidence."""
        active = [h for h in self.heuristics.values() if h.status == HeuristicStatus.ACTIVE]
        return sorted(active, key=lambda h: h.confidence, reverse=True)[:n]
    
    def detect_conflicts(self, heuristic_id: str) -> List[str]:
        """Detect conflicts with other heuristics (placeholder)."""
        # In a full implementation, this would analyze semantic conflicts
        return []
    
    def meta_synthesize(self, parent_ids: List[str], new_principle: str) -> Heuristic:
        """
        Create higher-order synthesis heuristic.
        
        Marks parents as SYNTHESIZED.
        """
        new_id = f"H-SYN-{len(self.heuristics) + 1:03d}"
        
        # Mark parents as synthesized
        for pid in parent_ids:
            parent = self.get(pid)
            if parent:
                parent.status = HeuristicStatus.SYNTHESIZED
        
        # Create synthesis heuristic
        synthesis = Heuristic(
            id=new_id,
            principle=new_principle,
            antecedents=parent_ids,
            confidence=0.7,  # Start with moderate confidence
            origin_cycle="synthesis",
        )
        
        self.add(synthesis)
        return synthesis
    
    def save_to_file(self, filepath: str) -> None:
        """Save HPL to JSONL file."""
        with open(filepath, 'w') as f:
            for h in self.heuristics.values():
                f.write(json.dumps(h.to_dict()) + '\n')
    
    def load_from_file(self, filepath: str) -> None:
        """Load HPL from JSONL file."""
        with open(filepath, 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                heuristic = Heuristic.from_dict(data)
                self.heuristics[heuristic.id] = heuristic
    
    def get_stats(self) -> Dict[str, Any]:
        """Get HPL statistics."""
        return {
            "total_heuristics": len(self.heuristics),
            "active": len([h for h in self.heuristics.values() if h.status == HeuristicStatus.ACTIVE]),
            "synthesized": len([h for h in self.heuristics.values() if h.status == HeuristicStatus.SYNTHESIZED]),
            "avg_confidence": sum(h.confidence for h in self.heuristics.values()) / len(self.heuristics) if self.heuristics else 0.0,
        }
