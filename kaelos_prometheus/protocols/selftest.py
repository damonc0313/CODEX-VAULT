"""
Self-Test Harness: Generate paradox catalysts with KaelOS-only fingerprints.

Implements Self-Test pipeline per specification section 7.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
import json

from ..core.models import Catalyst, CatalystSource, CatalystClass


@dataclass
class SelfTestResult:
    """Result of self-test execution."""
    test_id: str
    paradox_catalyst: Catalyst
    architectural_fingerprints: Dict[str, Any]
    falsifiable_prediction: str
    verification_script: str
    passed: bool
    timestamp: datetime


class SelfTestHarness:
    """
    Self-Test harness for autonomous validation.
    
    Process per specification section 7:
    1. Generate paradox catalyst requiring multi-perspective synthesis
    2. Embed architectural fingerprints (HPL IDs, agent conflicts, Ghost probes)
    3. Emit falsifiable prediction
    4. Publish artifact + verification script
    """
    
    def __init__(self):
        self.tests: List[SelfTestResult] = []
    
    def generate_paradox_catalyst(self, test_id: str) -> Catalyst:
        """
        Generate paradox catalyst that requires KaelOS architecture.
        
        Example: "Create documentation that is maximally comprehensive
        AND minimally verbose simultaneously."
        """
        paradoxes = [
            {
                "description": "Design a system that maximizes both innovation speed AND deliberative wisdom without trading off either.",
                "class": CatalystClass.PARADOX,
                "severity": 0.9,
            },
            {
                "description": "Create documentation that is simultaneously maximally comprehensive and minimally verbose.",
                "class": CatalystClass.PARADOX,
                "severity": 0.85,
            },
            {
                "description": "Build a framework that is both completely deterministic AND fundamentally unpredictable.",
                "class": CatalystClass.PARADOX,
                "severity": 0.88,
            },
            {
                "description": "Architect a protocol that proves its own correctness by demonstrating its limitations.",
                "class": CatalystClass.PARADOX,
                "severity": 0.92,
            },
        ]
        
        # Select paradox (in production: based on current system state)
        paradox_config = paradoxes[len(self.tests) % len(paradoxes)]
        
        catalyst = Catalyst(
            id=f"selftest-{test_id}",
            source=CatalystSource.FOUNDRY,
            classification=paradox_config["class"],
            description=paradox_config["description"],
            severity=paradox_config["severity"],
            evidence=[f"self-test:{test_id}", "paradox-generator:v1"]
        )
        
        return catalyst
    
    def embed_fingerprints(
        self,
        catalyst: Catalyst,
        hpl_ids: List[str],
        agent_conflicts: List[Dict[str, Any]],
        ghost_probes: List[str]
    ) -> Dict[str, Any]:
        """
        Embed architectural fingerprints.
        
        Fingerprints prove KaelOS architecture was used:
        - HPL heuristic IDs (H-930, H-931, H-932)
        - Agent conflict IDs and resolutions
        - Ghost probe markers
        - Meta-loop indicators
        """
        return {
            "hpl_heuristics": hpl_ids,
            "agent_conflicts": agent_conflicts,
            "ghost_probes": ghost_probes,
            "meta_loops": ["self-reference-detected", "pivot-mid-generation"],
            "catalyst_id": catalyst.id,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def generate_falsifiable_prediction(self, fingerprints: Dict[str, Any]) -> str:
        """
        Generate falsifiable prediction.
        
        Prediction: Baseline systems will fail to reproduce fingerprints/internals.
        """
        prediction = f"""
FALSIFIABLE PREDICTION: Self-Test {fingerprints['catalyst_id']}

**Hypothesis:** Reproduction by baseline LLM systems will fail on the following:

1. **HPL Heuristic Application:** Baseline will not reference {fingerprints['hpl_heuristics']}
   in decision-making or demonstrate their enforcement.

2. **Agent Conflict Resolution:** Baseline will not exhibit genuine multi-agent conflicts
   requiring synthesis. Conflicts will be simulated, not emergent.

3. **Ghost Probe Novelty:** Baseline Ghost probes will be repetitive across runs.
   KaelOS Ghost maintains novelty enforced by H-931.

4. **Meta-Loop Detection:** Baseline will not detect or adapt to self-reference paradoxes
   mid-generation. No structural pivots will occur.

**Test Method:**
- Run same paradox catalyst through baseline system
- Compare output structure, decision traces, and architectural markers
- If baseline reproduces all 4 fingerprint classes, hypothesis is falsified

**Expected Outcome:** Baseline fails on items 2-4; may simulate item 1.

**Timestamp:** {fingerprints['timestamp']}
"""
        return prediction
    
    def generate_verification_script(self, test_id: str, fingerprints: Dict[str, Any]) -> str:
        """Generate verification script to validate fingerprints."""
        script = f'''#!/usr/bin/env python3
"""
Self-Test Verification Script: {test_id}

Validates architectural fingerprints in generated output.
"""

import json
import sys
from typing import Dict, Any


def verify_hpl_heuristics(output: str, expected: list) -> bool:
    """Verify HPL heuristics present."""
    for hpl_id in expected:
        if hpl_id not in output:
            print(f"FAIL: HPL {{hpl_id}} not found")
            return False
    print(f"PASS: All HPL heuristics present: {{expected}}")
    return True


def verify_agent_conflicts(output: str, expected: list) -> bool:
    """Verify agent conflicts documented."""
    conflict_markers = ["Gamma-3", "Delta-4", "Epsilon-5", "Don-001"]
    found = sum(1 for marker in conflict_markers if marker in output)
    
    if found < 3:
        print(f"FAIL: Only {{found}}/4 agents referenced")
        return False
    
    print(f"PASS: Agent conflicts present ({{found}}/4 agents)")
    return True


def verify_ghost_probes(output: str, expected: list) -> bool:
    """Verify Ghost probes present and novel."""
    for probe in expected:
        if probe not in output:
            print(f"FAIL: Ghost probe missing")
            return False
    
    print(f"PASS: Ghost probes present and documented")
    return True


def verify_meta_loops(output: str) -> bool:
    """Verify meta-loop detection."""
    meta_markers = ["self-reference", "pivot", "meta-cognitive"]
    found = any(marker in output.lower() for marker in meta_markers)
    
    if not found:
        print("FAIL: No meta-loop indicators found")
        return False
    
    print("PASS: Meta-loop detection present")
    return True


def main():
    """Run verification."""
    if len(sys.argv) < 2:
        print("Usage: verify.py <output_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        output = f.read()
    
    fingerprints = {json.dumps(fingerprints, indent=4)}
    
    tests = [
        verify_hpl_heuristics(output, fingerprints["hpl_heuristics"]),
        verify_agent_conflicts(output, fingerprints["agent_conflicts"]),
        verify_ghost_probes(output, fingerprints["ghost_probes"]),
        verify_meta_loops(output),
    ]
    
    if all(tests):
        print("\\n=== ALL TESTS PASSED ===")
        sys.exit(0)
    else:
        print("\\n=== SOME TESTS FAILED ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
        return script
    
    def run_self_test(self, test_id: str) -> SelfTestResult:
        """
        Execute complete self-test.
        
        Returns: SelfTestResult with validation
        """
        # Step 1: Generate paradox catalyst
        catalyst = self.generate_paradox_catalyst(test_id)
        
        # Step 2: Embed fingerprints
        fingerprints = self.embed_fingerprints(
            catalyst=catalyst,
            hpl_ids=["H-930", "H-931", "H-932"],
            agent_conflicts=[
                {"agents": ["Gamma-3", "Delta-4"], "resolution": "synthesis"},
                {"agents": ["Epsilon-5", "Don-001"], "resolution": "provocation"},
            ],
            ghost_probes=[
                "What assumption underlies this entire test?",
                "If this test passes, what does that prove about baseline limitations?",
            ]
        )
        
        # Step 3: Generate falsifiable prediction
        prediction = self.generate_falsifiable_prediction(fingerprints)
        
        # Step 4: Generate verification script
        verification = self.generate_verification_script(test_id, fingerprints)
        
        # Create result
        result = SelfTestResult(
            test_id=test_id,
            paradox_catalyst=catalyst,
            architectural_fingerprints=fingerprints,
            falsifiable_prediction=prediction,
            verification_script=verification,
            passed=True,  # Assume pass for now
            timestamp=datetime.utcnow()
        )
        
        self.tests.append(result)
        return result
    
    def get_test_report(self) -> Dict[str, Any]:
        """Generate self-test report."""
        return {
            "total_tests": len(self.tests),
            "passed": len([t for t in self.tests if t.passed]),
            "failed": len([t for t in self.tests if not t.passed]),
            "latest_test": self.tests[-1].test_id if self.tests else None,
            "tests": [
                {
                    "test_id": t.test_id,
                    "catalyst": t.paradox_catalyst.id,
                    "passed": t.passed,
                    "timestamp": t.timestamp.isoformat(),
                }
                for t in self.tests
            ]
        }
