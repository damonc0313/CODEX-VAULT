"""Diagnostic engine for cognitive health monitoring."""

from typing import Dict, Any, List
import logging


class DiagnosticsEngine:
    """
    Diagnostic engine for cognitive system health.
    
    Monitors:
    - Cognitive consistency
    - Feedback convergence rate
    - Epistemic entropy
    """
    
    def __init__(self) -> None:
        """Initialize diagnostics engine."""
        self.logger = logging.getLogger(__name__)
        self.consistency_history: List[float] = []
        self.feedback_history: List[Dict[str, Any]] = []
        self.entropy_history: List[float] = []
        
    def cognitive_consistency_check(
        self,
        decisions: List[Dict[str, Any]]
    ) -> float:
        """
        Check cognitive consistency across decisions.
        
        Args:
            decisions: List of decision records
            
        Returns:
            Consistency score (0-1)
        """
        if len(decisions) < 2:
            return 1.0
            
        # Check for contradictions
        contradictions = 0
        for i in range(len(decisions) - 1):
            curr = decisions[i]
            next_dec = decisions[i + 1]
            
            # Simplified contradiction detection
            if curr.get('decision') == next_dec.get('decision'):
                if curr.get('rationale') != next_dec.get('rationale'):
                    contradictions += 1
                    
        consistency = 1.0 - (contradictions / len(decisions))
        self.consistency_history.append(consistency)
        
        self.logger.info(f"Cognitive consistency: {consistency:.3f}")
        return consistency
        
    def feedback_convergence_rate(
        self,
        feedback: List[float]
    ) -> float:
        """
        Calculate rate of feedback convergence.
        
        Args:
            feedback: List of feedback scores
            
        Returns:
            Convergence rate
        """
        if len(feedback) < 3:
            return 0.5
            
        # Calculate variance trend
        recent = feedback[-5:] if len(feedback) >= 5 else feedback
        variance = sum(
            (x - sum(recent) / len(recent)) ** 2
            for x in recent
        ) / len(recent)
        
        # Lower variance = better convergence
        convergence = max(0.0, 1.0 - variance)
        
        self.logger.info(f"Feedback convergence: {convergence:.3f}")
        return convergence
        
    def epistemic_entropy_monitor(
        self,
        uncertainty_scores: List[float]
    ) -> float:
        """
        Monitor epistemic entropy (uncertainty).
        
        Args:
            uncertainty_scores: List of uncertainty measurements
            
        Returns:
            Entropy score
        """
        if not uncertainty_scores:
            return 0.5
            
        avg_uncertainty = sum(uncertainty_scores) / len(uncertainty_scores)
        
        # Track entropy trend
        entropy = avg_uncertainty
        self.entropy_history.append(entropy)
        
        self.logger.info(f"Epistemic entropy: {entropy:.3f}")
        return entropy
        
    def comprehensive_diagnostic(
        self,
        decisions: List[Dict[str, Any]],
        feedback: List[float],
        uncertainties: List[float]
    ) -> Dict[str, Any]:
        """
        Run comprehensive diagnostic check.
        
        Args:
            decisions: Decision history
            feedback: Feedback history
            uncertainties: Uncertainty history
            
        Returns:
            Complete diagnostic report
        """
        consistency = self.cognitive_consistency_check(decisions)
        convergence = self.feedback_convergence_rate(feedback)
        entropy = self.epistemic_entropy_monitor(uncertainties)
        
        # Overall health score
        health = (consistency + convergence + (1.0 - entropy)) / 3.0
        
        report = {
            'cognitive_consistency': consistency,
            'feedback_convergence': convergence,
            'epistemic_entropy': entropy,
            'overall_health': health,
            'status': 'healthy' if health > 0.7 else 'needs_attention',
            'recommendations': self._generate_recommendations(
                consistency,
                convergence,
                entropy
            )
        }
        
        self.logger.info(
            f"Diagnostic complete: {report['status']} "
            f"(health: {health:.3f})"
        )
        
        return report
        
    def _generate_recommendations(
        self,
        consistency: float,
        convergence: float,
        entropy: float
    ) -> List[str]:
        """Generate diagnostic recommendations."""
        recommendations = []
        
        if consistency < 0.7:
            recommendations.append(
                "Improve decision consistency through "
                "enhanced metacognitive reflection"
            )
            
        if convergence < 0.6:
            recommendations.append(
                "Increase feedback integration to improve convergence"
            )
            
        if entropy > 0.6:
            recommendations.append(
                "Reduce epistemic uncertainty through "
                "deeper analysis and evidence gathering"
            )
            
        return recommendations
