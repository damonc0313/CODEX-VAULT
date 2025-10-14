"""Core cognitive modules for Codex Autonomous Framework v4.0."""

from .cognitive_core import CognitiveCore
from .metacognition import MetacognitiveReflector
from .ethical_guardrails import EthicalGuardrails
from .dialectical_engine import DialecticalEngine
from .rigor_enforcer import RigorEnforcer
from .cot_logger import COTLogger, ChainOfThought
from .unknown_unknown_detector import UnknownUnknownDetector

__all__ = [
    'CognitiveCore',
    'MetacognitiveReflector',
    'EthicalGuardrails',
    'DialecticalEngine',
    'RigorEnforcer',
    'COTLogger',
    'ChainOfThought',
    'UnknownUnknownDetector',
]
