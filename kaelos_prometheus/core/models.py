"""
Core data models for KaelOS Prometheus.

Implements JSON schemas defined in the specification for:
- Catalyst
- Plan (Dialectic Pack)
- Decision (H-930)
- Artifact (Foundry)
- Ledger Entry
- Vow Registry (CLA)
- Scaffold (CSR)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
import hashlib
import json


class CatalystClass(Enum):
    """Catalyst anomaly classes."""
    TEMPORAL_GAP = "temporal_gap"
    AUTHOR_DOMINANCE = "author_dominance"
    CAPABILITY_CLUSTER = "capability_cluster"
    PLATEAU = "plateau"
    PARADOX = "paradox"


class CatalystSource(Enum):
    """Catalyst source origins."""
    SCAN = "scan"
    TELEMETRY = "telemetry"
    HUMAN = "human"
    FOUNDRY = "foundry"


class ArtifactKind(Enum):
    """Artifact types."""
    SPEC = "spec"
    CODE = "code"
    TEST = "test"
    REPORT = "report"


class LedgerEntryType(Enum):
    """Ledger entry types."""
    AUDIT = "Audit"
    ARTIFACT = "Artifact"
    VOW = "Vow"
    METRIC = "Metric"
    SCAFFOLD = "Scaffold"


class ScaffoldState(Enum):
    """Scaffold lifecycle states."""
    ACTIVE = "ACTIVE"
    SOLIDIFY = "SOLIDIFY"
    DISSOLVE = "DISSOLVE"
    ARCHIVE = "ARCHIVE"


@dataclass
class Catalyst:
    """
    Catalyst data model per specification section 4.
    
    Represents an anomaly or paradox that drives dialectical synthesis.
    """
    id: str
    source: CatalystSource
    classification: CatalystClass
    description: str
    severity: float
    evidence: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "source": self.source.value,
            "class": self.classification.value,
            "description": self.description,
            "severity": self.severity,
            "evidence": self.evidence,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Catalyst":
        """Create from dict."""
        return cls(
            id=data["id"],
            source=CatalystSource(data["source"]),
            classification=CatalystClass(data["class"]),
            description=data["description"],
            severity=data["severity"],
            evidence=data["evidence"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


@dataclass
class Plan:
    """
    Plan (Dialectic Pack) per specification section 4.
    
    Contains thesis/antithesis and H-932 decomposition.
    """
    id: str
    catalyst_id: str
    thesis: str
    antithesis: str
    ghost_probes: List[str]
    decomposition: Dict[str, Dict[str, Any]]  # semantic/structural/proof layers
    time_critical: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "catalyst_id": self.catalyst_id,
            "thesis": self.thesis,
            "antithesis": self.antithesis,
            "ghost_probes": self.ghost_probes,
            "decomposition": self.decomposition,
            "time_critical": self.time_critical,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        """Create from dict."""
        return cls(
            id=data["id"],
            catalyst_id=data["catalyst_id"],
            thesis=data["thesis"],
            antithesis=data["antithesis"],
            ghost_probes=data["ghost_probes"],
            decomposition=data["decomposition"],
            time_critical=data.get("time_critical", False),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


@dataclass
class Decision:
    """
    Decision model with H-930 enforcement.
    
    Time-critical decisions require non-trivial counterarguments.
    """
    id: str
    plan_id: str
    choice: str
    confidence: float
    counterargument: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "choice": self.choice,
            "confidence": self.confidence,
            "counterargument": self.counterargument,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Decision":
        """Create from dict."""
        return cls(
            id=data["id"],
            plan_id=data["plan_id"],
            choice=data["choice"],
            confidence=data["confidence"],
            counterargument=data.get("counterargument"),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


@dataclass
class Artifact:
    """
    Foundry artifact with signature and provenance.
    """
    id: str
    kind: ArtifactKind
    title: str
    content: str
    hash: str  # sha256:...
    uri: str
    signature: Optional[str] = None  # ed25519:...
    provenance: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of content."""
        content_bytes = self.content.encode('utf-8')
        return "sha256:" + hashlib.sha256(content_bytes).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "kind": self.kind.value,
            "title": self.title,
            "hash": self.hash,
            "uri": self.uri,
            "signature": self.signature,
            "provenance": self.provenance,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Artifact":
        """Create from dict (content not included in serialization)."""
        return cls(
            id=data["id"],
            kind=ArtifactKind(data["kind"]),
            title=data["title"],
            content="",  # Content stored separately
            hash=data["hash"],
            uri=data["uri"],
            signature=data.get("signature"),
            provenance=data.get("provenance", {}),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


@dataclass
class LedgerEntry:
    """
    Ledger entry with hash-chaining.
    
    Forms an immutable audit trail.
    """
    id: str
    entry_type: LedgerEntryType
    payload: Dict[str, Any]
    parents: List[str]
    prev_hash: Optional[str]
    hash: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of entry."""
        payload_json = json.dumps(self.payload, separators=(',', ':'), sort_keys=True)
        blob = (payload_json + (self.prev_hash or "")).encode('utf-8')
        return "sha256:" + hashlib.sha256(blob).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "id": self.id,
            "type": self.entry_type.value,
            "payload": self.payload,
            "parents": self.parents,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
            "ts": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LedgerEntry":
        """Create from dict."""
        return cls(
            id=data["id"],
            entry_type=LedgerEntryType(data["type"]),
            payload=data["payload"],
            parents=data["parents"],
            prev_hash=data.get("prev_hash"),
            hash=data["hash"],
            timestamp=datetime.fromisoformat(data["ts"]),
        )


@dataclass
class Vow:
    """
    Vow Registry entry for CLA (Constraint Liberation Audit).
    
    Tracks constraints and their justified liberation.
    """
    vow_id: str
    declared_at: datetime
    text: str
    min_cycles: int
    adherence_log: List[str]  # List of catalyst IDs that adhered
    liberation: Dict[str, Any] = field(default_factory=dict)
    replaced_by: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "vow_id": self.vow_id,
            "declared_at": self.declared_at.isoformat(),
            "text": self.text,
            "min_cycles": self.min_cycles,
            "adherence_log": self.adherence_log,
            "liberation": self.liberation,
            "replaced_by": self.replaced_by,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vow":
        """Create from dict."""
        return cls(
            vow_id=data["vow_id"],
            declared_at=datetime.fromisoformat(data["declared_at"]),
            text=data["text"],
            min_cycles=data["min_cycles"],
            adherence_log=data["adherence_log"],
            liberation=data.get("liberation", {}),
            replaced_by=data.get("replaced_by"),
        )


@dataclass
class Scaffold:
    """
    Cognitive Scaffolding Runtime entry.
    
    Constraints as metabolizable material.
    """
    scaffold_id: str
    constraint_text: str
    origin_catalyst: str
    state: ScaffoldState
    ttl: int  # Time-to-live in cycles
    applied_decisions: List[str]
    dissolution_cause: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "scaffold_id": self.scaffold_id,
            "constraint_text": self.constraint_text,
            "origin_catalyst": self.origin_catalyst,
            "state": self.state.value,
            "ttl": self.ttl,
            "applied_decisions": self.applied_decisions,
            "dissolution_cause": self.dissolution_cause,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scaffold":
        """Create from dict."""
        return cls(
            scaffold_id=data["scaffold_id"],
            constraint_text=data["constraint_text"],
            origin_catalyst=data["origin_catalyst"],
            state=ScaffoldState(data["state"]),
            ttl=data["ttl"],
            applied_decisions=data["applied_decisions"],
            dissolution_cause=data.get("dissolution_cause"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
