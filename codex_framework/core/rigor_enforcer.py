"""Code quality and rigor enforcement module."""

from dataclasses import dataclass
from typing import Dict, List, Optional
import ast
import logging


@dataclass
class RigorMetrics:
    """Metrics for code rigor assessment."""
    
    pep8_compliant: bool
    has_type_annotations: bool
    cyclomatic_complexity: int
    function_length: int
    test_coverage: float
    passed: bool


class RigorEnforcer:
    """
    Enforces code quality standards.
    
    Constraints:
    - PEP8 compliance
    - Type annotations required
    - Cyclomatic complexity ≤ 10
    - Function length ≤ 50 lines
    - Test coverage > 80%
    """
    
    def __init__(self) -> None:
        """Initialize rigor enforcer."""
        self.logger = logging.getLogger(__name__)
        self.max_complexity = 10
        self.max_function_length = 50
        self.min_test_coverage = 0.80
        
    def measure_complexity(self, code: str) -> int:
        """
        Measure cyclomatic complexity of code.
        
        Args:
            code: Python code to analyze
            
        Returns:
            Cyclomatic complexity score
        """
        try:
            tree = ast.parse(code)
            complexity = self._calculate_complexity(tree)
            self.logger.info(f"Cyclomatic complexity: {complexity}")
            return complexity
        except SyntaxError:
            self.logger.error("Syntax error in code")
            return 999  # High value to indicate failure
            
    def validate_type_hints(self, code: str) -> bool:
        """
        Validate presence of type annotations.
        
        Args:
            code: Python code to analyze
            
        Returns:
            True if type hints are present, False otherwise
        """
        try:
            tree = ast.parse(code)
            functions = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]
            
            if not functions:
                return True  # No functions to check
                
            annotated = sum(
                1 for func in functions
                if self._has_annotations(func)
            )
            
            has_hints = annotated == len(functions)
            self.logger.info(
                f"Type hints: {annotated}/{len(functions)} functions"
            )
            return has_hints
        except SyntaxError:
            return False
            
    def audit_style_compliance(self, code: str) -> bool:
        """
        Audit PEP8 style compliance.
        
        Args:
            code: Python code to analyze
            
        Returns:
            True if compliant, False otherwise
        """
        # Simplified PEP8 checks
        issues = []
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 79:
                issues.append(f"Line {i}: exceeds 79 characters")
                
            # Check for tabs
            if '\t' in line:
                issues.append(f"Line {i}: contains tabs")
                
        is_compliant = len(issues) == 0
        if not is_compliant:
            self.logger.warning(f"PEP8 issues: {issues[:5]}")
        else:
            self.logger.info("PEP8 compliant")
            
        return is_compliant
        
    def enforce_test_coverage(
        self,
        coverage_data: Optional[Dict[str, float]] = None
    ) -> bool:
        """
        Enforce minimum test coverage requirement.
        
        Args:
            coverage_data: Coverage metrics
            
        Returns:
            True if coverage meets requirement, False otherwise
        """
        if coverage_data is None:
            self.logger.warning("No coverage data provided")
            return False
            
        overall_coverage = coverage_data.get('overall', 0.0)
        meets_requirement = overall_coverage >= self.min_test_coverage
        
        self.logger.info(
            f"Test coverage: {overall_coverage:.1%} "
            f"(required: {self.min_test_coverage:.1%})"
        )
        
        return meets_requirement
        
    def validate_all(
        self,
        code: str,
        coverage_data: Optional[Dict[str, float]] = None
    ) -> RigorMetrics:
        """
        Validate code against all rigor constraints.
        
        Args:
            code: Python code to validate
            coverage_data: Test coverage metrics
            
        Returns:
            Complete rigor metrics
        """
        complexity = self.measure_complexity(code)
        has_types = self.validate_type_hints(code)
        is_pep8 = self.audit_style_compliance(code)
        has_coverage = self.enforce_test_coverage(coverage_data)
        
        # Measure function length
        func_length = self._measure_function_length(code)
        
        passed = all([
            complexity <= self.max_complexity,
            has_types,
            is_pep8,
            func_length <= self.max_function_length,
            has_coverage
        ])
        
        metrics = RigorMetrics(
            pep8_compliant=is_pep8,
            has_type_annotations=has_types,
            cyclomatic_complexity=complexity,
            function_length=func_length,
            test_coverage=coverage_data.get('overall', 0.0)
            if coverage_data else 0.0,
            passed=passed
        )
        
        self.logger.info(f"Rigor validation: {'PASSED' if passed else 'FAILED'}")
        return metrics
        
    def refactor_or_flag(self, metrics: RigorMetrics) -> List[str]:
        """
        Generate refactoring recommendations.
        
        Args:
            metrics: Current rigor metrics
            
        Returns:
            List of refactoring recommendations
        """
        recommendations = []
        
        if not metrics.pep8_compliant:
            recommendations.append("Apply PEP8 formatting")
            
        if not metrics.has_type_annotations:
            recommendations.append("Add type annotations")
            
        if metrics.cyclomatic_complexity > self.max_complexity:
            recommendations.append(
                f"Reduce complexity from {metrics.cyclomatic_complexity} "
                f"to ≤ {self.max_complexity}"
            )
            
        if metrics.function_length > self.max_function_length:
            recommendations.append(
                f"Reduce function length from {metrics.function_length} "
                f"to ≤ {self.max_function_length}"
            )
            
        if metrics.test_coverage < self.min_test_coverage:
            recommendations.append(
                f"Increase test coverage from {metrics.test_coverage:.1%} "
                f"to > {self.min_test_coverage:.1%}"
            )
            
        return recommendations
        
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity from AST."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            # Increment for control flow statements
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
                
        return complexity
        
    def _has_annotations(self, func: ast.FunctionDef) -> bool:
        """Check if function has type annotations."""
        # Check return annotation
        has_return = func.returns is not None
        
        # Check argument annotations (excluding 'self' and 'cls')
        args_to_check = [
            arg for arg in func.args.args
            if arg.arg not in ('self', 'cls')
        ]
        
        # If no args besides self/cls, just check return
        if not args_to_check:
            return has_return
            
        args_annotated = all(
            arg.annotation is not None
            for arg in args_to_check
        )
        
        return has_return and args_annotated
        
    def _measure_function_length(self, code: str) -> int:
        """Measure maximum function length in code."""
        try:
            tree = ast.parse(code)
            functions = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]
            
            if not functions:
                return 0
                
            max_length = max(
                self._get_function_length(func)
                for func in functions
            )
            return max_length
        except SyntaxError:
            return 999
            
    def _get_function_length(self, func: ast.FunctionDef) -> int:
        """Get length of a function in lines."""
        if not func.body:
            return 1
        first_line = func.lineno
        last_line = max(
            node.lineno for node in ast.walk(func)
            if hasattr(node, 'lineno')
        )
        return last_line - first_line + 1
