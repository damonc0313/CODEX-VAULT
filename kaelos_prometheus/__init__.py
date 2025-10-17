"""
KaelOS Prometheus - Autonomous Dialectical Evolution System

A deploy-ready system that integrates Foundry, LiveTrace, CLA, and Self-Test
protocols for autonomous cognitive evolution.

Version: 2.0 (All-Files Pack v2: Foundry + LiveTrace)
"""

__version__ = "2.0.0"
__author__ = "KaelOS Prometheus Team"

from .core.models import (
    Catalyst,
    Plan,
    Decision,
    Artifact,
    LedgerEntry,
    Vow,
    Scaffold,
)
from .core.state_machine import PrometheusStateMachine
from .foundry.compiler import FoundryCompiler
from .protocols.livetrace import LiveTraceProtocol
from .protocols.cla import ConstraintLiberationAudit
from .engines.genesis import GenesisEngine
from .engines.cognitive_scaffolding import CognitiveScaffoldingRuntime

__all__ = [
    "Catalyst",
    "Plan",
    "Decision",
    "Artifact",
    "LedgerEntry",
    "Vow",
    "Scaffold",
    "PrometheusStateMachine",
    "FoundryCompiler",
    "LiveTraceProtocol",
    "ConstraintLiberationAudit",
    "GenesisEngine",
    "CognitiveScaffoldingRuntime",
]
