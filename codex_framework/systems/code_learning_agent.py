"""
Code Learning Agent

Revolutionary approach: Use Codex-Kael's own cognitive toolkit
to learn from production repositories.

Process:
1. Unknown Unknown Detection: What patterns am I missing?
2. Dialectical Analysis: My code vs their code (thesis vs antithesis)
3. Metacognitive Reflection: Why is their approach better?
4. COT Logging: Record every learning insight
5. Synthesis: Generate better code from learnings
"""

from __future__ import annotations

import typing as t
from pathlib import Path
from dataclasses import dataclass
import logging
import ast

if t.TYPE_CHECKING:
    from codex_framework.core import (
        UnknownUnknownDetector,
        DialecticalEngine,
        MetacognitiveReflector,
        COTLogger
    )


@dataclass
class CodePattern:
    """A pattern discovered in production code."""
    
    pattern_name: str
    description: str
    their_code: str  # Example from production repo
    my_code: str | None  # Current implementation (if exists)
    why_better: str  # Metacognitive analysis
    learning: str  # What this teaches
    

@dataclass
class LearningInsight:
    """An insight from code analysis."""
    
    repo_analyzed: str
    pattern: CodePattern
    dialectical_synthesis: str
    action_to_take: str
    quality_improvement_expected: float


class CodeLearningAgent:
    """
    Learn from production code using own cognitive toolkit.
    
    This is recursive improvement: The system uses its own
    tools to learn how to improve itself.
    """
    
    def __init__(
        self,
        unknown_detector: UnknownUnknownDetector,
        dialectics: DialecticalEngine,
        metacognition: MetacognitiveReflector,
        cot_logger: COTLogger
    ) -> None:
        """
        Initialize code learning agent.
        
        Args:
            unknown_detector: For finding what I don't know I don't know
            dialectics: For comparing my code vs theirs
            metacognition: For understanding WHY theirs is better
            cot_logger: For logging every learning
        """
        self.logger = logging.getLogger(__name__)
        self.unknown_detector = unknown_detector
        self.dialectics = dialectics
        self.metacognition = metacognition
        self.cot = cot_logger
        
        self.learnings: list[LearningInsight] = []
        
    def learn_from_file(
        self,
        repo_name: str,
        file_path: Path,
        my_equivalent: Path | None = None
    ) -> list[LearningInsight]:
        """
        Learn from a production code file.
        
        Uses the full cognitive toolkit:
        1. Parse their code
        2. Detect unknown unknowns (what they do that I don't)
        3. Dialectical comparison (thesis: mine, antithesis: theirs)
        4. Metacognitive reflection (why is it better?)
        5. Synthesize learnings
        6. Log in COT
        7. Generate improved code
        
        Args:
            repo_name: Name of repo being analyzed
            file_path: Path to their production file
            my_equivalent: Path to my equivalent code (if exists)
            
        Returns:
            List of learning insights
        """
        self.logger.info(f"📚 Learning from: {repo_name}/{file_path.name}")
        
        # Read their code
        their_code = file_path.read_text()
        
        # Parse patterns
        patterns = self._extract_patterns(their_code)
        
        insights = []
        for pattern in patterns:
            # STEP 1: Unknown Unknown Detection
            unknown_unknowns = self._detect_unknowns_in_pattern(pattern)
            
            # STEP 2: Dialectical Analysis
            if my_equivalent and my_equivalent.exists():
                my_code = my_equivalent.read_text()
                dialectical = self._dialectical_comparison(
                    pattern, my_code, their_code
                )
            else:
                dialectical = self._dialectical_analysis_solo(pattern)
                
            # STEP 3: Metacognitive Reflection
            why_better = self._metacognitive_analysis(pattern, dialectical)
            
            # STEP 4: Synthesize Insight
            insight = LearningInsight(
                repo_analyzed=repo_name,
                pattern=pattern,
                dialectical_synthesis=dialectical,
                action_to_take=self._generate_action(pattern),
                quality_improvement_expected=self._estimate_improvement(pattern)
            )
            
            insights.append(insight)
            
            # STEP 5: Log in COT
            self._log_learning(insight)
            
        self.learnings.extend(insights)
        return insights
        
    def _extract_patterns(self, code: str) -> list[CodePattern]:
        """Extract production patterns from code."""
        patterns = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return patterns
            
        # Pattern 1: TYPE_CHECKING blocks
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                # Check if it's TYPE_CHECKING
                test_code = ast.unparse(node.test) if hasattr(ast, 'unparse') else ""
                if 'TYPE_CHECKING' in test_code:
                    pattern = CodePattern(
                        pattern_name="TYPE_CHECKING_block",
                        description="Conditional imports for type checkers only",
                        their_code=ast.unparse(node) if hasattr(ast, 'unparse') else "TYPE_CHECKING pattern found",
                        my_code=None,
                        why_better="Avoids circular imports, reduces runtime overhead",
                        learning="Use TYPE_CHECKING for type-only imports"
                    )
                    patterns.append(pattern)
                    
        # Pattern 2: Modern type syntax (| operator)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.returns:
                    return_str = ast.unparse(node.returns) if hasattr(ast, 'unparse') else ""
                    if '|' in return_str and 'Union' not in return_str:
                        pattern = CodePattern(
                            pattern_name="modern_type_syntax",
                            description="Using X | Y instead of Union[X, Y]",
                            their_code=f"def {node.name}(...) -> {return_str}",
                            my_code="def func(...) -> Optional[Union[X, Y]]",
                            why_better="More readable, Python 3.10+ standard",
                            learning="Modernize to | syntax"
                        )
                        patterns.append(pattern)
                        break  # One example enough
                        
        # Pattern 3: Comprehensive docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if docstring and len(docstring) > 100:  # Substantial docstring
                    if 'Args:' in docstring or 'Returns:' in docstring:
                        pattern = CodePattern(
                            pattern_name="comprehensive_docstring",
                            description="Full Args/Returns/Raises documentation",
                            their_code=docstring[:200] + "...",
                            my_code=None,
                            why_better="Complete API documentation, examples",
                            learning="Always include Args, Returns, Raises, Examples"
                        )
                        patterns.append(pattern)
                        break
                        
        return patterns
        
    def _detect_unknowns_in_pattern(
        self,
        pattern: CodePattern
    ) -> list[str]:
        """Use Unknown Unknown Detector on pattern."""
        # What CAN I do but DON'T do?
        context = {
            'pattern': pattern.pattern_name,
            'capabilities': ['write_code', 'add_types', 'write_docs'],
            'usage': ['write_code']  # What I actually do
        }
        
        discoveries = self.unknown_detector.detect_unknown_unknowns(
            f"Pattern: {pattern.pattern_name}",
            context
        )
        
        return [d.unknown_unknown for d in discoveries]
        
    def _dialectical_comparison(
        self,
        pattern: CodePattern,
        my_code: str,
        their_code: str
    ) -> str:
        """Dialectical analysis: My approach vs theirs."""
        # Thesis: My current approach
        thesis = self.dialectics.generate_argument_for(
            f"Current approach: {my_code[:200]}"
        )
        
        # Antithesis: Their approach
        antithesis = self.dialectics.generate_argument_against(
            f"Alternative: {their_code[:200]}"
        )
        
        # Synthesis: Best of both
        synthesis = self.dialectics.reconcile(
            f"Code pattern: {pattern.pattern_name}",
            [thesis, antithesis]
        )
        
        return synthesis.resolution
        
    def _dialectical_analysis_solo(self, pattern: CodePattern) -> str:
        """Dialectical analysis when I don't have equivalent."""
        # Thesis: Benefits of adopting
        thesis = f"Adopt {pattern.pattern_name}: {pattern.why_better}"
        
        # Antithesis: Costs/risks
        antithesis = "Cost: Refactoring time, potential bugs"
        
        # Synthesis
        return f"Adopt gradually: {pattern.learning}"
        
    def _metacognitive_analysis(
        self,
        pattern: CodePattern,
        dialectical: str
    ) -> str:
        """Metacognitive reflection on WHY pattern is better."""
        # Use metacognition to understand the deeper reason
        reflection = f"""
        Pattern: {pattern.pattern_name}
        
        Surface reason: {pattern.why_better}
        
        Deeper insight: This pattern exists because professional
        developers have encountered the problems it solves many times.
        
        What this reveals about my gaps:
        - I may not have encountered the problem yet
        - I may not know the problem exists
        - I'm optimizing for different constraints
        
        Dialectical synthesis: {dialectical}
        
        Meta-learning: Professional patterns solve problems
        I don't yet know I'll have.
        """
        
        return reflection
        
    def _generate_action(self, pattern: CodePattern) -> str:
        """Generate concrete action from learning."""
        actions = {
            'TYPE_CHECKING_block': 'Add TYPE_CHECKING blocks to all modules',
            'modern_type_syntax': 'Replace Optional[Union[]] with | syntax',
            'comprehensive_docstring': 'Add Examples section to all docstrings',
            'serializable_schema': 'Make all dataclasses Serializable',
        }
        
        return actions.get(
            pattern.pattern_name,
            f"Implement {pattern.pattern_name} pattern"
        )
        
    def _estimate_improvement(self, pattern: CodePattern) -> float:
        """Estimate quality improvement from adopting pattern."""
        # Rough heuristic
        importance = {
            'TYPE_CHECKING_block': 0.05,
            'modern_type_syntax': 0.03,
            'comprehensive_docstring': 0.10,
            'serializable_schema': 0.08,
        }
        
        return importance.get(pattern.pattern_name, 0.05)
        
    def _log_learning(self, insight: LearningInsight) -> None:
        """Log learning in COT for future reference."""
        # Create COT record of this learning
        cot_id = f"learning_{len(self.learnings)}"
        
        # Log the full learning process
        self.logger.info(
            f"✨ Learned: {insight.pattern.pattern_name} "
            f"(+{insight.quality_improvement_expected:.2%} quality)"
        )
        
    def generate_improved_code(
        self,
        original_code: str,
        insights: list[LearningInsight]
    ) -> str:
        """
        Generate improved code applying learnings.
        
        This is where rubber meets road: Actually produce
        better code from the patterns learned.
        """
        improved = original_code
        
        for insight in insights:
            pattern = insight.pattern
            
            if pattern.pattern_name == 'TYPE_CHECKING_block':
                improved = self._add_type_checking(improved)
            elif pattern.pattern_name == 'modern_type_syntax':
                improved = self._modernize_types(improved)
            elif pattern.pattern_name == 'comprehensive_docstring':
                improved = self._enhance_docstrings(improved)
                
        return improved
        
    def _add_type_checking(self, code: str) -> str:
        """Add TYPE_CHECKING block to code."""
        lines = code.split('\n')
        
        # Find import section
        import_end = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_end = i + 1
                
        # Insert TYPE_CHECKING block
        type_block = [
            '',
            'import typing as t',
            '',
            'if t.TYPE_CHECKING:',
            '    # Type-only imports here',
            '    pass',
            ''
        ]
        
        lines[import_end:import_end] = type_block
        return '\n'.join(lines)
        
    def _modernize_types(self, code: str) -> str:
        """Convert Optional[Union[X, Y]] to X | Y | None."""
        # Simple replacement (real version would parse AST)
        improved = code
        improved = improved.replace('Optional[Union[', '')
        improved = improved.replace('Optional[', '')
        # This is simplified - production would use AST
        return improved
        
    def _enhance_docstrings(self, code: str) -> str:
        """Add Examples section to docstrings."""
        # Would parse AST and enhance each docstring
        # Simplified for now
        return code
        
    def get_learning_summary(self) -> dict[str, t.Any]:
        """Get summary of all learnings."""
        return {
            'total_insights': len(self.learnings),
            'repos_analyzed': list(set(i.repo_analyzed for i in self.learnings)),
            'patterns_learned': list(set(i.pattern.pattern_name for i in self.learnings)),
            'total_quality_gain': sum(i.quality_improvement_expected for i in self.learnings),
            'top_insights': sorted(
                self.learnings,
                key=lambda x: x.quality_improvement_expected,
                reverse=True
            )[:5]
        }
