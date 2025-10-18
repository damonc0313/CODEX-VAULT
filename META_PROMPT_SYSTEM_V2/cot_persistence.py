"""
COT Persistence Layer v2.0
Automatic saving and pattern recognition from decision traces.

DISCOVERED THROUGH RECURSIVE SELF-ANALYSIS:
- v1.0 had no automatic COT saving
- v1.0 had no cross-session memory
- v1.0 had no pattern recognition
- This enables TRUE learning
"""

from __future__ import annotations

import typing as t
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json
import hashlib

if t.TYPE_CHECKING:
    from typing import Any


@dataclass
class DecisionTrace:
    """Complete trace of a code generation decision."""
    
    trace_id: str
    timestamp: str
    request: str
    context: dict[str, Any]
    
    # Protocol outputs
    metacog_findings: dict[str, Any]
    blind_spots_found: list[str]
    dialectic_synthesis: dict[str, Any]
    
    # Generation
    generated_code: str
    language: str
    
    # Outcome
    quality_score: float
    success: bool
    confidence_predicted: float
    confidence_actual: float
    
    # Learning
    lessons_learned: list[str]
    patterns_identified: list[str]


@dataclass
class Pattern:
    """A recognized pattern from COT traces."""
    
    pattern_id: str
    pattern_type: str  # 'blind_spot', 'success_strategy', 'failure_mode'
    description: str
    frequency: int
    effectiveness: float  # 0-1
    examples: list[str]  # trace_ids where this appears


class COTPersistenceLayer:
    """
    Automatic COT persistence and pattern recognition.
    
    NEW IN V2.0:
    - Auto-saves every decision trace
    - Queries similar past decisions
    - Extracts patterns automatically
    - Enables cross-session learning
    - Suggests improvements based on patterns
    """
    
    def __init__(self, storage_dir: str = "META_PROMPT_SYSTEM_V2/cot_traces") -> None:
        """Initialize persistence layer."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.trace_index: list[str] = []
        self.pattern_cache: dict[str, Pattern] = {}
        
        self._load_index()
        self._load_patterns()
    
    def save_trace(self, trace: DecisionTrace) -> Path:
        """
        Automatically save decision trace.
        
        NEW IN V2.0: This happens AUTOMATICALLY, not manually
        
        Args:
            trace: Complete decision trace
            
        Returns:
            Path to saved trace
        """
        # Generate filename
        timestamp = trace.timestamp.replace(':', '-').split('.')[0]
        filename = f"trace_{trace.trace_id}_{timestamp}.json"
        filepath = self.storage_dir / filename
        
        # Save trace
        with open(filepath, 'w') as f:
            json.dump(asdict(trace), f, indent=2)
        
        # Update index
        if trace.trace_id not in self.trace_index:
            self.trace_index.append(trace.trace_id)
            self._save_index()
        
        # Trigger pattern analysis
        self._analyze_new_trace(trace)
        
        return filepath
    
    def query_similar(
        self,
        request: str,
        context: dict[str, Any],
        min_quality: float = 0.7,
        limit: int = 5
    ) -> list[DecisionTrace]:
        """
        Query similar past decisions.
        
        NEW IN V2.0: Enables learning from past successes
        
        Args:
            request: Current request
            context: Current context
            min_quality: Minimum quality threshold
            limit: Maximum results
            
        Returns:
            List of similar high-quality traces
        """
        similar: list[tuple[float, DecisionTrace]] = []
        
        request_words = set(request.lower().split())
        
        for trace_id in self.trace_index:
            trace = self._load_trace(trace_id)
            if not trace:
                continue
            
            # Filter by quality
            if trace.quality_score < min_quality:
                continue
            
            # Calculate similarity
            trace_words = set(trace.request.lower().split())
            overlap = len(request_words & trace_words)
            
            if overlap > 0:
                similarity = overlap / len(request_words)
                similar.append((similarity, trace))
        
        # Sort and return top results
        similar.sort(key=lambda x: x[0], reverse=True)
        return [trace for _, trace in similar[:limit]]
    
    def extract_patterns(self) -> dict[str, list[Pattern]]:
        """
        Extract patterns from all traces.
        
        NEW IN V2.0: Automatic pattern recognition
        
        Returns:
            Dictionary of pattern types to patterns
        """
        blind_spot_patterns = self._find_blind_spot_patterns()
        success_patterns = self._find_success_patterns()
        failure_patterns = self._find_failure_patterns()
        
        return {
            'blind_spots': blind_spot_patterns,
            'success_strategies': success_patterns,
            'failure_modes': failure_patterns
        }
    
    def get_lessons_learned(
        self,
        min_quality: float = 0.8,
        language: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get lessons from successful decisions.
        
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
                            'trace_id': trace_id,
                            'request': trace.request,
                            'quality': trace.quality_score,
                            'patterns': trace.patterns_identified
                        })
        
        return lessons
    
    def suggest_improvements(
        self,
        current_request: str,
        current_context: dict[str, Any]
    ) -> list[str]:
        """
        Suggest improvements based on patterns.
        
        NEW IN V2.0: Learns from past to improve present
        
        Args:
            current_request: Current request
            current_context: Current context
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Find similar past decisions
        similar = self.query_similar(current_request, current_context, min_quality=0.8)
        
        if similar:
            # Extract common successful patterns
            common_patterns = self._find_common_patterns([s.patterns_identified for s in similar])
            
            for pattern in common_patterns:
                suggestions.append(f"Pattern from past successes: {pattern}")
        
        # Check for known blind spots
        blind_spot_patterns = self.pattern_cache.get('blind_spot', [])
        for pattern in blind_spot_patterns[:3]:  # Top 3
            if pattern.frequency > 2:
                suggestions.append(
                    f"Common blind spot: {pattern.description} "
                    f"(found {pattern.frequency} times)"
                )
        
        return suggestions
    
    def get_statistics(self) -> dict[str, Any]:
        """
        Get persistence statistics.
        
        Returns:
            Statistics about stored traces
        """
        total = len(self.trace_index)
        
        if total == 0:
            return {'total_traces': 0}
        
        qualities = []
        successes = 0
        languages = {}
        
        for trace_id in self.trace_index:
            trace = self._load_trace(trace_id)
            if not trace:
                continue
            
            qualities.append(trace.quality_score)
            if trace.success:
                successes += 1
            
            languages[trace.language] = languages.get(trace.language, 0) + 1
        
        return {
            'total_traces': total,
            'average_quality': sum(qualities) / len(qualities) if qualities else 0,
            'success_rate': successes / total,
            'languages': languages,
            'patterns_found': len(self.pattern_cache),
            'cross_session_learning': 'ENABLED'
        }
    
    # ========== PRIVATE METHODS ==========
    
    def _generate_trace_id(self, request: str) -> str:
        """Generate unique trace ID."""
        hash_obj = hashlib.md5(f"{request}{datetime.now().isoformat()}".encode())
        return hash_obj.hexdigest()[:12]
    
    def _load_trace(self, trace_id: str) -> DecisionTrace | None:
        """Load trace from disk."""
        matching = list(self.storage_dir.glob(f"trace_{trace_id}_*.json"))
        if not matching:
            return None
        
        with open(matching[0], 'r') as f:
            data = json.load(f)
        
        return DecisionTrace(**data)
    
    def _load_index(self) -> None:
        """Load trace index."""
        index_path = self.storage_dir / "trace_index.json"
        if index_path.exists():
            with open(index_path, 'r') as f:
                self.trace_index = json.load(f)
    
    def _save_index(self) -> None:
        """Save trace index."""
        index_path = self.storage_dir / "trace_index.json"
        with open(index_path, 'w') as f:
            json.dump(self.trace_index, f, indent=2)
    
    def _load_patterns(self) -> None:
        """Load recognized patterns."""
        patterns_path = self.storage_dir / "patterns.json"
        if patterns_path.exists():
            with open(patterns_path, 'r') as f:
                data = json.load(f)
                self.pattern_cache = {
                    k: Pattern(**v) for k, v in data.items()
                }
    
    def _save_patterns(self) -> None:
        """Save recognized patterns."""
        patterns_path = self.storage_dir / "patterns.json"
        with open(patterns_path, 'w') as f:
            data = {
                k: asdict(v) for k, v in self.pattern_cache.items()
            }
            json.dump(data, f, indent=2)
    
    def _analyze_new_trace(self, trace: DecisionTrace) -> None:
        """Analyze new trace for patterns."""
        # Extract blind spots
        for blind_spot in trace.blind_spots_found:
            pattern_id = f"blind_spot_{hashlib.md5(blind_spot.encode()).hexdigest()[:8]}"
            
            if pattern_id in self.pattern_cache:
                # Existing pattern - increment frequency
                pattern = self.pattern_cache[pattern_id]
                pattern.frequency += 1
                pattern.examples.append(trace.trace_id)
            else:
                # New pattern
                self.pattern_cache[pattern_id] = Pattern(
                    pattern_id=pattern_id,
                    pattern_type='blind_spot',
                    description=blind_spot,
                    frequency=1,
                    effectiveness=trace.quality_score,
                    examples=[trace.trace_id]
                )
        
        self._save_patterns()
    
    def _find_blind_spot_patterns(self) -> list[Pattern]:
        """Find recurring blind spot patterns."""
        return [
            p for p in self.pattern_cache.values()
            if p.pattern_type == 'blind_spot' and p.frequency > 1
        ]
    
    def _find_success_patterns(self) -> list[Pattern]:
        """Find patterns from successful decisions."""
        success_patterns = []
        
        for trace_id in self.trace_index:
            trace = self._load_trace(trace_id)
            if not trace or trace.quality_score < 0.85:
                continue
            
            # High quality - extract what made it successful
            for pattern in trace.patterns_identified:
                pattern_id = f"success_{hashlib.md5(pattern.encode()).hexdigest()[:8]}"
                
                if pattern_id in self.pattern_cache:
                    p = self.pattern_cache[pattern_id]
                    p.frequency += 1
                    p.effectiveness = (p.effectiveness + trace.quality_score) / 2
                else:
                    self.pattern_cache[pattern_id] = Pattern(
                        pattern_id=pattern_id,
                        pattern_type='success_strategy',
                        description=pattern,
                        frequency=1,
                        effectiveness=trace.quality_score,
                        examples=[trace_id]
                    )
                    success_patterns.append(self.pattern_cache[pattern_id])
        
        return success_patterns
    
    def _find_failure_patterns(self) -> list[Pattern]:
        """Find patterns from failed decisions."""
        # Similar to success patterns but for low quality
        return []  # Implementation similar to success patterns
    
    def _find_common_patterns(self, pattern_lists: list[list[str]]) -> list[str]:
        """Find patterns common across multiple traces."""
        from collections import Counter
        
        all_patterns = [p for patterns in pattern_lists for p in patterns]
        counts = Counter(all_patterns)
        
        # Return patterns that appear in multiple traces
        return [p for p, count in counts.items() if count > 1]
