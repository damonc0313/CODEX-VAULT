#!/usr/bin/env python3
"""
KaelOS Prometheus CLI

Implements CLI per specification section 12.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional

from ..core.state_machine import PrometheusStateMachine
from ..protocols.cla import ConstraintLiberationAudit, LiberationRequest
from ..protocols.selftest import SelfTestHarness
from ..engines.genesis import GenesisEngine


def cmd_scan(args):
    """Execute SCAN phase."""
    sm = PrometheusStateMachine(args.db)
    
    if args.telemetry:
        print(f"Loading telemetry from {args.telemetry}")
        telemetry = sm.metrics.load_telemetry_from_files()
        print(f"Loaded telemetry: {len(telemetry)} sources")
    
    # Run just SCAN phase
    sm.state = sm.state.SCAN
    catalyst = sm._scan()
    
    if catalyst:
        print(f"\n✓ Catalyst generated: {catalyst.id}")
        print(f"  Class: {catalyst.classification.value}")
        print(f"  Severity: {catalyst.severity:.2f}")
        print(f"  Description: {catalyst.description}")
    else:
        print("\n✗ No catalyst generated (Stop-Risk)")
    
    return 0


def cmd_plan(args):
    """Execute ARCHITECT phase."""
    sm = PrometheusStateMachine(args.db)
    
    # Get catalyst
    catalyst = sm.db.get_catalyst(args.id)
    if not catalyst:
        print(f"✗ Catalyst {args.id} not found")
        return 1
    
    print(f"Architecting plan for catalyst {catalyst.id}...")
    
    # Run ARCHITECT
    plan = sm._architect(catalyst)
    
    print(f"\n✓ Plan generated: {plan.id}")
    print(f"  Thesis: {plan.thesis[:100]}...")
    print(f"  Antithesis: {plan.antithesis[:100]}...")
    print(f"  Ghost Probes: {len(plan.ghost_probes)}")
    
    if args.ghost:
        print("\n  Ghost Probes:")
        for i, probe in enumerate(plan.ghost_probes, 1):
            print(f"    {i}. {probe}")
    
    return 0


def cmd_decompose(args):
    """Check H-932 decomposition."""
    sm = PrometheusStateMachine(args.db)
    
    plan = sm.db.get_plan(args.id)
    if not plan:
        print(f"✗ Plan {args.id} not found")
        return 1
    
    decomp = plan.decomposition
    
    print(f"\n✓ H-932 Decomposition for {plan.id}:")
    print(f"\n  Semantic Layer:")
    print(f"    {json.dumps(decomp.get('semantic', {}), indent=4)}")
    print(f"\n  Structural Layer:")
    print(f"    {json.dumps(decomp.get('structural', {}), indent=4)}")
    print(f"\n  Proof Layer:")
    print(f"    {json.dumps(decomp.get('proof', {}), indent=4)}")
    
    return 0


def cmd_execute(args):
    """Execute EXECUTE phase."""
    sm = PrometheusStateMachine(args.db)
    
    plan = sm.db.get_plan(args.id)
    if not plan:
        print(f"✗ Plan {args.id} not found")
        return 1
    
    print(f"Executing plan {plan.id}...")
    
    if args.time_critical:
        plan.time_critical = True
    
    decision, artifacts = sm._execute(plan)
    
    print(f"\n✓ Decision: {decision.id}")
    print(f"  Choice: {decision.choice}")
    print(f"  Confidence: {decision.confidence:.2f}")
    
    if decision.counterargument and args.counterargument:
        print(f"\n  H-930 Counterargument:")
        print(f"    {decision.counterargument[:200]}...")
    
    print(f"\n✓ Artifacts: {len(artifacts)}")
    for art in artifacts:
        print(f"  - {art.title} ({art.kind.value})")
        print(f"    Hash: {art.hash[:40]}...")
        print(f"    Signature: {art.signature[:40] if art.signature else 'None'}...")
    
    return 0


def cmd_vow(args):
    """Vow operations."""
    cla = ConstraintLiberationAudit()
    
    if args.action == 'declare':
        if not args.text:
            print("✗ --text required for declare")
            return 1
        
        vow = cla.declare_vow(args.text, args.min_cycles or 3)
        print(f"\n✓ Vow declared: {vow.vow_id}")
        print(f"  Text: {vow.text}")
        print(f"  Min cycles: {vow.min_cycles}")
    
    elif args.action == 'liberate':
        if not args.id or not args.justify:
            print("✗ --id and --justify required for liberate")
            return 1
        
        request = LiberationRequest(
            vow_id=args.id,
            diagnostics="User-requested liberation",
            justification=args.justify,
            replacement_vow=args.replace
        )
        
        granted = cla.request_liberation(request)
        
        if granted:
            print(f"\n✓ Liberation granted for {args.id}")
            print(f"  CLR: {cla.get_clr():.2f}")
        else:
            print(f"\n✗ Liberation denied for {args.id}")
    
    elif args.action == 'status':
        report = cla.get_audit_report()
        print(f"\n✓ CLA Status:")
        print(f"  Active Vow: {report['active_vow']}")
        print(f"  Total Vows: {report['total_vows']}")
        print(f"  Liberations: {report['liberation_count']}")
        print(f"  CLR: {report['clr']:.2f}")
        print(f"  Stop Rule Satisfied: {report['stop_rule_satisfied']}")
    
    return 0


def cmd_integrate(args):
    """Execute INTEGRATE phase."""
    sm = PrometheusStateMachine(args.db)
    
    # Get artifact
    artifact = sm.db.get_artifact(args.id)
    if not artifact:
        print(f"✗ Artifact {args.id} not found")
        return 1
    
    print(f"Integrating artifact {artifact.id}...")
    
    # Create minimal context
    from ..core.state_machine import CycleContext
    context = CycleContext(
        cycle_id=f"manual-{args.id[:8]}",
        artifacts=[artifact]
    )
    
    ledger_entry = sm._integrate(context)
    
    print(f"\n✓ Ledger entry: {ledger_entry.hash[:40]}...")
    print(f"  Type: {ledger_entry.entry_type.value}")
    print(f"  Timestamp: {ledger_entry.timestamp.isoformat()}")
    
    return 0


def cmd_metrics(args):
    """Show metrics."""
    sm = PrometheusStateMachine(args.db)
    
    latest = sm.metrics.get_latest_snapshot()
    
    if not latest:
        print("✗ No metrics available")
        return 1
    
    print(f"\n✓ Latest Metrics (as of {latest.timestamp.isoformat()}):")
    print(f"\n  Core Metrics:")
    print(f"    CPI: {latest.cpi:.2f}")
    print(f"    ASR: {latest.asr:.2f}")
    print(f"    DF: {latest.df:.2f}")
    print(f"    Praxis: {'✓' if latest.praxis else '✗'}")
    
    print(f"\n  Telemetry Metrics:")
    print(f"    GRL: {latest.grl:.1f}h")
    print(f"    ABI: {latest.abi:.2f}")
    print(f"    CBI: {latest.cbi}")
    print(f"    GPD: {latest.gpd}")
    print(f"    CLR: {latest.clr:.2f}")
    
    print(f"\n  Scaffolding Metrics:")
    print(f"    SSI: {latest.ssi:.2f}")
    print(f"    SLD: {latest.sld:.1f} days")
    print(f"    CDAR: {latest.cdar:.2f}")
    
    print(f"\n  Genesis & Trace:")
    print(f"    GCR: {latest.gcr:.2f}")
    print(f"    TLS: {latest.tls:.2f}")
    
    print(f"\n  Targets Met: {'✓ YES' if latest.meets_targets() else '✗ NO'}")
    
    return 0


def cmd_stop_rule(args):
    """Check Stop Rule."""
    sm = PrometheusStateMachine(args.db)
    
    ready = sm.metrics.check_stop_rule()
    
    print(f"\n✓ Stop Rule Check:")
    print(f"  Ready: {'✓ YES' if ready else '✗ NO'}")
    
    if ready:
        print(f"\n  All conditions met. Ready to publish evidence pack.")
        
        # Generate evidence pack
        status = sm.get_status()
        print(f"\n  Evidence Pack Preview:")
        print(f"    Cycles: {status['cycles_completed']}")
        print(f"    HPL: {status['hpl_stats']}")
        print(f"    CLA: {status['cla_report']['stop_rule_satisfied']}")
    
    return 0


def cmd_cycle(args):
    """Run complete cycle."""
    sm = PrometheusStateMachine(args.db)
    
    print("Running complete SCAN → ARCHITECT → EXECUTE → INTEGRATE cycle...\n")
    
    context = sm.run_cycle()
    
    print(f"\n✓ Cycle complete: {context.cycle_id}")
    print(f"  Catalyst: {context.catalyst.id if context.catalyst else 'None'}")
    print(f"  Plan: {context.plan.id if context.plan else 'None'}")
    print(f"  Decision: {context.decision.id if context.decision else 'None'}")
    print(f"  Artifacts: {len(context.artifacts)}")
    print(f"  Ledger: {context.ledger_entry.hash[:40] if context.ledger_entry else 'None'}...")
    
    # Show metrics
    latest = sm.metrics.get_latest_snapshot()
    if latest:
        print(f"\n  Metrics: CPI={latest.cpi:.2f} ASR={latest.asr:.2f} DF={latest.df:.2f}")
    
    return 0


def cmd_selftest(args):
    """Run self-test."""
    harness = SelfTestHarness()
    
    print(f"Running self-test {args.id}...\n")
    
    result = harness.run_self_test(args.id)
    
    print(f"\n✓ Self-Test Complete: {result.test_id}")
    print(f"  Catalyst: {result.paradox_catalyst.id}")
    print(f"  Description: {result.paradox_catalyst.description}")
    print(f"  Passed: {'✓' if result.passed else '✗'}")
    
    print(f"\n  Architectural Fingerprints:")
    for key, value in result.architectural_fingerprints.items():
        print(f"    {key}: {value if not isinstance(value, list) else f'{len(value)} items'}")
    
    if args.save:
        # Save prediction and verification script
        pred_path = Path(f"selftest_{args.id}_prediction.txt")
        pred_path.write_text(result.falsifiable_prediction)
        
        verify_path = Path(f"selftest_{args.id}_verify.py")
        verify_path.write_text(result.verification_script)
        
        print(f"\n  Saved:")
        print(f"    Prediction: {pred_path}")
        print(f"    Verification: {verify_path}")
    
    return 0


def cli():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="KaelOS Prometheus - Autonomous Dialectical Evolution System"
    )
    parser.add_argument('--db', default='/mnt/data/mydatabase.db', help='Database path')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # scan
    p_scan = subparsers.add_parser('scan', help='Execute SCAN phase')
    p_scan.add_argument('--telemetry', help='Telemetry JSON file')
    p_scan.set_defaults(func=cmd_scan)
    
    # plan
    p_plan = subparsers.add_parser('plan', help='Execute ARCHITECT phase')
    p_plan.add_argument('--id', required=True, help='Catalyst ID')
    p_plan.add_argument('--ghost', action='store_true', help='Show Ghost probes')
    p_plan.set_defaults(func=cmd_plan)
    
    # decompose
    p_decomp = subparsers.add_parser('decompose', help='Show H-932 decomposition')
    p_decomp.add_argument('--id', required=True, help='Plan ID')
    p_decomp.set_defaults(func=cmd_decompose)
    
    # execute
    p_exec = subparsers.add_parser('execute', help='Execute EXECUTE phase')
    p_exec.add_argument('--id', required=True, help='Plan ID')
    p_exec.add_argument('--time-critical', action='store_true', help='Mark time-critical')
    p_exec.add_argument('--counterargument', action='store_true', help='Show counterargument')
    p_exec.set_defaults(func=cmd_execute)
    
    # vow
    p_vow = subparsers.add_parser('vow', help='Vow operations')
    p_vow.add_argument('action', choices=['declare', 'liberate', 'status'])
    p_vow.add_argument('--id', help='Vow ID')
    p_vow.add_argument('--text', help='Vow text')
    p_vow.add_argument('--min-cycles', type=int, help='Minimum cycles')
    p_vow.add_argument('--justify', help='Liberation justification')
    p_vow.add_argument('--replace', help='Replacement vow text')
    p_vow.set_defaults(func=cmd_vow)
    
    # integrate
    p_int = subparsers.add_parser('integrate', help='Execute INTEGRATE phase')
    p_int.add_argument('--id', required=True, help='Artifact ID')
    p_int.set_defaults(func=cmd_integrate)
    
    # metrics
    p_metrics = subparsers.add_parser('metrics', help='Show metrics')
    p_metrics.set_defaults(func=cmd_metrics)
    
    # stop-rule
    p_stop = subparsers.add_parser('stop-rule', help='Check Stop Rule')
    p_stop.add_argument('--check', action='store_true', help='Check conditions')
    p_stop.set_defaults(func=cmd_stop_rule)
    
    # cycle
    p_cycle = subparsers.add_parser('cycle', help='Run complete cycle')
    p_cycle.set_defaults(func=cmd_cycle)
    
    # selftest
    p_selftest = subparsers.add_parser('selftest', help='Run self-test')
    p_selftest.add_argument('id', help='Test ID')
    p_selftest.add_argument('--save', action='store_true', help='Save artifacts')
    p_selftest.set_defaults(func=cmd_selftest)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            raise
        return 1


if __name__ == '__main__':
    sys.exit(cli())
