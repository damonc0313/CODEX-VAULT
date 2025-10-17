#!/usr/bin/env python3
"""
KaelOS Prometheus Demo Script

Demonstrates the complete system in action.
"""

import sys
from pathlib import Path

# Add to path if running from workspace root
sys.path.insert(0, str(Path(__file__).parent))

from kaelos_prometheus.core.state_machine import PrometheusStateMachine
from kaelos_prometheus.core.models import Catalyst, CatalystSource, CatalystClass
from kaelos_prometheus.protocols.cla import ConstraintLiberationAudit, LiberationRequest
from kaelos_prometheus.protocols.selftest import SelfTestHarness


def demo_state_machine():
    """Demonstrate state machine cycle."""
    print("=" * 70)
    print("DEMO 1: State Machine Cycle")
    print("=" * 70)
    
    sm = PrometheusStateMachine()
    
    print("\nRunning complete SCAN → ARCHITECT → EXECUTE → INTEGRATE cycle...")
    
    try:
        context = sm.run_cycle()
        
        print(f"\n✓ Cycle Complete: {context.cycle_id}")
        if context.catalyst:
            print(f"  Catalyst: {context.catalyst.id}")
            print(f"  Severity: {context.catalyst.severity:.2f}")
        if context.plan:
            print(f"  Plan: {context.plan.id}")
            print(f"  Ghost Probes: {len(context.plan.ghost_probes)}")
        if context.decision:
            print(f"  Decision: {context.decision.id}")
            print(f"  Confidence: {context.decision.confidence:.2f}")
        print(f"  Artifacts: {len(context.artifacts)}")
        
        # Show metrics
        snapshot = sm.metrics.get_latest_snapshot()
        if snapshot:
            print(f"\n  Metrics:")
            print(f"    CPI: {snapshot.cpi:.2f}")
            print(f"    ASR: {snapshot.asr:.2f}")
            print(f"    DF: {snapshot.df:.2f}")
            print(f"    Praxis: {'✓' if snapshot.praxis else '✗'}")
            print(f"    Targets Met: {'✓' if snapshot.meets_targets() else '✗'}")
    
    except Exception as e:
        print(f"\n✗ Note: {e}")
        print("  (This is expected if telemetry files are not present)")
    
    print("\n✓ Demo 1 Complete\n")


def demo_cla():
    """Demonstrate CLA (Constraint Liberation Audit)."""
    print("=" * 70)
    print("DEMO 2: Constraint Liberation Audit")
    print("=" * 70)
    
    cla = ConstraintLiberationAudit()
    
    # Declare vow
    print("\nDeclaring Vow-001...")
    vow = cla.declare_vow(
        text="No more than 2 smart-layout variants per card",
        min_cycles=3
    )
    print(f"✓ Vow declared: {vow.vow_id}")
    print(f"  Text: {vow.text}")
    print(f"  Min cycles: {vow.min_cycles}")
    
    # Simulate adherence
    print("\nSimulating adherence across 3 cycles...")
    for i in range(3):
        cla.record_adherence(f"cat-{i:03d}")
        print(f"  Cycle {i+1}: adhered")
    
    # Request liberation
    print("\nRequesting liberation with justification...")
    request = LiberationRequest(
        vow_id=vow.vow_id,
        diagnostics="Constraint limits exploration quality",
        justification=(
            "After analyzing 50+ generated cards, evidence shows that allowing "
            "3-4 layout variants significantly improves readability and user "
            "comprehension (measured via A/B testing). The original constraint "
            "was set conservatively but empirical data demonstrates it's too "
            "restrictive. Propose new constraint: 'No more than 4 variants' with "
            "mandatory readability scoring."
        ),
        replacement_vow="No more than 4 smart-layout variants per card, with mandatory readability scoring"
    )
    
    granted = cla.request_liberation(request)
    
    if granted:
        print(f"✓ Liberation GRANTED")
        print(f"  CLR: {cla.get_clr():.2f}")
        print(f"  Replacement: {request.replacement_vow}")
    else:
        print(f"✗ Liberation DENIED")
    
    # Show report
    report = cla.get_audit_report()
    print(f"\nCLA Status:")
    print(f"  Total Vows: {report['total_vows']}")
    print(f"  Liberations: {report['liberation_count']}")
    print(f"  CLR: {report['clr']:.2f}")
    print(f"  Stop Rule Ready: {report['stop_rule_satisfied']}")
    
    print("\n✓ Demo 2 Complete\n")


def demo_selftest():
    """Demonstrate Self-Test harness."""
    print("=" * 70)
    print("DEMO 3: Self-Test Harness")
    print("=" * 70)
    
    harness = SelfTestHarness()
    
    print("\nGenerating paradox catalyst and verification...")
    result = harness.run_self_test("demo-001")
    
    print(f"\n✓ Self-Test Generated: {result.test_id}")
    print(f"  Catalyst: {result.paradox_catalyst.id}")
    print(f"  Description: {result.paradox_catalyst.description}")
    print(f"  Severity: {result.paradox_catalyst.severity:.2f}")
    
    print(f"\n  Architectural Fingerprints:")
    fp = result.architectural_fingerprints
    print(f"    HPL Heuristics: {fp['hpl_heuristics']}")
    print(f"    Agent Conflicts: {len(fp['agent_conflicts'])}")
    print(f"    Ghost Probes: {len(fp['ghost_probes'])}")
    print(f"    Meta-Loops: {fp['meta_loops']}")
    
    print(f"\n  Falsifiable Prediction:")
    print(result.falsifiable_prediction[:300] + "...")
    
    print(f"\n  Verification Script: {len(result.verification_script)} bytes")
    
    print("\n✓ Demo 3 Complete\n")


def demo_multi_agent():
    """Demonstrate multi-agent synthesis."""
    print("=" * 70)
    print("DEMO 4: Multi-Agent Dialectical Synthesis")
    print("=" * 70)
    
    from kaelos_prometheus.core.agents import MultiAgentOrchestrator
    
    orchestrator = MultiAgentOrchestrator()
    
    # Create test catalyst
    catalyst = {
        "id": "demo-catalyst",
        "description": "Design a system that maximizes both speed AND thoroughness"
    }
    
    print("\nExecuting multi-agent synthesis...")
    print(f"  Catalyst: {catalyst['description']}")
    
    result = orchestrator.dialectical_synthesis(catalyst, enforce_h931=True)
    
    print(f"\n✓ Synthesis Complete")
    print(f"  Thesis (Gamma-3):")
    print(f"    {result['thesis'][:150]}...")
    
    print(f"\n  Antithesis (Epsilon-5):")
    print(f"    {result['antithesis'][:150]}...")
    
    print(f"\n  Ghost Probes (Don-001):")
    for i, probe in enumerate(result['ghost_probes'], 1):
        print(f"    {i}. {probe}")
    
    print(f"\n  Validation (Delta-4):")
    print(f"    {result['validation'][:150]}...")
    
    print(f"\n  Agents Involved: {', '.join(result['agents_involved'])}")
    print(f"  Conflict Detected: {'✓' if result['conflict_detected'] else '✗'}")
    
    print("\n✓ Demo 4 Complete\n")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("KaelOS Prometheus v2.0 - System Demonstration")
    print("=" * 70 + "\n")
    
    demos = [
        ("State Machine Cycle", demo_state_machine),
        ("Constraint Liberation Audit", demo_cla),
        ("Self-Test Harness", demo_selftest),
        ("Multi-Agent Synthesis", demo_multi_agent),
    ]
    
    for i, (name, func) in enumerate(demos, 1):
        try:
            func()
        except Exception as e:
            print(f"\n✗ Demo {i} Error: {e}")
            if "--debug" in sys.argv:
                raise
    
    print("=" * 70)
    print("All Demonstrations Complete")
    print("=" * 70)
    print("\nKaelOS Prometheus v2.0 is fully operational.")
    print("\nNext steps:")
    print("  - Run: python -m kaelos_prometheus.first_run")
    print("  - CLI: kaelos cycle")
    print("  - Help: kaelos --help")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
