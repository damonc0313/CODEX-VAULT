"""System-level components and protocols."""

from .innovation_protocol import InnovationProtocol
from .execution_orchestrator import ExecutionOrchestrator
from .adaptive_scaling import AdaptiveScaling

__all__ = [
    'InnovationProtocol',
    'ExecutionOrchestrator',
    'AdaptiveScaling',
]
