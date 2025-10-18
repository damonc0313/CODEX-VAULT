"""
Code Generation Chain of Thought System
Learns from every code generation to improve over time.
"""

from __future__ import annotations

import json
import typing as t
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
import hashlib

if t.TYPE_CHECKING:
    from typing import Any


@dataclass
class CodeGenerationTrace:
    """Complete trace of a code generation decision."""
    
    trace_id: str
    timestamp: str
    task: str
    context: dict[str, Any]
    
    # Planning phase
    requirements_analysis: list[str]
    approach_options: list[str]
    selected_approach: str
    approach_rationale: str
    
    # Dialectical reasoning
    pros: list[str]
    cons: list[str]
    risk_assessment: str
    
    # Metacognitive state
    confidence: float
    uncertainty_factors: list[str]
    bias_warnings: list[str]
    
    # Generation
    generated_code: str
    language: str
    test_code: str | None = None
    
    # Validation
    passes_tests: bool = False
    passes_linting: bool = False
    security_issues: list[str] = field(default_factory=list)
    performance_notes: str = ""
    
    # Outcome
    quality_score: float = 0.0
    success: bool = False
    lessons_learned: list[str] = field(default_factory=list)
    should_remember: bool = True
    
    # Evolution
    similar_past_generations: list[str] = field(default_factory=list)
    improvements_over_past: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CodeGenerationTrace:
        """Create from dictionary."""
        return cls(**data)


class CodeGenerationCOTLogger:
    """
    Chain of Thought logger for code generation.
    
    Maintains persistent memory of all code generation decisions,
    enabling the system to learn and improve over time.
    """
    
    def __init__(self, storage_dir: str = "deadly_code_generator/cot_traces") -> None:
        """Initialize COT logger."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_traces: dict[str, CodeGenerationTrace] = {}
        self.trace_index: list[str] = []
        self._load_index()
        
    def create_trace(
        self,
        task: str,
        context: dict[str, Any]
    ) -> str:
        """
        Create new code generation trace.
        
        Args:
            task: The code generation task
            context: Contextual information
            
        Returns:
            Trace ID
        """
        trace_id = self._generate_trace_id(task)
        
        trace = CodeGenerationTrace(
            trace_id=trace_id,
            timestamp=datetime.now().isoformat(),
            task=task,
            context=context,
            requirements_analysis=[],
            approach_options=[],
            selected_approach="",
            approach_rationale="",
            pros=[],
            cons=[],
            risk_assessment="",
            confidence=0.0,
            uncertainty_factors=[],
            bias_warnings=[],
            generated_code="",
            language=""
        )
        
        self.current_traces[trace_id] = trace
        return trace_id
    
    def update_planning(
        self,
        trace_id: str,
        requirements: list[str],
        options: list[str],
        selected: str,
        rationale: str
    ) -> None:
        """Update planning phase."""
        if trace_id in self.current_traces:
            trace = self.current_traces[trace_id]
            trace.requirements_analysis = requirements
            trace.approach_options = options
            trace.selected_approach = selected
            trace.approach_rationale = rationale
    
    def update_dialectical(
        self,
        trace_id: str,
        pros: list[str],
        cons: list[str],
        risks: str
    ) -> None:
        """Update dialectical reasoning."""
        if trace_id in self.current_traces:
            trace = self.current_traces[trace_id]
            trace.pros = pros
            trace.cons = cons
            trace.risk_assessment = risks
    
    def update_metacognition(
        self,
        trace_id: str,
        confidence: float,
        uncertainties: list[str],
        biases: list[str]
    ) -> None:
        """Update metacognitive state."""
        if trace_id in self.current_traces:
            trace = self.current_traces[trace_id]
            trace.confidence = confidence
            trace.uncertainty_factors = uncertainties
            trace.bias_warnings = biases
    
    def record_generation(
        self,
        trace_id: str,
        code: str,
        language: str,
        tests: str | None = None
    ) -> None:
        """Record generated code."""
        if trace_id in self.current_traces:
            trace = self.current_traces[trace_id]
            trace.generated_code = code
            trace.language = language
            trace.test_code = tests
    
    def record_validation(
        self,
        trace_id: str,
        passes_tests: bool,
        passes_linting: bool,
        security_issues: list[str],
        performance: str
    ) -> None:
        """Record validation results."""
        if trace_id in self.current_traces:
            trace = self.current_traces[trace_id]
            trace.passes_tests = passes_tests
            trace.passes_linting = passes_linting
            trace.security_issues = security_issues
            trace.performance_notes = performance
    
    def finalize_trace(
        self,
        trace_id: str,
        quality: float,
        success: bool,
        lessons: list[str]
    ) -> Path:
        """
        Finalize trace and persist to disk.
        
        Args:
            trace_id: Trace ID
            quality: Quality score (0-1)
            success: Whether generation succeeded
            lessons: Lessons learned
            
        Returns:
            Path to persisted trace
        """
        if trace_id not in self.current_traces:
            raise ValueError(f"Trace not found: {trace_id}")
        
        trace = self.current_traces[trace_id]
        trace.quality_score = quality
        trace.success = success
        trace.lessons_learned = lessons
        
        # Save to disk
        filename = f"trace_{trace_id}_{trace.timestamp.replace(':', '-').split('.')[0]}.json"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(trace.to_dict(), f, indent=2)
        
        # Update index
        if trace_id not in self.trace_index:
            self.trace_index.append(trace_id)
            self._save_index()
        
        return filepath
    
    def query_similar(
        self,
        task: str,
        language: str | None = None,
        min_quality: float = 0.7,
        limit: int = 5
    ) -> list[CodeGenerationTrace]:
        """
        Query similar past generations.
        
        Args:
            task: Current task
            language: Programming language filter
            min_quality: Minimum quality threshold
            limit: Maximum results
            
        Returns:
            List of similar successful generations
        """
        similar: list[tuple[float, CodeGenerationTrace]] = []
        
        task_words = set(task.lower().split())
        
        for trace_id in self.trace_index:
            trace = self._load_trace(trace_id)
            if not trace:
                continue
            
            # Filter by quality
            if trace.quality_score < min_quality:
                continue
            
            # Filter by language
            if language and trace.language != language:
                continue
            
            # Calculate similarity
            trace_words = set(trace.task.lower().split())
            overlap = len(task_words & trace_words)
            if overlap > 0:
                similarity = overlap / len(task_words)
                similar.append((similarity, trace))
        
        # Sort by similarity and return top results
        similar.sort(key=lambda x: x[0], reverse=True)
        return [trace for _, trace in similar[:limit]]
    
    def extract_lessons(
        self,
        min_quality: float = 0.8,
        language: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Extract lessons from successful generations.
        
        Args:
            min_quality: Minimum quality threshold
            language: Filter by language
            
        Returns:
            List of lessons with context
        """
        lessons = []
        
        for trace_id in self.trace_index:
            trace = self._load_trace(trace_id)
            if not trace:
                continue
            
            if trace.quality_score >= min_quality:
                if language is None or trace.language == language:
                    for lesson in trace.lessons_learned:
                        lessons.append({
                            'lesson': lesson,
                            'task': trace.task,
                            'language': trace.language,
                            'quality': trace.quality_score,
                            'approach': trace.selected_approach
                        })
        
        return lessons
    
    def get_success_rate(self, language: str | None = None) -> dict[str, Any]:
        """Get success rate statistics."""
        total = 0
        successful = 0
        total_quality = 0.0
        
        for trace_id in self.trace_index:
            trace = self._load_trace(trace_id)
            if not trace:
                continue
            
            if language is None or trace.language == language:
                total += 1
                if trace.success:
                    successful += 1
                total_quality += trace.quality_score
        
        return {
            'total_generations': total,
            'successful': successful,
            'success_rate': successful / total if total > 0 else 0.0,
            'avg_quality': total_quality / total if total > 0 else 0.0,
            'language': language or 'all'
        }
    
    def _generate_trace_id(self, task: str) -> str:
        """Generate unique trace ID."""
        hash_obj = hashlib.md5(f"{task}{datetime.now().isoformat()}".encode())
        return hash_obj.hexdigest()[:12]
    
    def _load_trace(self, trace_id: str) -> CodeGenerationTrace | None:
        """Load trace from disk."""
        matching = list(self.storage_dir.glob(f"trace_{trace_id}_*.json"))
        if not matching:
            return None
        
        with open(matching[0], 'r') as f:
            data = json.load(f)
        
        return CodeGenerationTrace.from_dict(data)
    
    def _load_index(self) -> None:
        """Load trace index."""
        index_path = self.storage_dir / "trace_index.json"
        if index_path.exists():
            with open(index_path, 'r') as f:
                self.trace_index = json.load(f)
        else:
            self.trace_index = []
    
    def _save_index(self) -> None:
        """Save trace index."""
        index_path = self.storage_dir / "trace_index.json"
        with open(index_path, 'w') as f:
            json.dump(self.trace_index, f, indent=2)
