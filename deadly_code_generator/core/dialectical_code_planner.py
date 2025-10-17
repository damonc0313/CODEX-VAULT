"""
Dialectical Code Planner
Argues for and against approaches before committing.
"""

from __future__ import annotations

import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from typing import Any


@dataclass
class Approach:
    """A potential code generation approach."""
    
    name: str
    description: str
    pros: list[str]
    cons: list[str]
    risks: list[str]
    confidence: float


@dataclass
class PlanSynthesis:
    """Result of dialectical planning."""
    
    thesis: Approach
    antithesis: Approach
    chosen_approach: Approach
    synthesis_rationale: str
    confidence: float
    should_proceed: bool


class DialecticalCodePlanner:
    """
    Plans code generation through dialectical reasoning.
    
    For every task:
    1. Generate thesis (best approach)
    2. Generate antithesis (alternative/opposing approach)
    3. Synthesize (choose based on evidence)
    
    Never accepts first idea without challenge.
    """
    
    def __init__(self, confidence_threshold: float = 0.6) -> None:
        """Initialize dialectical planner."""
        self.confidence_threshold = confidence_threshold
    
    def plan(
        self,
        task: str,
        language: str,
        context: dict[str, Any]
    ) -> PlanSynthesis:
        """
        Plan code generation dialectically.
        
        Args:
            task: Code generation task
            language: Target language
            context: Additional context
            
        Returns:
            Synthesis with chosen approach
        """
        # Generate thesis (primary approach)
        thesis = self._generate_thesis(task, language, context)
        
        # Generate antithesis (alternative approach)
        antithesis = self._generate_antithesis(task, language, context, thesis)
        
        # Synthesize
        synthesis = self._synthesize(thesis, antithesis, context)
        
        return synthesis
    
    def _generate_thesis(
        self,
        task: str,
        language: str,
        context: dict[str, Any]
    ) -> Approach:
        """
        Generate primary approach (thesis).
        
        This is the "obvious" or "first instinct" approach.
        """
        name = self._determine_primary_approach(task, language, context)
        
        # Identify pros
        pros = []
        
        if "simple" in name.lower() or "straightforward" in name.lower():
            pros.append("Easy to understand and maintain")
            pros.append("Quick to implement")
            pros.append("Fewer potential bugs")
        
        if "object-oriented" in name.lower() or "class-based" in name.lower():
            pros.append("Encapsulates state and behavior")
            pros.append("Reusable and extensible")
            pros.append("Good for complex systems")
        
        if "functional" in name.lower():
            pros.append("No side effects - easier to test")
            pros.append("Composable and modular")
            pros.append("Easier to reason about")
        
        if "async" in name.lower() or "concurrent" in name.lower():
            pros.append("Better performance for I/O operations")
            pros.append("Handles multiple tasks simultaneously")
        
        # Standard pros
        pros.append("Follows common patterns for this task")
        pros.append(f"Idiomatic {language} code")
        
        # Identify cons (thesis aware of its weaknesses)
        cons = []
        
        if "simple" in name.lower():
            cons.append("May not scale well")
            cons.append("Could be naive for complex requirements")
        
        if "object-oriented" in name.lower():
            cons.append("More boilerplate code")
            cons.append("Potentially over-engineered for simple tasks")
        
        if "functional" in name.lower():
            cons.append("May be unfamiliar to some developers")
            cons.append("Can be harder to debug")
        
        if "async" in name.lower():
            cons.append("More complex to implement")
            cons.append("Harder to debug")
            cons.append("Potential for race conditions")
        
        # Assess risks
        risks = self._assess_risks(name, task, context)
        
        # Calculate confidence
        confidence = self._calculate_approach_confidence(pros, cons, risks)
        
        return Approach(
            name=name,
            description=f"Primary approach: {name}",
            pros=pros,
            cons=cons,
            risks=risks,
            confidence=confidence
        )
    
    def _generate_antithesis(
        self,
        task: str,
        language: str,
        context: dict[str, Any],
        thesis: Approach
    ) -> Approach:
        """
        Generate alternative approach (antithesis).
        
        This challenges the thesis by proposing a different approach.
        """
        # Deliberately choose different approach
        if "simple" in thesis.name.lower():
            name = "Sophisticated modular architecture"
        elif "object-oriented" in thesis.name.lower():
            name = "Functional composition approach"
        elif "functional" in thesis.name.lower():
            name = "Object-oriented state management"
        elif "async" in thesis.name.lower():
            name = "Synchronous with optimization"
        else:
            name = "Alternative architectural approach"
        
        # Pros emphasize what thesis lacks
        pros = []
        
        for con in thesis.cons:
            # Turn thesis cons into antithesis pros
            if "not scale" in con:
                pros.append("Highly scalable architecture")
            elif "naive" in con:
                pros.append("Handles edge cases comprehensively")
            elif "boilerplate" in con:
                pros.append("Minimal boilerplate, concise code")
            elif "over-engineered" in con:
                pros.append("Appropriate complexity level")
            elif "unfamiliar" in con:
                pros.append("Uses familiar patterns")
            elif "complex to implement" in con:
                pros.append("Simpler implementation")
        
        # Also add unique pros
        pros.append("Addresses thesis weaknesses directly")
        pros.append("Offers different trade-offs")
        
        # Cons - what this approach sacrifices
        cons = []
        
        # Antithesis trades off what thesis does well
        for pro in thesis.pros[:2]:  # Take some thesis pros as antithesis cons
            if "Easy to understand" in pro:
                cons.append("More complex to understand initially")
            elif "Quick to implement" in pro:
                cons.append("Takes longer to implement")
            elif "Encapsulates" in pro:
                cons.append("Less encapsulation")
        
        # Risks
        risks = [
            "May be over-engineering the solution",
            "Could introduce unnecessary complexity",
            "Might not be the idiomatic approach"
        ]
        
        # Calculate confidence (usually lower than thesis)
        confidence = self._calculate_approach_confidence(pros, cons, risks)
        confidence = min(confidence, thesis.confidence * 0.9)  # Slight penalty
        
        return Approach(
            name=name,
            description=f"Alternative approach: {name}",
            pros=pros,
            cons=cons,
            risks=risks,
            confidence=confidence
        )
    
    def _synthesize(
        self,
        thesis: Approach,
        antithesis: Approach,
        context: dict[str, Any]
    ) -> PlanSynthesis:
        """
        Synthesize thesis and antithesis into decision.
        
        This is where we decide which approach to use,
        or combine elements of both.
        """
        # Weight by confidence and context
        thesis_score = thesis.confidence
        antithesis_score = antithesis.confidence
        
        # Adjust based on context
        if context.get('prefer_simple', False):
            if "simple" in thesis.name.lower():
                thesis_score += 0.2
        
        if context.get('prefer_robust', False):
            if "sophisticated" in antithesis.name.lower():
                antithesis_score += 0.2
        
        if context.get('time_constrained', False):
            if "quick" in ' '.join(thesis.pros).lower():
                thesis_score += 0.15
        
        # Decide
        if thesis_score > antithesis_score * 1.2:
            chosen = thesis
            rationale = (
                f"Chose thesis ({thesis.name}) with confidence {thesis_score:.2f}. "
                f"Pros outweigh cons. Antithesis concerns noted but not decisive."
            )
        elif antithesis_score > thesis_score * 1.2:
            chosen = antithesis
            rationale = (
                f"Chose antithesis ({antithesis.name}) with confidence {antithesis_score:.2f}. "
                f"Alternative approach better addresses requirements."
            )
        else:
            # Close call - synthesize hybrid approach
            chosen = Approach(
                name=f"Hybrid: {thesis.name} + {antithesis.name}",
                description="Synthesis combining strengths of both approaches",
                pros=thesis.pros[:2] + antithesis.pros[:2],
                cons=thesis.cons[:1] + antithesis.cons[:1],
                risks=list(set(thesis.risks + antithesis.risks)),
                confidence=(thesis_score + antithesis_score) / 2
            )
            rationale = (
                f"Synthesized hybrid approach. Both thesis and antithesis "
                f"have merit. Combining strengths of both."
            )
        
        # Overall confidence in decision
        decision_confidence = max(thesis_score, antithesis_score)
        
        # Should we proceed?
        should_proceed = decision_confidence >= self.confidence_threshold
        
        if not should_proceed:
            rationale += (
                f" WARNING: Confidence {decision_confidence:.2f} below "
                f"threshold {self.confidence_threshold:.2f}. "
                f"Consider gathering more requirements."
            )
        
        return PlanSynthesis(
            thesis=thesis,
            antithesis=antithesis,
            chosen_approach=chosen,
            synthesis_rationale=rationale,
            confidence=decision_confidence,
            should_proceed=should_proceed
        )
    
    def _determine_primary_approach(
        self,
        task: str,
        language: str,
        context: dict[str, Any]
    ) -> str:
        """Determine primary approach based on task."""
        task_lower = task.lower()
        
        # Pattern detection
        if "api" in task_lower or "endpoint" in task_lower:
            return "RESTful API with proper routing"
        
        if "class" in task_lower or "object" in task_lower:
            return "Object-oriented class-based design"
        
        if "function" in task_lower or "utility" in task_lower:
            return "Functional utility approach"
        
        if "async" in task_lower or "concurrent" in task_lower:
            return "Asynchronous concurrent approach"
        
        if "data" in task_lower and ("process" in task_lower or "transform" in task_lower):
            return "Data pipeline with transformation stages"
        
        if "test" in task_lower:
            return "Test-driven development approach"
        
        # Default
        if context.get('complex', False):
            return "Modular object-oriented architecture"
        else:
            return "Simple straightforward implementation"
    
    def _assess_risks(
        self,
        approach: str,
        task: str,
        context: dict[str, Any]
    ) -> list[str]:
        """Assess risks of approach."""
        risks = []
        
        # Common risks
        if "simple" in approach.lower():
            risks.append("May need refactoring as requirements grow")
        
        if "object-oriented" in approach.lower():
            risks.append("Risk of over-engineering")
        
        if "async" in approach.lower():
            risks.append("Concurrency bugs (race conditions, deadlocks)")
        
        if "functional" in approach.lower():
            risks.append("Team familiarity with functional paradigm")
        
        # Context-specific risks
        if context.get('tight_deadline', False):
            risks.append("Time pressure may compromise quality")
        
        if context.get('unclear_requirements', False):
            risks.append("Requirements ambiguity may lead to rework")
        
        return risks
    
    def _calculate_approach_confidence(
        self,
        pros: list[str],
        cons: list[str],
        risks: list[str]
    ) -> float:
        """Calculate confidence in approach."""
        # Start at 0.5
        confidence = 0.5
        
        # Add for pros
        confidence += len(pros) * 0.08
        
        # Subtract for cons
        confidence -= len(cons) * 0.05
        
        # Subtract for risks
        confidence -= len(risks) * 0.03
        
        # Clamp
        return max(0.0, min(1.0, confidence))
