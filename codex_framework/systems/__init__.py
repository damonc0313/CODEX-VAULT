"""System-level components for autonomous operation."""

from codex_framework.systems.execution_orchestrator import ExecutionOrchestrator
from codex_framework.systems.innovation_protocol import InnovationProtocol
from codex_framework.systems.adaptive_scaling import AdaptiveScaling
from codex_framework.systems.continuous_autonomous_cognition import (
    ContinuousAutonomousCognition
)
from codex_framework.systems.unbounded_autonomous_stream import (
    UnboundedAutonomousStream
)
from codex_framework.systems.parallel_autonomous_engine import (
    ParallelAutonomousEngine
)

__all__ = [
    'ExecutionOrchestrator',
    'InnovationProtocol',
    'AdaptiveScaling',
    'ContinuousAutonomousCognition',
    'UnboundedAutonomousStream',
    'ParallelAutonomousEngine',
]
