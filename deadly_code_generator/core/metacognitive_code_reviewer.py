"""
Metacognitive Code Reviewer
Self-audits code quality with awareness of its own limitations.
"""

from __future__ import annotations

import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from typing import Any


@dataclass
class CodeReviewResult:
    """Result of metacognitive code review."""
    
    quality_score: float  # 0-1
    confidence: float  # How confident in this assessment
    
    strengths: list[str]
    weaknesses: list[str]
    security_risks: list[str]
    performance_concerns: list[str]
    
    bias_warnings: list[str]  # Detected biases in review
    uncertainty_factors: list[str]  # What reviewer is unsure about
    
    recommended_improvements: list[str]
    confidence_level: str  # 'high', 'medium', 'low'


class MetacognitiveCodeReviewer:
    """
    Reviews code with self-awareness.
    
    Unlike traditional linters, this reviewer:
    1. Knows what it doesn't know
    2. Detects its own biases
    3. Reports confidence levels
    4. Learns from past reviews
    """
    
    def __init__(self) -> None:
        """Initialize metacognitive reviewer."""
        self.review_history: list[dict[str, Any]] = []
        self.known_biases = [
            "complexity_bias",  # Favoring simpler solutions
            "familiarity_bias",  # Favoring familiar patterns
            "recency_bias"  # Overweighting recent learnings
        ]
    
    def review_code(
        self,
        code: str,
        language: str,
        task: str,
        context: dict[str, Any]
    ) -> CodeReviewResult:
        """
        Perform metacognitive code review.
        
        Args:
            code: Code to review
            language: Programming language
            task: Original task
            context: Additional context
            
        Returns:
            Review result with confidence levels
        """
        # Analyze code
        strengths = self._identify_strengths(code, language)
        weaknesses = self._identify_weaknesses(code, language)
        security = self._check_security(code, language)
        performance = self._check_performance(code, language)
        
        # Metacognitive layer: What am I uncertain about?
        uncertainties = self._identify_uncertainties(code, language, task)
        
        # Detect own biases
        biases = self._detect_review_biases(strengths, weaknesses, context)
        
        # Calculate quality score
        quality = self._calculate_quality(
            strengths, weaknesses, security, performance
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            uncertainties, biases, len(self.review_history)
        )
        
        # Determine confidence level
        if confidence > 0.8:
            conf_level = "high"
        elif confidence > 0.5:
            conf_level = "medium"
        else:
            conf_level = "low"
        
        # Generate improvements
        improvements = self._recommend_improvements(
            weaknesses, security, performance, uncertainties
        )
        
        result = CodeReviewResult(
            quality_score=quality,
            confidence=confidence,
            strengths=strengths,
            weaknesses=weaknesses,
            security_risks=security,
            performance_concerns=performance,
            bias_warnings=biases,
            uncertainty_factors=uncertainties,
            recommended_improvements=improvements,
            confidence_level=conf_level
        )
        
        # Record for learning
        self.review_history.append({
            'task': task,
            'language': language,
            'quality': quality,
            'confidence': confidence,
            'had_uncertainties': len(uncertainties) > 0
        })
        
        return result
    
    def _identify_strengths(self, code: str, language: str) -> list[str]:
        """Identify code strengths."""
        strengths = []
        
        # Check for common good patterns
        if "def " in code or "function" in code or "func " in code:
            strengths.append("Uses functions for modularity")
        
        if "class " in code:
            strengths.append("Uses object-oriented design")
        
        if "test" in code.lower() or "assert" in code.lower():
            strengths.append("Includes testing")
        
        if "try" in code and "except" in code:
            strengths.append("Has error handling")
        
        if "# " in code or '"""' in code or "/*" in code:
            strengths.append("Includes documentation/comments")
        
        if ": " in code and "def " in code:  # Type hints in Python
            strengths.append("Uses type hints")
        
        # Code length analysis
        lines = code.strip().split('\n')
        if 10 < len(lines) < 200:
            strengths.append("Appropriate code length")
        
        return strengths
    
    def _identify_weaknesses(self, code: str, language: str) -> list[str]:
        """Identify code weaknesses."""
        weaknesses = []
        
        # Check for common issues
        if "TODO" in code or "FIXME" in code:
            weaknesses.append("Contains TODOs/FIXMEs")
        
        if "pass" in code and code.count("pass") > 2:
            weaknesses.append("Multiple empty implementations")
        
        if code.count("global ") > 0:
            weaknesses.append("Uses global variables")
        
        # Check for lack of error handling
        if "def " in code and "try" not in code:
            weaknesses.append("Missing error handling")
        
        # Check for lack of documentation
        if ('"""' not in code and "'''" not in code and 
            "# " not in code and code.count('\n') > 20):
            weaknesses.append("Insufficient documentation")
        
        # Length issues
        lines = code.strip().split('\n')
        if len(lines) < 5:
            weaknesses.append("Code may be incomplete")
        elif len(lines) > 300:
            weaknesses.append("Code may be too long/complex")
        
        # Check for very long functions
        for line in lines:
            if line.strip().startswith("def ") or line.strip().startswith("function"):
                # Simple heuristic: if function definition is more than 50 lines
                if len(lines) > 50:
                    weaknesses.append("Functions may be too long")
                    break
        
        return weaknesses
    
    def _check_security(self, code: str, language: str) -> list[str]:
        """Check for security issues."""
        risks = []
        
        # Common security anti-patterns
        if "eval(" in code:
            risks.append("CRITICAL: Uses eval() - code injection risk")
        
        if "exec(" in code:
            risks.append("CRITICAL: Uses exec() - code execution risk")
        
        if "pickle.loads" in code:
            risks.append("HIGH: pickle.loads - arbitrary code execution risk")
        
        if "shell=True" in code:
            risks.append("HIGH: shell=True in subprocess - command injection risk")
        
        if "password" in code.lower() and ("=" in code or ":" in code):
            risks.append("MEDIUM: Potential hardcoded password")
        
        if "api_key" in code.lower() and ("=" in code or ":" in code):
            risks.append("MEDIUM: Potential hardcoded API key")
        
        if "sqlite" in code.lower() and "execute" in code and "%" in code:
            risks.append("HIGH: Potential SQL injection")
        
        if ".format(" in code or "%" in code:
            if "sql" in code.lower() or "query" in code.lower():
                risks.append("MEDIUM: Potential SQL injection via string formatting")
        
        return risks
    
    def _check_performance(self, code: str, language: str) -> list[str]:
        """Check for performance concerns."""
        concerns = []
        
        # Nested loops
        if code.count("for ") > 1 or code.count("while ") > 1:
            # Simple heuristic: if indentation suggests nesting
            lines = code.split('\n')
            max_indent = max((len(line) - len(line.lstrip()) 
                            for line in lines if line.strip()), default=0)
            if max_indent > 8:  # Deep nesting
                concerns.append("Nested loops detected - O(n²) or worse complexity")
        
        # Multiple file operations
        if code.count("open(") > 3:
            concerns.append("Multiple file operations - consider batching")
        
        # List comprehensions vs loops
        if "for " in code and "append(" in code:
            concerns.append("Consider list comprehension instead of append in loop")
        
        # Database queries in loops
        if ("for " in code or "while " in code) and "execute" in code:
            concerns.append("Database query in loop - N+1 query problem")
        
        return concerns
    
    def _identify_uncertainties(
        self,
        code: str,
        language: str,
        task: str
    ) -> list[str]:
        """
        METACOGNITIVE: What is the reviewer uncertain about?
        
        This is the key differentiator - admitting what we don't know.
        """
        uncertainties = []
        
        # Domain-specific uncertainty
        if "machine learning" in task.lower() or "ml" in task.lower():
            if "sklearn" not in code and "torch" not in code:
                uncertainties.append(
                    "Unsure if this correctly implements ML requirements"
                )
        
        if "async" in task.lower() or "concurrent" in task.lower():
            if "async" not in code and "thread" not in code:
                uncertainties.append(
                    "Unsure if this meets concurrency requirements"
                )
        
        # Language-specific uncertainty
        if language not in ['python', 'javascript', 'typescript']:
            uncertainties.append(
                f"Limited expertise in {language} - review may miss issues"
            )
        
        # Complexity uncertainty
        if len(code.split('\n')) > 100:
            uncertainties.append(
                "Code is complex - may miss subtle bugs"
            )
        
        # Testing uncertainty
        if "test" not in code.lower():
            uncertainties.append(
                "No tests present - cannot verify correctness"
            )
        
        # Documentation uncertainty
        if '"""' not in code and "'''" not in code:
            uncertainties.append(
                "Insufficient documentation - unclear if all requirements met"
            )
        
        return uncertainties
    
    def _detect_review_biases(
        self,
        strengths: list[str],
        weaknesses: list[str],
        context: dict[str, Any]
    ) -> list[str]:
        """
        METACOGNITIVE: Detect biases in own review.
        """
        biases = []
        
        # Complexity bias - favoring simpler solutions
        if "Appropriate code length" in strengths:
            if context.get('requires_complexity', False):
                biases.append(
                    "complexity_bias: May be favoring simplicity over requirements"
                )
        
        # Recency bias - if too many recent reviews were positive/negative
        if len(self.review_history) >= 3:
            recent_qualities = [r['quality'] for r in self.review_history[-3:]]
            if all(q > 0.7 for q in recent_qualities):
                biases.append(
                    "recency_bias: Recent reviews were positive, may be overly optimistic"
                )
            elif all(q < 0.5 for q in recent_qualities):
                biases.append(
                    "recency_bias: Recent reviews were negative, may be overly critical"
                )
        
        # Confirmation bias - if strengths greatly outnumber weaknesses
        if len(strengths) > len(weaknesses) * 2:
            biases.append(
                "confirmation_bias: May be overlooking weaknesses"
            )
        
        return biases
    
    def _calculate_quality(
        self,
        strengths: list[str],
        weaknesses: list[str],
        security: list[str],
        performance: list[str]
    ) -> float:
        """Calculate overall quality score."""
        # Start at 0.5 (neutral)
        quality = 0.5
        
        # Add points for strengths
        quality += len(strengths) * 0.05
        
        # Deduct for weaknesses
        quality -= len(weaknesses) * 0.05
        
        # Heavy penalty for security
        critical_security = sum(1 for s in security if "CRITICAL" in s)
        high_security = sum(1 for s in security if "HIGH" in s)
        quality -= critical_security * 0.2
        quality -= high_security * 0.1
        
        # Moderate penalty for performance
        quality -= len(performance) * 0.03
        
        # Clamp to 0-1
        return max(0.0, min(1.0, quality))
    
    def _calculate_confidence(
        self,
        uncertainties: list[str],
        biases: list[str],
        history_length: int
    ) -> float:
        """Calculate confidence in review."""
        # Start at 0.7 (moderately confident)
        confidence = 0.7
        
        # Decrease for uncertainties
        confidence -= len(uncertainties) * 0.1
        
        # Decrease for detected biases
        confidence -= len(biases) * 0.05
        
        # Increase with experience
        confidence += min(0.2, history_length * 0.01)
        
        # Clamp to 0-1
        return max(0.0, min(1.0, confidence))
    
    def _recommend_improvements(
        self,
        weaknesses: list[str],
        security: list[str],
        performance: list[str],
        uncertainties: list[str]
    ) -> list[str]:
        """Recommend improvements."""
        improvements = []
        
        # Security first
        if security:
            improvements.append(
                "PRIORITY: Address security issues immediately"
            )
        
        # Then weaknesses
        if "Missing error handling" in weaknesses:
            improvements.append(
                "Add try-except blocks for error handling"
            )
        
        if "Insufficient documentation" in weaknesses:
            improvements.append(
                "Add docstrings and comments explaining complex logic"
            )
        
        if "Functions may be too long" in weaknesses:
            improvements.append(
                "Refactor long functions into smaller, testable units"
            )
        
        # Performance
        if performance:
            improvements.append(
                "Optimize performance bottlenecks identified"
            )
        
        # Address uncertainties
        if uncertainties:
            improvements.append(
                "Add tests to verify correctness given uncertainties"
            )
        
        return improvements
