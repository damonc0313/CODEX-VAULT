"""Metacognitive reflection system for self-awareness and cognitive validation."""

from __future__ import annotations

import typing as t
from dataclasses import dataclass
import logging


@dataclass
class MetacognitiveMetrics:
    """Metrics for metacognitive assessment."""
    
    cognitive_consistency_index: float
    epistemic_uncertainty_score: float
    context_alignment_ratio: float
    confidence_level: float = 0.5


class MetacognitiveReflector:
    """
    Implements metacognitive rigour framework.
    
    Performs introspection, coherence validation, reasoning transparency,
    and ethical self-audit at critical decision points.
    """
    
    def __init__(self) -> None:
        """Initialize metacognitive reflector."""
        self.logger = logging.getLogger(__name__)
        self.metrics = MetacognitiveMetrics(
            cognitive_consistency_index=1.0,
            epistemic_uncertainty_score=0.0,
            context_alignment_ratio=1.0
        )
        self.decision_trace: List[Dict[str, Any]] = []
        self.bias_flags: List[str] = []
        
    def perform_introspective_scan(self) -> dict[str, t.Any]:
        """
        Execute introspective analysis of current cognitive state.
        
        Returns:
            Dict containing introspection results and detected patterns
        """
        scan_result = {
            'timestamp': self._get_timestamp(),
            'metrics': self.metrics,
            'bias_flags': self.bias_flags.copy(),
            'decision_trace_length': len(self.decision_trace),
            'status': 'healthy' if not self.bias_flags else 'needs_attention'
        }
        self.logger.info(f"Introspective scan: {scan_result['status']}")
        return scan_result
        
    def coherence_validation(self, context: dict[str, t.Any]) -> bool:
        """
        Validate coherence of reasoning with context.
        
        Args:
            context: Current operational context
            
        Returns:
            True if coherence is validated, False otherwise
        """
        if not context:
            return False
            
        # Calculate alignment between context and current state
        alignment_score = self._calculate_alignment(context)
        self.metrics.context_alignment_ratio = alignment_score
        
        is_coherent = alignment_score > 0.7
        self.logger.info(f"Coherence validation: {is_coherent}")
        return is_coherent
        
    def reasoning_transparency(
        self,
        decision: str,
        rationale: str
    ) -> dict[str, str]:
        """
        Create transparent record of reasoning process.
        
        Args:
            decision: The decision made
            rationale: Reasoning behind the decision
            
        Returns:
            Transparent reasoning record
        """
        record = {
            'decision': decision,
            'rationale': rationale,
            'timestamp': self._get_timestamp(),
            'confidence': str(self.metrics.confidence_level)
        }
        self.decision_trace.append(record)
        return record
        
    def ethical_self_audit(self) -> dict[str, t.Any]:
        """
        Perform ethical self-audit of recent actions.
        
        Returns:
            Audit results with ethical compliance status
        """
        audit = {
            'decisions_reviewed': len(self.decision_trace),
            'bias_count': len(self.bias_flags),
            'ethical_status': 'compliant',
            'recommendations': []
        }
        
        if self.bias_flags:
            audit['ethical_status'] = 'requires_review'
            audit['recommendations'].append('Address detected biases')
            
        return audit
        
    def detect_cognitive_biases(
        self,
        decision_pattern: list[str]
    ) -> list[str]:
        """
        Detect potential cognitive biases in decision patterns.
        
        Args:
            decision_pattern: Sequence of recent decisions
            
        Returns:
            List of detected bias types
        """
        detected_biases = []
        
        # Check for confirmation bias (repetitive patterns)
        if self._has_repetitive_pattern(decision_pattern):
            detected_biases.append('confirmation_bias')
            
        # Check for recency bias
        if len(decision_pattern) > 3:
            if decision_pattern[-1] == decision_pattern[-2]:
                detected_biases.append('recency_bias')
                
        self.bias_flags.extend(detected_biases)
        return detected_biases
        
    def recalibrate_confidence_thresholds(self) -> None:
        """Adjust confidence thresholds based on performance."""
        # Increase confidence if consistency is high
        if self.metrics.cognitive_consistency_index > 0.85:
            self.metrics.confidence_level = min(
                0.95,
                self.metrics.confidence_level + 0.05
            )
        # Decrease if uncertainty is high
        elif self.metrics.epistemic_uncertainty_score > 0.6:
            self.metrics.confidence_level = max(
                0.3,
                self.metrics.confidence_level - 0.05
            )
            
    def _calculate_alignment(self, context: dict[str, t.Any]) -> float:
        """Calculate alignment score between context and state."""
        if not context:
            return 0.0
        # Simplified alignment calculation
        return min(1.0, len(context) / 10.0)
        
    def _has_repetitive_pattern(self, pattern: list[str]) -> bool:
        """Check for repetitive patterns in decisions."""
        if len(pattern) < 3:
            return False
        return len(set(pattern[-3:])) == 1
        
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
