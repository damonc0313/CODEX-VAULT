"""Codex Intelligence Index (CII) monitoring and adaptive scaling."""

from dataclasses import dataclass
from typing import Dict, Any
import logging


@dataclass
class IntelligenceMetrics:
    """Metrics for intelligence assessment."""
    
    adaptability_score: float = 0.5
    ethical_stability_index: float = 1.0
    reasoning_depth: float = 0.5
    innovation_rate: float = 0.0
    clarity_index: float = 0.5


class IntelligenceIndexMonitor:
    """
    Monitor and calculate Codex Intelligence Index (CII).
    
    CII = (adaptability + clarity + ethical_stability
           + innovation_rate + reasoning_depth) / 5
    
    Triggers adaptive scaling when CII falls below threshold.
    """
    
    def __init__(self, threshold: float = 0.6) -> None:
        """
        Initialize intelligence index monitor.
        
        Args:
            threshold: Minimum acceptable CII
        """
        self.logger = logging.getLogger(__name__)
        self.threshold = threshold
        self.metrics = IntelligenceMetrics()
        self.history: list = []
        
    def update_adaptability(self, score: float) -> None:
        """Update adaptability score."""
        self.metrics.adaptability_score = max(0.0, min(1.0, score))
        
    def update_ethical_stability(self, index: float) -> None:
        """Update ethical stability index."""
        self.metrics.ethical_stability_index = max(0.0, min(1.0, index))
        
    def update_reasoning_depth(self, depth: float) -> None:
        """Update reasoning depth."""
        self.metrics.reasoning_depth = max(0.0, min(1.0, depth))
        
    def update_innovation_rate(self, rate: float) -> None:
        """Update innovation rate."""
        self.metrics.innovation_rate = max(0.0, min(1.0, rate))
        
    def update_clarity(self, clarity: float) -> None:
        """Update clarity index."""
        self.metrics.clarity_index = max(0.0, min(1.0, clarity))
        
    def calculate_cii(self) -> float:
        """
        Calculate Codex Intelligence Index.
        
        Returns:
            CII score (0-1)
        """
        cii = (
            self.metrics.adaptability_score
            + self.metrics.clarity_index
            + self.metrics.ethical_stability_index
            + self.metrics.innovation_rate
            + self.metrics.reasoning_depth
        ) / 5.0
        
        self.history.append({
            'cii': cii,
            'metrics': self.metrics
        })
        
        self.logger.info(f"CII calculated: {cii:.3f}")
        
        # Trigger adaptive scaling if needed
        if cii < self.threshold:
            self.logger.warning(
                f"CII {cii:.3f} below threshold {self.threshold}"
            )
            self.trigger_adaptive_scaling()
            
        return cii
        
    def trigger_adaptive_scaling(self) -> Dict[str, Any]:
        """
        Trigger adaptive scaling adjustments.
        
        Returns:
            Scaling adjustments made
        """
        adjustments = {
            'action': 'adaptive_scaling_triggered',
            'recommendations': []
        }
        
        # Analyze weak areas
        if self.metrics.adaptability_score < 0.5:
            adjustments['recommendations'].append(
                'increase_learning_rate'
            )
            
        if self.metrics.reasoning_depth < 0.5:
            adjustments['recommendations'].append(
                'deepen_reflection'
            )
            
        if self.metrics.innovation_rate < 0.3:
            adjustments['recommendations'].append(
                'activate_innovation_protocol'
            )
            
        self.logger.info(
            f"Adaptive scaling: {len(adjustments['recommendations'])} "
            f"adjustments"
        )
        
        return adjustments
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current intelligence status.
        
        Returns:
            Status report with CII and metrics
        """
        current_cii = self.calculate_cii()
        
        return {
            'cii': current_cii,
            'threshold': self.threshold,
            'status': 'healthy' if current_cii >= self.threshold else 'scaling',
            'metrics': {
                'adaptability': self.metrics.adaptability_score,
                'ethical_stability': self.metrics.ethical_stability_index,
                'reasoning_depth': self.metrics.reasoning_depth,
                'innovation_rate': self.metrics.innovation_rate,
                'clarity': self.metrics.clarity_index
            }
        }
