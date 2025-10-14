"""Core cognitive modules for Codex Autonomous Framework v4.0."""

from .cognitive_core import CognitiveCore
from .metacognition import MetacognitiveReflector
from .ethical_guardrails import EthicalGuardrails
from .dialectical_engine import DialecticalEngine
from .rigor_enforcer import RigorEnforcer
from .cot_logger import COTLogger, ChainOfThought

__all__ = [
    'CognitiveCore',
    'MetacognitiveReflector',
    'EthicalGuardrails',
    'DialecticalEngine',
    'RigorEnforcer',
    'COTLogger',
    'ChainOfThought',
]
