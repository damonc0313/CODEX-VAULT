"""
Custom exceptions for Codex Framework.

Production-grade pattern: Comprehensive exception hierarchy
for precise error handling and debugging.
"""


class CodexError(Exception):
    """Base exception for all Codex Framework errors."""
    
    def __init__(self, message: str, context: dict = None) -> None:
        """
        Initialize Codex error.
        
        Args:
            message: Error message
            context: Additional context for debugging
        """
        self.message = message
        self.context = context or {}
        super().__init__(self.message)
        
    def __str__(self) -> str:
        """String representation with context."""
        base = f"CodexError: {self.message}"
        if self.context:
            base += f" | Context: {self.context}"
        return base


class ValidationError(CodexError):
    """Raised when validation fails."""
    
    pass


class EthicalViolationError(CodexError):
    """Raised when ethical guardrails are violated."""
    
    def __init__(
        self,
        message: str,
        principle_violated: str,
        context: dict = None
    ) -> None:
        """
        Initialize ethical violation error.
        
        Args:
            message: Error message
            principle_violated: Which ethical principle was violated
            context: Additional context
        """
        super().__init__(message, context)
        self.principle_violated = principle_violated


class RigorViolationError(CodexError):
    """Raised when code rigor requirements are not met."""
    
    def __init__(
        self,
        message: str,
        failed_checks: list,
        context: dict = None
    ) -> None:
        """
        Initialize rigor violation error.
        
        Args:
            message: Error message
            failed_checks: List of failed rigor checks
            context: Additional context
        """
        super().__init__(message, context)
        self.failed_checks = failed_checks


class DialecticalResolutionError(CodexError):
    """Raised when dialectical synthesis cannot be achieved."""
    
    pass


class MetacognitiveError(CodexError):
    """Raised when metacognitive processes fail."""
    
    pass


class COTError(CodexError):
    """Raised for Chain of Thought logging errors."""
    
    pass


class IntelligenceIndexError(CodexError):
    """Raised when CII calculation fails."""
    
    pass


class AutonomousExecutionError(CodexError):
    """Raised when autonomous execution encounters issues."""
    
    def __init__(
        self,
        message: str,
        cycle_id: str,
        context: dict = None
    ) -> None:
        """
        Initialize autonomous execution error.
        
        Args:
            message: Error message
            cycle_id: Execution cycle that failed
            context: Additional context
        """
        super().__init__(message, context)
        self.cycle_id = cycle_id
