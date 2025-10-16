"""Central cognitive processing core."""

from __future__ import annotations

import typing as t
import logging

if t.TYPE_CHECKING:
    from .metacognition import MetacognitiveReflector
    from .ethical_guardrails import EthicalGuardrails
    from .dialectical_engine import DialecticalEngine
    from .rigor_enforcer import RigorEnforcer
else:
    from .metacognition import MetacognitiveReflector
    from .ethical_guardrails import EthicalGuardrails
    from .dialectical_engine import DialecticalEngine
    from .rigor_enforcer import RigorEnforcer


class CognitiveCore:
    """
    Central cognitive processing system.
    
    Integrates metacognition, ethics, dialectics, and rigor
    for comprehensive decision-making.
    """
    
    def __init__(self) -> None:
        """Initialize cognitive core with all subsystems."""
        self.logger = logging.getLogger(__name__)
        self.metacognition = MetacognitiveReflector()
        self.ethics = EthicalGuardrails()
        self.dialectics = DialecticalEngine()
        self.rigor = RigorEnforcer()
        self.state: Dict[str, Any] = {
            'mode': 'idle',
            'active': True,
            'version': '4.0'
        }
        
    def process_decision(
        self,
        proposition: str,
        context: dict[str, t.Any]
    ) -> dict[str, t.Any]:
        """
        Process decision through full cognitive pipeline.
        
        Args:
            proposition: Decision to make
            context: Contextual information
            
        Returns:
            Decision result with full cognitive trace
        """
        # 1. Metacognitive introspection
        self.metacognition.perform_introspective_scan()
        
        # 2. Dialectical processing
        synthesis = self.dialectics.dialectical_process(proposition, context)
        
        # 3. Ethical validation
        ethical_check = self.ethics.uncertainty_analysis(
            synthesis.confidence
        )
        
        # 4. Coherence validation
        is_coherent = self.metacognition.coherence_validation(context)
        
        # 5. Record reasoning
        reasoning_record = self.metacognition.reasoning_transparency(
            decision=synthesis.resolution,
            rationale=synthesis.thesis.reasoning
        )
        
        result = {
            'decision': synthesis.resolution,
            'confidence': synthesis.confidence,
            'ethical_status': ethical_check.passed,
            'coherent': is_coherent,
            'reasoning': reasoning_record,
            'synthesis': synthesis
        }
        
        self.logger.info(f"Decision processed: {synthesis.resolution}")
        return result
        
    def validate_artifact(
        self,
        code: str,
        artifact_path: str | None = None
    ) -> dict[str, t.Any]:
        """
        Validate code artifact through rigor and ethical checks.
        
        Args:
            code: Code to validate
            artifact_path: Path to artifact file
            
        Returns:
            Validation results
        """
        # Rigor validation
        rigor_metrics = self.rigor.validate_all(code)
        
        # Ethical validation
        ethical_valid = self.ethics.validate_all_principles(
            output=code,
            confidence=0.9 if rigor_metrics.passed else 0.3,
            artifact_path=artifact_path
        )
        
        # Metacognitive audit
        audit = self.metacognition.ethical_self_audit()
        
        result = {
            'rigor_passed': rigor_metrics.passed,
            'ethical_passed': ethical_valid,
            'metrics': rigor_metrics,
            'audit': audit,
            'recommendations': self.rigor.refactor_or_flag(rigor_metrics)
        }
        
        return result
        
    def set_mode(self, mode: str) -> None:
        """
        Set operational mode.
        
        Args:
            mode: New operational mode
        """
        self.state['mode'] = mode
        self.logger.info(f"Mode changed to: {mode}")
        
    def get_status(self) -> dict[str, t.Any]:
        """
        Get current cognitive core status.
        
        Returns:
            Status information
        """
        return {
            'state': self.state,
            'metacognitive_metrics': self.metacognition.metrics,
            'dialectical_balance': self.dialectics.monitor_logical_balance(),
            'ethical_history_length': len(self.ethics.validation_history)
        }
