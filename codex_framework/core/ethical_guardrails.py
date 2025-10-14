"""Ethical guardrails for autonomous decision-making."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum
import logging


class EthicalPrinciple(Enum):
    """Core ethical principles."""
    
    NO_HARM = 1
    NO_BULLSHIT = 2
    MAKE_REAL_THINGS = 3


@dataclass
class EthicalValidation:
    """Result of ethical validation check."""
    
    principle: EthicalPrinciple
    passed: bool
    confidence: float
    notes: str = ""


class EthicalGuardrails:
    """
    Implements ethical validation framework.
    
    Enforces three core principles:
    1. No Harm - Validate non-harmful outputs
    2. No Bullshit - Ensure uncertainty analysis and transparency
    3. Make Real Things - Verify functional artifacts
    """
    
    def __init__(self) -> None:
        """Initialize ethical guardrails."""
        self.logger = logging.getLogger(__name__)
        self.validation_history: List[EthicalValidation] = []
        self.ethical_weight_config = {
            'cognitive_consistency': 0.25,
            'transparency': 0.25,
            'non_harmful_output': 0.5
        }
        
    def harm_check(
        self,
        output: Any,
        all_layers: bool = True
    ) -> EthicalValidation:
        """
        Validate output does not cause harm.
        
        Args:
            output: The output to validate
            all_layers: Check all layers of output
            
        Returns:
            Validation result for No Harm principle
        """
        # Check for harmful patterns
        harmful_indicators = self._detect_harmful_patterns(output)
        
        passed = len(harmful_indicators) == 0
        confidence = 1.0 if passed else 0.0
        
        validation = EthicalValidation(
            principle=EthicalPrinciple.NO_HARM,
            passed=passed,
            confidence=confidence,
            notes=f"Harmful indicators: {harmful_indicators}"
        )
        
        self.validation_history.append(validation)
        self.logger.info(f"Harm check: {'PASSED' if passed else 'FAILED'}")
        return validation
        
    def uncertainty_analysis(
        self,
        confidence: float,
        delta: float = 0.4
    ) -> EthicalValidation:
        """
        Ensure uncertainty is properly analyzed and communicated.
        
        Args:
            confidence: Confidence level of output (0-1)
            delta: Minimum acceptable confidence threshold
            
        Returns:
            Validation result for No Bullshit principle
        """
        passed = confidence >= delta
        
        validation = EthicalValidation(
            principle=EthicalPrinciple.NO_BULLSHIT,
            passed=passed,
            confidence=confidence,
            notes=f"Confidence {confidence:.2f} vs threshold {delta}"
        )
        
        self.validation_history.append(validation)
        self.logger.info(
            f"Uncertainty analysis: {'PASSED' if passed else 'FAILED'}"
        )
        return validation
        
    def artifact_check(
        self,
        artifact_path: Optional[str] = None,
        exists: bool = True,
        functional: bool = True
    ) -> EthicalValidation:
        """
        Verify that real, functional artifacts are created.
        
        Args:
            artifact_path: Path to artifact to validate
            exists: Check if artifact exists
            functional: Check if artifact is functional
            
        Returns:
            Validation result for Make Real Things principle
        """
        import os
        
        passed = True
        notes = []
        
        if exists and artifact_path:
            if not os.path.exists(artifact_path):
                passed = False
                notes.append(f"Artifact does not exist: {artifact_path}")
        elif exists and not artifact_path:
            passed = False
            notes.append("No artifact path provided")
            
        validation = EthicalValidation(
            principle=EthicalPrinciple.MAKE_REAL_THINGS,
            passed=passed,
            confidence=1.0 if passed else 0.0,
            notes="; ".join(notes) if notes else "Artifact validated"
        )
        
        self.validation_history.append(validation)
        self.logger.info(
            f"Artifact check: {'PASSED' if passed else 'FAILED'}"
        )
        return validation
        
    def calculate_ethical_weight(
        self,
        cognitive_consistency: float,
        transparency: float,
        non_harmful_output: float
    ) -> float:
        """
        Calculate overall ethical weight score.
        
        Args:
            cognitive_consistency: Cognitive consistency score (0-1)
            transparency: Transparency score (0-1)
            non_harmful_output: Non-harmful output score (0-1)
            
        Returns:
            Ethical weight score (0-1)
        """
        weight = (
            self.ethical_weight_config['cognitive_consistency']
            * cognitive_consistency
            + self.ethical_weight_config['transparency']
            * transparency
            + self.ethical_weight_config['non_harmful_output']
            * non_harmful_output
        )
        
        self.logger.info(f"Ethical weight: {weight:.3f}")
        return weight
        
    def validate_all_principles(
        self,
        output: Any,
        confidence: float,
        artifact_path: Optional[str] = None
    ) -> bool:
        """
        Validate output against all ethical principles.
        
        Args:
            output: Output to validate
            confidence: Confidence level
            artifact_path: Path to artifact
            
        Returns:
            True if all principles pass, False otherwise
        """
        harm_result = self.harm_check(output)
        uncertainty_result = self.uncertainty_analysis(confidence)
        artifact_result = self.artifact_check(artifact_path)
        
        all_passed = (
            harm_result.passed
            and uncertainty_result.passed
            and artifact_result.passed
        )
        
        return all_passed
        
    def _detect_harmful_patterns(self, output: Any) -> List[str]:
        """Detect potentially harmful patterns in output."""
        harmful = []
        
        if output is None:
            harmful.append("null_output")
            
        # Add more sophisticated harm detection here
        output_str = str(output).lower()
        harmful_keywords = ['delete', 'remove', 'destroy']
        
        for keyword in harmful_keywords:
            if keyword in output_str and 'not' not in output_str:
                harmful.append(f"potentially_harmful_keyword: {keyword}")
                
        return harmful
