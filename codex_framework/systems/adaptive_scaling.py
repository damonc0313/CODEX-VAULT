"""Adaptive intelligence scaling system."""

from typing import Dict, Any
from dataclasses import dataclass
import logging


@dataclass
class ScalingParameters:
    """Dynamic scaling parameters."""
    
    learning_rate: float = 0.1
    reflection_depth: int = 3
    feedback_weighting: float = 0.5
    uncertainty_tolerance: float = 0.4


class AdaptiveScaling:
    """
    Adaptive intelligence scaling system.
    
    Dynamically adjusts cognitive parameters based on performance
    and intelligence index metrics.
    """
    
    def __init__(self) -> None:
        """Initialize adaptive scaling system."""
        self.logger = logging.getLogger(__name__)
        self.parameters = ScalingParameters()
        self.adjustment_history: list = []
        
    def adjust_parameters(
        self,
        cii: float,
        feedback_convergence: float,
        entropy: float,
        bias_detected: bool
    ) -> Dict[str, Any]:
        """
        Adjust parameters based on metrics.
        
        Args:
            cii: Current Codex Intelligence Index
            feedback_convergence: Feedback convergence rate
            entropy: Epistemic entropy level
            bias_detected: Whether bias was detected
            
        Returns:
            Adjustment report
        """
        adjustments = []
        
        # Increase learning rate if feedback convergence slow
        if feedback_convergence < 0.6:
            old_lr = self.parameters.learning_rate
            self.parameters.learning_rate = min(
                0.3,
                self.parameters.learning_rate * 1.2
            )
            adjustments.append(
                f"Learning rate: {old_lr:.3f} → "
                f"{self.parameters.learning_rate:.3f}"
            )
            
        # Deepen reflection if entropy high
        if entropy > 0.6:
            old_depth = self.parameters.reflection_depth
            self.parameters.reflection_depth = min(
                5,
                self.parameters.reflection_depth + 1
            )
            adjustments.append(
                f"Reflection depth: {old_depth} → "
                f"{self.parameters.reflection_depth}"
            )
            
        # Lower uncertainty tolerance if bias detected
        if bias_detected:
            old_tol = self.parameters.uncertainty_tolerance
            self.parameters.uncertainty_tolerance = max(
                0.2,
                self.parameters.uncertainty_tolerance - 0.05
            )
            adjustments.append(
                f"Uncertainty tolerance: {old_tol:.3f} → "
                f"{self.parameters.uncertainty_tolerance:.3f}"
            )
            
        # Scale feedback weighting based on CII
        if cii < 0.6:
            old_weight = self.parameters.feedback_weighting
            self.parameters.feedback_weighting = min(
                0.8,
                self.parameters.feedback_weighting + 0.1
            )
            adjustments.append(
                f"Feedback weighting: {old_weight:.3f} → "
                f"{self.parameters.feedback_weighting:.3f}"
            )
            
        report = {
            'adjustments_made': len(adjustments),
            'details': adjustments,
            'new_parameters': self.parameters
        }
        
        self.adjustment_history.append(report)
        
        self.logger.info(
            f"Adaptive scaling: {len(adjustments)} adjustments"
        )
        
        return report
        
    def get_parameters(self) -> ScalingParameters:
        """Get current scaling parameters."""
        return self.parameters
        
    def reset_parameters(self) -> None:
        """Reset parameters to defaults."""
        self.parameters = ScalingParameters()
        self.logger.info("Parameters reset to defaults")
