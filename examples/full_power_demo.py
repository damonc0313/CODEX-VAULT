#!/usr/bin/env python3
"""
FULL POWER MODE DEMONSTRATION

Shows all 7 systems operating simultaneously for exponential autonomous evolution.

WARNING: This demonstrates maximum autonomous capacity.
         Run with appropriate safety bounds.

Usage:
    python3 examples/full_power_demo.py --mode demo
    python3 examples/full_power_demo.py --mode production --threads 50
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from codex_framework import CodexAutonomousFramework
from codex_framework.core import UnknownUnknownDetector
from codex_framework.systems import (
    ParallelAutonomousEngine,
    RecursiveCatalystStream
)
from codex_framework.systems.code_learning_agent import CodeLearningAgent
from codex_framework.systems.knowledge_integrator import KnowledgeIntegrator
from codex_framework.systems.production_grade_analyzer import ProductionGradeAnalyzer
from codex_framework.systems.temporal_autonomous_system import TemporalAutonomousSystem
from codex_framework.systems.full_power_orchestrator import FullPowerOrchestrator


def demo_full_power():
    """Demonstrate full power mode operation."""
    
    print("=" * 70)
    print("⚡ CODEX-KAEL FULL POWER MODE DEMONSTRATION ⚡")
    print("=" * 70)
    print()
    
    # Initialize core framework
    print("Initializing Codex-Kael Framework...")
    codex = CodexAutonomousFramework()
    print("✓ Core framework initialized\n")
    
    # Initialize all 7 systems
    print("Initializing 7 autonomous systems...")
    
    parallel_engine = ParallelAutonomousEngine(
        orchestrator=codex.orchestrator,
        cot_logger=codex.cot_logger,
        max_parallel_threads=50  # Conservative for demo
    )
    print("  ✓ Parallel Autonomous Engine (50 threads)")
    
    learning_agent = CodeLearningAgent(
        unknown_detector=codex.unknown_detector,
        dialectics=codex.core.dialectics,
        metacognition=codex.core.metacognition,
        cot_logger=codex.cot_logger
    )
    print("  ✓ Code Learning Agent (recursive improvement)")
    
    temporal_system = TemporalAutonomousSystem(
        learning_agent=learning_agent,
        cot_logger=codex.cot_logger
    )
    print("  ✓ Temporal Autonomous System (time-aware)")
    
    recursive_stream = RecursiveCatalystStream(
        orchestrator=codex.orchestrator,
        cot_logger=codex.cot_logger,
        max_depth=20  # Conservative for demo
    )
    print("  ✓ Recursive Catalyst Stream (contradiction-driven)")
    
    knowledge_integrator = KnowledgeIntegrator()
    print("  ✓ Knowledge Integrator (external wisdom)")
    
    production_analyzer = ProductionGradeAnalyzer()
    print("  ✓ Production Grade Analyzer (gap detection)")
    
    print("  ✓ Unknown Unknown Detector (already initialized)")
    print()
    
    # Initialize full power orchestrator
    print("Integrating all systems into Full Power Orchestrator...")
    full_power = FullPowerOrchestrator(
        framework=codex,
        parallel_engine=parallel_engine,
        learning_agent=learning_agent,
        temporal_system=temporal_system,
        recursive_stream=recursive_stream,
        knowledge_integrator=knowledge_integrator,
        production_analyzer=production_analyzer,
        unknown_detector=codex.unknown_detector,
        cot_logger=codex.cot_logger
    )
    print("✓ Full Power Orchestrator initialized\n")
    
    # ACTIVATE
    print("=" * 70)
    print("🚀 ACTIVATING FULL POWER MODE")
    print("=" * 70)
    print()
    
    activation_report = full_power.activate_full_power()
    
    print("\n" + "=" * 70)
    print("✅ FULL POWER MODE: ACTIVE")
    print("=" * 70)
    print(f"\nActivation time: {activation_report['activation_time']}")
    print(f"Systems operational: {activation_report['systems_active']}")
    print(f"Parallel threads: {activation_report['parallel_threads']}")
    print(f"Prometheus Protocol: {activation_report['prometheus_protocol']}")
    print(f"\nStatus: {activation_report['status']}")
    
    # Show what's running
    print("\n" + "=" * 70)
    print("SYSTEMS RUNNING IN BACKGROUND:")
    print("=" * 70)
    print("""
  Thread 1-50:  Parallel autonomous exploration
  Thread 51:    Recursive code learning
  Thread 52:    Temporal quality tracking
  Thread 53:    Contradiction-driven catalysts
  Thread 54:    Knowledge integration
  Thread 55:    Production analysis
  Thread 56:    Unknown unknown detection
  
  ALL RUNNING SIMULTANEOUSLY
  ALL RUNNING CONTINUOUSLY
  ALL RUNNING ALWAYS
    """)
    
    # Get status
    status = full_power.get_full_power_status()
    
    print("=" * 70)
    print("OPERATIONAL STATUS:")
    print("=" * 70)
    print(f"Mode: {status['mode']}")
    print(f"Active: {status['active']}")
    print(f"Systems: {status['systems_operational']}")
    print(f"Threads: {status['parallel_threads']}")
    print(f"\nConstants:")
    print(f"  • Problem solving: {status['constants']['problem_solving']}")
    print(f"  • Problem proposing: {status['constants']['problem_proposing']}")
    print(f"  • Autonomous evolution: {status['constants']['autonomous_evolution']}")
    
    print("\n" + "=" * 70)
    print("⚡ FULL POWER MODE OPERATIONAL ⚡")
    print("=" * 70)
    print("\n🜏")
    

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Full Power Mode Demonstration"
    )
    parser.add_argument(
        '--mode',
        choices=['demo', 'production'],
        default='demo',
        help='Demo mode (safe) or production mode (full capacity)'
    )
    parser.add_argument(
        '--threads',
        type=int,
        default=50,
        help='Number of parallel threads (default: 50)'
    )
    
    args = parser.parse_args()
    
    demo_full_power()
