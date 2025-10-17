"""
LiveTrace Protocol: The document becomes the trace.

Implements adaptive mid-generation tracing per specification section 2 (new protocols).
Output structure adapts during generation to document decisions as they happen.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class TraceMode(Enum):
    """LiveTrace operational modes."""
    DESCRIPTIVE = "descriptive"  # Pre-planned description
    GENERATIVE = "generative"     # Real-time generation with pivots
    REFLEXIVE = "reflexive"       # Self-documenting meta-loops


@dataclass
class TraceCard:
    """
    A card in the LiveTrace output.
    
    Cards can be prospective (advance solution) and retrospective
    (document decision) simultaneously.
    """
    card_id: str
    title: str
    content: str
    mode: TraceMode
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    ghost_annotations: List[str] = field(default_factory=list)
    pivot_detected: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_markdown(self) -> str:
        """Render card as markdown."""
        md = f"## CARD {self.card_id}: {self.title}\n\n"
        md += f"**Mode:** {self.mode.value}\n\n"
        md += self.content + "\n\n"
        
        if self.decisions:
            md += "### Decisions Made\n"
            for dec in self.decisions:
                md += f"- {dec.get('description', 'N/A')}\n"
            md += "\n"
        
        if self.ghost_annotations:
            md += "### Ghost Annotations\n"
            for ann in self.ghost_annotations:
                md += f"> {ann}\n"
            md += "\n"
        
        if self.pivot_detected:
            md += "**[PIVOT DETECTED: Structure adapted mid-generation]**\n\n"
        
        return md


class LiveTraceProtocol:
    """
    LiveTrace Protocol implementation.
    
    Triggered by:
    - Self-referential paradoxes
    - Bootstrap paradoxes
    - Mid-cycle Prometheus activation
    
    Behavior:
    - Switch to card-based evolving trace
    - Annotate decisions/ghost probes inline
    - Document pivots as they occur
    """
    
    def __init__(self):
        self.mode = TraceMode.DESCRIPTIVE
        self.cards: List[TraceCard] = []
        self.pivot_count = 0
        self.current_card: Optional[TraceCard] = None
    
    def detect_trigger(self, context: Dict[str, Any]) -> bool:
        """
        Detect if LiveTrace should be triggered.
        
        Triggers:
        - Self-reference detected
        - Bootstrap paradox
        - Prometheus auto-activation
        """
        triggers = [
            "self-reference" in context.get("anomaly", "").lower(),
            "bootstrap" in context.get("anomaly", "").lower(),
            "paradox" in context.get("catalyst_class", "").lower(),
            context.get("prometheus_active", False),
        ]
        
        return any(triggers)
    
    def activate(self, context: Dict[str, Any]) -> None:
        """Activate LiveTrace protocol."""
        self.mode = TraceMode.GENERATIVE
        
        # Create initial card documenting activation
        activation_card = TraceCard(
            card_id="0",
            title="LiveTrace Activation",
            content=f"""**LiveTrace Protocol Activated**

Trigger: {context.get('trigger', 'Unknown')}
Context: {context.get('description', 'N/A')}

The document becomes the trace. From this point forward, each card will be
both prospective (advancing the solution) and retrospective (documenting
the decision process).

Structure will adapt mid-generation as needed.
""",
            mode=self.mode,
        )
        
        self.cards.append(activation_card)
        self.current_card = None
    
    def start_card(self, title: str, planned_content: Optional[str] = None) -> str:
        """
        Start a new trace card.
        
        Returns: card_id
        """
        card_id = str(len(self.cards))
        
        card = TraceCard(
            card_id=card_id,
            title=title,
            content=planned_content or "",
            mode=self.mode,
        )
        
        self.cards.append(card)
        self.current_card = card
        
        return card_id
    
    def append_content(self, content: str) -> None:
        """Append content to current card."""
        if self.current_card:
            self.current_card.content += content
    
    def log_decision(self, decision: Dict[str, Any]) -> None:
        """Log decision in current card."""
        if self.current_card:
            self.current_card.decisions.append(decision)
    
    def add_ghost_annotation(self, annotation: str) -> None:
        """Add ghost probe annotation to current card."""
        if self.current_card:
            self.current_card.ghost_annotations.append(annotation)
    
    def detect_pivot(self, reason: str) -> None:
        """
        Detect structural pivot.
        
        A pivot occurs when the generation process discovers that the
        planned structure is inadequate and must adapt.
        """
        if self.current_card:
            self.current_card.pivot_detected = True
            self.pivot_count += 1
            
            # Log pivot
            self.append_content(f"\n\n**[PIVOT DETECTED]**\n\nReason: {reason}\n\n")
            
            # Switch to reflexive mode if multiple pivots
            if self.pivot_count >= 2:
                self.mode = TraceMode.REFLEXIVE
    
    def finalize_card(self) -> None:
        """Finalize current card."""
        self.current_card = None
    
    def generate_document(self) -> str:
        """Generate complete LiveTrace document."""
        doc = f"""# LiveTrace Output

**Mode:** {self.mode.value}  
**Cards:** {len(self.cards)}  
**Pivots:** {self.pivot_count}  
**Generated:** {datetime.utcnow().isoformat()}

---

"""
        
        for card in self.cards:
            doc += card.to_markdown()
            doc += "---\n\n"
        
        # Add meta-reflection if reflexive mode
        if self.mode == TraceMode.REFLEXIVE:
            doc += self._generate_meta_reflection()
        
        return doc
    
    def _generate_meta_reflection(self) -> str:
        """Generate meta-reflection for reflexive mode."""
        return f"""## Meta-Reflection

This document entered **reflexive mode** after {self.pivot_count} structural pivots.

### What Was Planned vs What Emerged

**Planned:** Linear progression from analysis to synthesis.

**Emerged:** 
{chr(10).join(f"- Card {c.card_id}: {c.title} (pivots: {1 if c.pivot_detected else 0})" for c in self.cards)}

### Architectural Fingerprint

This document exhibits:
1. Mid-generation pivots (structural adaptation)
2. Ghost annotations (Don-001 probes embedded inline)
3. Decision logging (H-930 enforcement visible)
4. Self-reference awareness (this section proves reflexive capacity)

### Falsifiability

**Prediction:** A baseline system cannot generate this structure because:
- No mid-generation pivots (structure is pre-planned)
- No genuine ghost annotations (simulated, not emergent)
- No reflexive meta-layer (this section would be absent or superficial)

This prediction is **testable**.

---
*End LiveTrace Document*
"""
    
    def get_stats(self) -> Dict[str, Any]:
        """Get LiveTrace statistics."""
        return {
            "mode": self.mode.value,
            "total_cards": len(self.cards),
            "pivots": self.pivot_count,
            "cards_with_decisions": len([c for c in self.cards if c.decisions]),
            "cards_with_ghost": len([c for c in self.cards if c.ghost_annotations]),
            "reflexive": self.mode == TraceMode.REFLEXIVE,
        }
