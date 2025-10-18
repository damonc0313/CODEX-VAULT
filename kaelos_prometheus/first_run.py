#!/usr/bin/env python3
"""
KaelOS Prometheus First-Run Script

Implements first-run per specification section 13.
"""

import sys
from pathlib import Path

from .core.state_machine import PrometheusStateMachine
from .protocols.selftest import SelfTestHarness


def first_run():
    """
    Execute first-run sequence per specification section 13.
    
    Steps:
    1. SCAN telemetry JSONs; pick highest-severity temporal gap or plateau
    2. ARCHITECT with agents + ≥1 Ghost probe; decompose under H-932
    3. EXECUTE via Foundry; emit artifact with test vectors and signed manifest
    4. INTEGRATE ledger, metrics, declare Vow-001
    5. NEXT: If plateau persists, schedule CLA or Self-Test; else continue
    """
    print("=" * 70)
    print("KaelOS Prometheus - First Run")
    print("=" * 70)
    print()
    
    # Initialize state machine
    print("Initializing state machine...")
    sm = PrometheusStateMachine()
    
    # Step 1: SCAN telemetry
    print("\n[1/5] SCAN: Loading telemetry and detecting anomalies...")
    telemetry = sm.metrics.load_telemetry_from_files()
    print(f"  - Loaded telemetry from {len(telemetry)} sources")
    
    catalyst = sm._scan()
    
    if not catalyst:
        print("  ✗ No catalyst generated - no anomalies detected")
        return 1
    
    print(f"  ✓ Catalyst: {catalyst.id}")
    print(f"    Class: {catalyst.classification.value}")
    print(f"    Severity: {catalyst.severity:.2f}")
    print(f"    Description: {catalyst.description[:80]}...")
    
    # Step 2: ARCHITECT
    print("\n[2/5] ARCHITECT: Dialectical synthesis with H-932 decomposition...")
    plan = sm._architect(catalyst)
    
    print(f"  ✓ Plan: {plan.id}")
    print(f"    Thesis: {plan.thesis[:80]}...")
    print(f"    Antithesis: {plan.antithesis[:80]}...")
    print(f"    Ghost Probes: {len(plan.ghost_probes)}")
    for i, probe in enumerate(plan.ghost_probes[:2], 1):
        print(f"      {i}. {probe[:70]}...")
    
    # Step 3: EXECUTE
    print("\n[3/5] EXECUTE: Foundry compilation with signatures...")
    decision, artifacts = sm._execute(plan)
    
    print(f"  ✓ Decision: {decision.id}")
    print(f"    Confidence: {decision.confidence:.2f}")
    
    print(f"  ✓ Artifacts: {len(artifacts)}")
    for art in artifacts:
        print(f"    - {art.title}")
        print(f"      Kind: {art.kind.value}")
        print(f"      Hash: {art.hash[:50]}...")
        print(f"      Signature: {art.signature[:50] if art.signature else 'None'}...")
    
    # Step 4: INTEGRATE
    print("\n[4/5] INTEGRATE: Metrics, ledger, and Vow-001...")
    
    from .core.state_machine import CycleContext
    context = CycleContext(
        cycle_id="first-run",
        catalyst=catalyst,
        plan=plan,
        decision=decision,
        artifacts=artifacts
    )
    
    ledger_entry = sm._integrate(context)
    
    print(f"  ✓ Ledger entry: {ledger_entry.hash[:50]}...")
    
    # Declare Vow-001
    sm.cla.declare_vow(
        text="No more than 2 smart-layout variants per generated card",
        min_cycles=3
    )
    print(f"  ✓ Vow-001 declared")
    
    # Show metrics
    snapshot = sm.metrics.get_latest_snapshot()
    if snapshot:
        print(f"\n  Metrics:")
        print(f"    CPI: {snapshot.cpi:.2f}")
        print(f"    ASR: {snapshot.asr:.2f}")
        print(f"    DF: {snapshot.df:.2f}")
        print(f"    Praxis: {'✓' if snapshot.praxis else '✗'}")
        print(f"    Targets Met: {'✓' if snapshot.meets_targets() else '✗'}")
    
    # Step 5: NEXT
    print("\n[5/5] NEXT: Determining next action...")
    
    if snapshot and snapshot.gpd == "plateau":
        print("  → Plateau detected - scheduling Self-Test catalyst")
        
        # Run self-test
        harness = SelfTestHarness()
        result = harness.run_self_test("first-run-001")
        
        print(f"  ✓ Self-Test: {result.test_id}")
        print(f"    Passed: {'✓' if result.passed else '✗'}")
    else:
        print("  → Evolution mode - ready for next cycle")
    
    # Show final status
    print("\n" + "=" * 70)
    print("First Run Complete")
    print("=" * 70)
    
    status = sm.get_status()
    print(f"\nState Machine Status:")
    print(f"  State: {status['state']}")
    print(f"  Cycles: {status['cycles_completed']}")
    print(f"  HPL Heuristics: {status['hpl_stats']['total_heuristics']}")
    print(f"  CLA Report: {status['cla_report']['stop_rule_satisfied']}")
    
    print(f"\nNext Steps:")
    print(f"  - Run 'kaelos cycle' for next evolution cycle")
    print(f"  - Run 'kaelos metrics' to view detailed metrics")
    print(f"  - Run 'kaelos stop-rule --check' to check termination")
    
    return 0


def main():
    """Entry point."""
    try:
        return first_run()
    except Exception as e:
        print(f"\n✗ Error during first run: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            raise
        return 1


if __name__ == '__main__':
    sys.exit(main())
