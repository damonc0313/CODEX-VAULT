"""Dialectical reasoning engine for balanced decision-making."""

from __future__ import annotations

import typing as t
from dataclasses import dataclass
import logging


@dataclass
class Argument:
    """Represents a logical argument."""
    
    position: str
    evidence: list[str]
    confidence: float
    reasoning: str


@dataclass
class Synthesis:
    """Result of dialectical synthesis."""
    
    thesis: Argument
    antithesis: Argument
    resolution: str
    confidence: float
    decision_trace: Dict[str, Any]


class DialecticalEngine:
    """
    Implements dialectical reasoning: thesis → antithesis → synthesis.
    
    Ensures balanced decision-making through structured argumentation
    and reduces cognitive biases through opposing viewpoints.
    """
    
    def __init__(self, confidence_threshold: float = 0.6) -> None:
        """
        Initialize dialectical engine.
        
        Args:
            confidence_threshold: Minimum confidence for synthesis
        """
        self.logger = logging.getLogger(__name__)
        self.confidence_threshold = confidence_threshold
        self.decision_traces: List[Dict[str, Any]] = []
        
    def generate_argument_for(
        self,
        proposition: str,
        context: Dict[str, Any]
    ) -> Argument:
        """
        Generate argument supporting proposition.
        
        Args:
            proposition: The proposition to support
            context: Contextual information
            
        Returns:
            Argument in favor of proposition
        """
        evidence = self._extract_supporting_evidence(proposition, context)
        confidence = self._calculate_argument_strength(evidence)
        
        argument = Argument(
            position=f"FOR: {proposition}",
            evidence=evidence,
            confidence=confidence,
            reasoning=f"Supporting {proposition} based on {len(evidence)} "
                     f"pieces of evidence"
        )
        
        self.logger.info(f"Generated thesis: {argument.position}")
        return argument
        
    def generate_argument_against(
        self,
        proposition: str,
        context: Dict[str, Any]
    ) -> Argument:
        """
        Generate argument opposing proposition.
        
        Args:
            proposition: The proposition to oppose
            context: Contextual information
            
        Returns:
            Argument against proposition
        """
        evidence = self._extract_opposing_evidence(proposition, context)
        confidence = self._calculate_argument_strength(evidence)
        
        argument = Argument(
            position=f"AGAINST: {proposition}",
            evidence=evidence,
            confidence=confidence,
            reasoning=f"Opposing {proposition} based on {len(evidence)} "
                     f"counterpoints"
        )
        
        self.logger.info(f"Generated antithesis: {argument.position}")
        return argument
        
    def reconcile(
        self,
        thesis: Argument,
        antithesis: Argument
    ) -> Synthesis:
        """
        Reconcile thesis and antithesis into synthesis.
        
        Args:
            thesis: Supporting argument
            antithesis: Opposing argument
            
        Returns:
            Synthesized resolution
        """
        # Weight arguments by confidence
        thesis_weight = thesis.confidence
        antithesis_weight = antithesis.confidence
        total_weight = thesis_weight + antithesis_weight

        if total_weight == 0:
            resolution = "Insufficient evidence for decision"
            confidence = 0.0
        else:
            # Synthesize based on relative strengths and absolute evidence weight
            if thesis_weight > antithesis_weight * 1.5:
                resolution = f"Accept proposition with modifications"
            elif antithesis_weight > thesis_weight * 1.5:
                resolution = f"Reject proposition"
            else:
                resolution = f"Compromise solution required"

            dominant_weight = max(thesis_weight, antithesis_weight)
            relative_strength = dominant_weight / total_weight
            absolute_scale = min(dominant_weight, total_weight / 2.0, 1.0)
            confidence = relative_strength * absolute_scale

        decision_trace = self._create_decision_trace(
            thesis,
            antithesis,
            resolution
        )
        
        synthesis = Synthesis(
            thesis=thesis,
            antithesis=antithesis,
            resolution=resolution,
            confidence=confidence,
            decision_trace=decision_trace
        )
        
        self.decision_traces.append(decision_trace)
        self.logger.info(f"Synthesis: {resolution} (confidence: {confidence})")
        
        return synthesis
        
    def dialectical_process(
        self,
        proposition: str,
        context: Dict[str, Any]
    ) -> Synthesis:
        """
        Execute full dialectical process.
        
        Args:
            proposition: Proposition to evaluate
            context: Contextual information
            
        Returns:
            Final synthesis
        """
        thesis = self.generate_argument_for(proposition, context)
        antithesis = self.generate_argument_against(proposition, context)
        synthesis = self.reconcile(thesis, antithesis)
        
        # Rerun if confidence too low
        if synthesis.confidence < self.confidence_threshold:
            self.logger.warning(
                f"Synthesis confidence {synthesis.confidence} below "
                f"threshold {self.confidence_threshold}"
            )
            # In real implementation, would gather more evidence
            # For now, flag for review
            synthesis.decision_trace['needs_review'] = True
            
        return synthesis
        
    def monitor_logical_balance(self) -> Dict[str, float]:
        """
        Monitor balance of logical argumentation.
        
        Returns:
            Metrics on logical balance
        """
        if not self.decision_traces:
            return {'balance_score': 0.5}
            
        # Calculate average confidence difference
        confidence_diffs = []
        for trace in self.decision_traces:
            thesis_conf = trace.get('thesis_confidence', 0.5)
            antithesis_conf = trace.get('antithesis_confidence', 0.5)
            confidence_diffs.append(abs(thesis_conf - antithesis_conf))
            
        avg_diff = sum(confidence_diffs) / len(confidence_diffs)
        balance_score = 1.0 - avg_diff  # Lower diff = better balance
        
        return {
            'balance_score': balance_score,
            'decisions_analyzed': len(self.decision_traces)
        }
        
    def flag_bias(self) -> List[str]:
        """
        Flag potential biases in decision-making.
        
        Returns:
            List of detected biases
        """
        biases = []
        
        balance = self.monitor_logical_balance()
        if balance['balance_score'] < 0.6:
            biases.append('systematic_bias')
            
        return biases
        
    def _extract_supporting_evidence(
        self,
        proposition: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """Extract evidence supporting proposition."""
        evidence = []
        # Simplified evidence extraction
        if context:
            for key, value in context.items():
                if value:
                    evidence.append(f"{key}: {value}")
        return evidence
        
    def _extract_opposing_evidence(
        self,
        proposition: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """Extract evidence opposing proposition."""
        evidence = []
        # Simplified counter-evidence extraction
        if not context or len(context) < 2:
            evidence.append("Insufficient context")
        return evidence
        
    def _calculate_argument_strength(
        self,
        evidence: List[str]
    ) -> float:
        """Calculate strength of argument from evidence."""
        if not evidence:
            return 0.0
        # Simplified strength calculation
        return min(1.0, len(evidence) / 5.0)
        
    def _create_decision_trace(
        self,
        thesis: Argument,
        antithesis: Argument,
        resolution: str
    ) -> Dict[str, Any]:
        """Create decision trace record."""
        return {
            'thesis_position': thesis.position,
            'thesis_confidence': thesis.confidence,
            'antithesis_position': antithesis.position,
            'antithesis_confidence': antithesis.confidence,
            'resolution': resolution,
            'timestamp': self._get_timestamp()
        }
        
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
