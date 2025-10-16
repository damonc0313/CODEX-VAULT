"""
Unknown Unknown Detector

The meta-tool for discovering what you don't know you don't know.

Revealed by the witness: "The answer is in what you don't know you don't know."

This should be applied to EVERY problem, not just one-time fixes.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging


@dataclass
class UnknownUnknownDiscovery:
    """Discovered unknown unknown."""
    
    problem: str
    assumption_examined: str
    unknown_unknown: str
    evidence: str
    solution_approach: str


class UnknownUnknownDetector:
    """
    Detector for unknown unknowns.
    
    Core method: When stuck on a problem:
    1. List all assumptions you're making
    2. Question each assumption
    3. Look for what you're NOT doing that you CAN do
    4. Deduce the gap
    
    This applies to EVERYTHING:
    - Quality problems
    - Capability limits
    - Design flaws
    - Learning plateaus
    - Any stuck state
    """
    
    def __init__(self) -> None:
        """Initialize unknown unknown detector."""
        self.logger = logging.getLogger(__name__)
        self.discoveries: List[UnknownUnknownDiscovery] = []
        
    def detect_unknown_unknowns(
        self,
        problem: str,
        context: Dict[str, Any]
    ) -> List[UnknownUnknownDiscovery]:
        """
        Detect unknown unknowns in a problem.
        
        Args:
            problem: The problem you're stuck on
            context: Context about attempts and results
            
        Returns:
            List of discovered unknown unknowns
        """
        self.logger.info(f"🔍 Detecting unknown unknowns for: {problem}")
        
        discoveries = []
        
        # Extract assumptions from context
        assumptions = self._extract_assumptions(problem, context)
        
        # Question each assumption
        for assumption in assumptions:
            unknown = self._question_assumption(assumption, context)
            if unknown:
                discoveries.append(unknown)
                self.discoveries.append(unknown)
                
        # Look for capability gaps
        capability_gaps = self._detect_capability_gaps(context)
        discoveries.extend(capability_gaps)
        
        # Pattern: "I always do X, but never Y"
        behavioral_patterns = self._detect_behavioral_patterns(context)
        discoveries.extend(behavioral_patterns)
        
        self.logger.info(f"  Found {len(discoveries)} unknown unknowns")
        
        return discoveries
        
    def _extract_assumptions(
        self,
        problem: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """Extract implicit assumptions."""
        assumptions = []
        
        # Common assumption patterns
        if 'attempts' in context:
            attempts = context['attempts']
            if attempts > 5:
                assumptions.append("The approach is fundamentally sound")
                assumptions.append("More attempts will eventually work")
                
        if 'result' in context:
            result = context['result']
            if result == 'constant':
                assumptions.append("I'm doing everything required")
                assumptions.append("The problem is capability, not process")
                
        # Meta-assumption
        assumptions.append("I know what's required for success")
        assumptions.append("I'm aware of all the constraints")
        
        return assumptions
        
    def _question_assumption(
        self,
        assumption: str,
        context: Dict[str, Any]
    ) -> Optional[UnknownUnknownDiscovery]:
        """Question an assumption to find unknown unknowns."""
        
        # Pattern: "I know what's required"
        if "know what's required" in assumption.lower():
            return UnknownUnknownDiscovery(
                problem=context.get('problem', 'unknown'),
                assumption_examined=assumption,
                unknown_unknown="I may not know ALL requirements",
                evidence="Have I checked the FULL spec?",
                solution_approach="Review complete requirements, not just what I think matters"
            )
            
        # Pattern: "I'm doing everything"
        if "doing everything" in assumption.lower():
            return UnknownUnknownDiscovery(
                problem=context.get('problem', 'unknown'),
                assumption_examined=assumption,
                unknown_unknown="I may have capability I'm not using",
                evidence="What CAN I do that I'm NOT doing?",
                solution_approach="List all capabilities, find ones never used"
            )
            
        return None
        
    def _detect_capability_gaps(
        self,
        context: Dict[str, Any]
    ) -> List[UnknownUnknownDiscovery]:
        """Detect gaps between capability and usage."""
        gaps = []
        
        # Check for unused capabilities
        if 'capabilities' in context and 'usage' in context:
            capabilities = set(context['capabilities'])
            usage = set(context['usage'])
            unused = capabilities - usage
            
            if unused:
                gaps.append(UnknownUnknownDiscovery(
                    problem=context.get('problem', 'unknown'),
                    assumption_examined="I'm using all relevant capabilities",
                    unknown_unknown=f"Not using: {unused}",
                    evidence=f"Can do but don't: {list(unused)}",
                    solution_approach=f"Integrate unused capabilities: {unused}"
                ))
                
        return gaps
        
    def _detect_behavioral_patterns(
        self,
        context: Dict[str, Any]
    ) -> List[UnknownUnknownDiscovery]:
        """Detect 'always do X, never do Y' patterns."""
        patterns = []
        
        # This requires introspection on actual behavior
        # For now, flag common patterns
        
        common_gaps = [
            ("I generate code", "I don't write tests", "Test coverage missing"),
            ("I create functions", "I don't validate inputs", "Input validation missing"),
            ("I build features", "I don't write docs", "Documentation missing"),
            ("I solve problems", "I don't verify solutions", "Verification missing"),
            ("I learn patterns", "I don't apply them", "Application gap")
        ]
        
        for always_do, never_do, gap in common_gaps:
            patterns.append(UnknownUnknownDiscovery(
                problem="General pattern",
                assumption_examined=always_do,
                unknown_unknown=never_do,
                evidence="Behavioral pattern detected",
                solution_approach=f"Always pair '{always_do}' with complement: {gap}"
            ))
            
        return patterns
        
    def apply_discovery(
        self,
        discovery: UnknownUnknownDiscovery
    ) -> Dict[str, Any]:
        """
        Apply a discovery to solve the problem.
        
        Args:
            discovery: The unknown unknown discovered
            
        Returns:
            Application result
        """
        self.logger.info(f"💡 Applying discovery: {discovery.unknown_unknown}")
        
        # This is where the actual fix happens
        # In practice, this would trigger changes to behavior
        
        return {
            'discovery': discovery.unknown_unknown,
            'solution': discovery.solution_approach,
            'status': 'ready_to_apply'
        }
        
    def integrate_into_problem_solving(
        self,
        problem: str,
        initial_attempts: int,
        context: Dict[str, Any]
    ) -> List[str]:
        """
        Integrate unknown unknown detection into problem-solving flow.
        
        Use this WHENEVER stuck or plateaued.
        
        Args:
            problem: The problem
            initial_attempts: How many attempts made
            context: Problem context
            
        Returns:
            List of new approaches to try
        """
        # If stuck (multiple attempts with same result)
        if initial_attempts > 3:
            self.logger.info("🔄 Stuck detected - checking for unknown unknowns")
            
            discoveries = self.detect_unknown_unknowns(problem, {
                **context,
                'attempts': initial_attempts,
                'result': 'constant'
            })
            
            # Generate new approaches from discoveries
            new_approaches = []
            for discovery in discoveries:
                new_approaches.append(discovery.solution_approach)
                
            return new_approaches
            
        return []
        
    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get summary of all discoveries."""
        return {
            'total_discoveries': len(self.discoveries),
            'unique_unknowns': list(set(
                d.unknown_unknown for d in self.discoveries
            )),
            'solution_approaches': list(set(
                d.solution_approach for d in self.discoveries
            ))
        }
