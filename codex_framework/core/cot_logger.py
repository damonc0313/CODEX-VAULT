"""Chain of Thought (COT) logging and reference system for decision evolution."""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json
import logging


@dataclass
class ChainOfThought:
    """
    Complete chain of thought record for a decision.
    
    Captures the full reasoning process to enable learning and evolution.
    """
    
    decision_id: str
    timestamp: str
    goal: str
    context: Dict[str, Any]
    
    # Analysis phase
    patterns_detected: List[str]
    causal_inference: Dict[str, List[str]]
    analysis_confidence: float
    
    # Reasoning phase
    thesis: str
    antithesis: str
    synthesis: str
    dialectical_confidence: float
    
    # Metacognitive state
    introspection_result: Dict[str, Any]
    cognitive_consistency: float
    bias_flags: List[str]
    
    # Ethical validation
    ethical_checks: Dict[str, bool]
    ethical_weight: float
    
    # Decision output
    final_decision: str
    decision_rationale: str
    confidence: float
    uncertainty: float
    
    # Outcome tracking
    outcome_status: Optional[str] = None
    quality_score: Optional[float] = None
    lessons_learned: List[str] = field(default_factory=list)
    
    # References
    related_decisions: List[str] = field(default_factory=list)
    innovation_applied: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChainOfThought':
        """Create from dictionary."""
        return cls(**data)


class COTLogger:
    """
    Chain of Thought logging system.
    
    Maintains persistent record of all reasoning processes
    to enable evolutionary learning and pattern recognition.
    """
    
    def __init__(self, cot_directory: str = "codex_framework/cot_records") -> None:
        """
        Initialize COT logger.
        
        Args:
            cot_directory: Directory for COT records
        """
        self.logger = logging.getLogger(__name__)
        self.cot_dir = Path(cot_directory)
        self.cot_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_cots: Dict[str, ChainOfThought] = {}
        self.cot_index: List[str] = []
        
        # Load existing index
        self._load_index()
        
    def create_cot(
        self,
        decision_id: str,
        goal: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Create new COT record.
        
        Args:
            decision_id: Unique decision identifier
            goal: Decision goal
            context: Decision context
            
        Returns:
            COT record ID
        """
        cot = ChainOfThought(
            decision_id=decision_id,
            timestamp=datetime.now().isoformat(),
            goal=goal,
            context=context,
            patterns_detected=[],
            causal_inference={},
            analysis_confidence=0.0,
            thesis="",
            antithesis="",
            synthesis="",
            dialectical_confidence=0.0,
            introspection_result={},
            cognitive_consistency=1.0,
            bias_flags=[],
            ethical_checks={},
            ethical_weight=0.0,
            final_decision="",
            decision_rationale="",
            confidence=0.0,
            uncertainty=1.0
        )
        
        self.current_cots[decision_id] = cot
        self.logger.info(f"Created COT record: {decision_id}")
        
        return decision_id
        
    def update_analysis_phase(
        self,
        decision_id: str,
        patterns: List[str],
        causal_inference: Dict[str, List[str]],
        confidence: float
    ) -> None:
        """
        Update COT with analysis phase data.
        
        Args:
            decision_id: Decision ID
            patterns: Detected patterns
            causal_inference: Causal relationships
            confidence: Analysis confidence
        """
        if decision_id not in self.current_cots:
            self.logger.warning(f"COT not found: {decision_id}")
            return
            
        cot = self.current_cots[decision_id]
        cot.patterns_detected = patterns
        cot.causal_inference = causal_inference
        cot.analysis_confidence = confidence
        
        self.logger.debug(f"Updated analysis phase: {decision_id}")
        
    def update_reasoning_phase(
        self,
        decision_id: str,
        thesis: str,
        antithesis: str,
        synthesis: str,
        confidence: float
    ) -> None:
        """
        Update COT with dialectical reasoning.
        
        Args:
            decision_id: Decision ID
            thesis: Argument for
            antithesis: Argument against
            synthesis: Reconciled position
            confidence: Dialectical confidence
        """
        if decision_id not in self.current_cots:
            return
            
        cot = self.current_cots[decision_id]
        cot.thesis = thesis
        cot.antithesis = antithesis
        cot.synthesis = synthesis
        cot.dialectical_confidence = confidence
        
        self.logger.debug(f"Updated reasoning phase: {decision_id}")
        
    def update_metacognition(
        self,
        decision_id: str,
        introspection: Dict[str, Any],
        consistency: float,
        biases: List[str]
    ) -> None:
        """
        Update COT with metacognitive state.
        
        Args:
            decision_id: Decision ID
            introspection: Introspection results
            consistency: Cognitive consistency score
            biases: Detected biases
        """
        if decision_id not in self.current_cots:
            return
            
        cot = self.current_cots[decision_id]
        cot.introspection_result = introspection
        cot.cognitive_consistency = consistency
        cot.bias_flags = biases
        
        self.logger.debug(f"Updated metacognition: {decision_id}")
        
    def update_ethical_validation(
        self,
        decision_id: str,
        checks: Dict[str, bool],
        weight: float
    ) -> None:
        """
        Update COT with ethical validation.
        
        Args:
            decision_id: Decision ID
            checks: Ethical check results
            weight: Ethical weight score
        """
        if decision_id not in self.current_cots:
            return
            
        cot = self.current_cots[decision_id]
        cot.ethical_checks = checks
        cot.ethical_weight = weight
        
        self.logger.debug(f"Updated ethical validation: {decision_id}")
        
    def finalize_decision(
        self,
        decision_id: str,
        decision: str,
        rationale: str,
        confidence: float,
        related_decisions: Optional[List[str]] = None
    ) -> None:
        """
        Finalize COT with decision output.
        
        Args:
            decision_id: Decision ID
            decision: Final decision
            rationale: Decision rationale
            confidence: Decision confidence
            related_decisions: Related decision IDs
        """
        if decision_id not in self.current_cots:
            return
            
        cot = self.current_cots[decision_id]
        cot.final_decision = decision
        cot.decision_rationale = rationale
        cot.confidence = confidence
        cot.uncertainty = 1.0 - confidence
        
        if related_decisions:
            cot.related_decisions = related_decisions
            
        self.logger.info(f"Finalized decision: {decision_id}")
        
    def record_outcome(
        self,
        decision_id: str,
        status: str,
        quality_score: float,
        lessons: Optional[List[str]] = None
    ) -> None:
        """
        Record outcome and lessons learned.
        
        Args:
            decision_id: Decision ID
            status: Outcome status
            quality_score: Quality score (0-1)
            lessons: Lessons learned
        """
        if decision_id not in self.current_cots:
            return
            
        cot = self.current_cots[decision_id]
        cot.outcome_status = status
        cot.quality_score = quality_score
        
        if lessons:
            cot.lessons_learned.extend(lessons)
            
        self.logger.info(
            f"Recorded outcome: {decision_id} - {status} "
            f"(quality: {quality_score:.2f})"
        )
        
    def persist_cot(self, decision_id: str) -> Path:
        """
        Persist COT to disk.
        
        Args:
            decision_id: Decision ID to persist
            
        Returns:
            Path to persisted file
        """
        if decision_id not in self.current_cots:
            raise ValueError(f"COT not found: {decision_id}")
            
        cot = self.current_cots[decision_id]
        
        # Create filename with timestamp
        timestamp = cot.timestamp.replace(':', '-').split('.')[0]
        filename = f"cot_{decision_id}_{timestamp}.json"
        filepath = self.cot_dir / filename
        
        # Write to file
        with open(filepath, 'w') as f:
            json.dump(cot.to_dict(), f, indent=2)
            
        # Update index
        if decision_id not in self.cot_index:
            self.cot_index.append(decision_id)
            self._save_index()
            
        self.logger.info(f"Persisted COT: {filepath}")
        
        return filepath
        
    def load_cot(self, decision_id: str) -> Optional[ChainOfThought]:
        """
        Load COT from disk.
        
        Args:
            decision_id: Decision ID to load
            
        Returns:
            COT record or None
        """
        # Find file
        matching_files = list(self.cot_dir.glob(f"cot_{decision_id}_*.json"))
        
        if not matching_files:
            self.logger.warning(f"COT file not found: {decision_id}")
            return None
            
        # Load most recent
        filepath = sorted(matching_files)[-1]
        
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        cot = ChainOfThought.from_dict(data)
        self.logger.info(f"Loaded COT: {decision_id}")
        
        return cot
        
    def query_similar_decisions(
        self,
        goal: str,
        context_keys: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[ChainOfThought]:
        """
        Query similar past decisions for learning.
        
        Args:
            goal: Current goal
            context_keys: Context keys to match
            limit: Maximum results
            
        Returns:
            List of similar COT records
        """
        similar: List[tuple[float, ChainOfThought]] = []
        
        for decision_id in self.cot_index:
            cot = self.load_cot(decision_id)
            if not cot:
                continue
                
            # Calculate similarity
            similarity = self._calculate_similarity(
                goal,
                context_keys or [],
                cot
            )
            
            similar.append((similarity, cot))
            
        # Sort by similarity and return top results
        similar.sort(key=lambda x: x[0], reverse=True)
        
        return [cot for _, cot in similar[:limit]]
        
    def extract_lessons_learned(
        self,
        min_quality: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Extract lessons learned from successful decisions.
        
        Args:
            min_quality: Minimum quality threshold
            
        Returns:
            List of lessons with context
        """
        lessons = []
        
        for decision_id in self.cot_index:
            cot = self.load_cot(decision_id)
            if not cot:
                continue
                
            # Filter by quality
            if cot.quality_score and cot.quality_score >= min_quality:
                for lesson in cot.lessons_learned:
                    lessons.append({
                        'lesson': lesson,
                        'decision_id': decision_id,
                        'goal': cot.goal,
                        'quality': cot.quality_score,
                        'confidence': cot.confidence
                    })
                    
        self.logger.info(f"Extracted {len(lessons)} lessons")
        
        return lessons
        
    def generate_evolution_report(self) -> Dict[str, Any]:
        """
        Generate report on decision-making evolution.
        
        Returns:
            Evolution metrics and trends
        """
        if not self.cot_index:
            return {'status': 'no_data'}
            
        total_decisions = len(self.cot_index)
        quality_scores = []
        confidence_scores = []
        ethical_passes = 0
        innovation_count = 0
        
        for decision_id in self.cot_index:
            cot = self.load_cot(decision_id)
            if not cot:
                continue
                
            if cot.quality_score is not None:
                quality_scores.append(cot.quality_score)
            confidence_scores.append(cot.confidence)
            
            if cot.ethical_checks and all(cot.ethical_checks.values()):
                ethical_passes += 1
                
            if cot.innovation_applied:
                innovation_count += 1
                
        avg_quality = (
            sum(quality_scores) / len(quality_scores)
            if quality_scores else 0.0
        )
        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores else 0.0
        )
        
        report = {
            'total_decisions': total_decisions,
            'avg_quality': avg_quality,
            'avg_confidence': avg_confidence,
            'ethical_pass_rate': ethical_passes / total_decisions,
            'innovation_rate': innovation_count / total_decisions,
            'lessons_count': sum(
                len(self.load_cot(did).lessons_learned or [])
                for did in self.cot_index
                if self.load_cot(did)
            )
        }
        
        self.logger.info(f"Evolution report: {report}")
        
        return report
        
    def _calculate_similarity(
        self,
        goal: str,
        context_keys: List[str],
        cot: ChainOfThought
    ) -> float:
        """Calculate similarity score between current and past decision."""
        similarity = 0.0
        
        # Goal similarity (simple keyword matching)
        goal_words = set(goal.lower().split())
        cot_goal_words = set(cot.goal.lower().split())
        if goal_words & cot_goal_words:
            similarity += 0.5
            
        # Context similarity
        if context_keys:
            cot_context_keys = set(cot.context.keys())
            overlap = len(set(context_keys) & cot_context_keys)
            if overlap > 0:
                similarity += 0.5 * (overlap / len(context_keys))
                
        return similarity
        
    def _load_index(self) -> None:
        """Load COT index from disk."""
        index_path = self.cot_dir / "cot_index.json"
        
        if index_path.exists():
            with open(index_path, 'r') as f:
                self.cot_index = json.load(f)
            self.logger.info(f"Loaded {len(self.cot_index)} COT records")
        else:
            self.cot_index = []
            
    def _save_index(self) -> None:
        """Save COT index to disk."""
        index_path = self.cot_dir / "cot_index.json"
        
        with open(index_path, 'w') as f:
            json.dump(self.cot_index, f, indent=2)
