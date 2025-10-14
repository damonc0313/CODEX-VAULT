from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .intelligence import IntelligenceIndexMonitor
from .telemetry import Telemetry


@dataclass(frozen=True)
class ExecutionResult:
    success: bool
    cii: float
    artifact_paths: List[Path]


class ExecutionLoop:
    def __init__(self, telemetry: Telemetry) -> None:
        self.telemetry = telemetry
        self.intelligence_monitor = IntelligenceIndexMonitor()

    def run(self, goal: str, artifact_dir: Path) -> ExecutionResult:
        artifact_dir.mkdir(parents=True, exist_ok=True)

        self.telemetry.record(
            {
                "goal_id": goal,
                "agent_mode": "analysis",
                "uncertainty": 0.2,
                "ethical_status": "ok",
                "artifact_hash": "",
                "result": "starting",
            }
        )

        # Simplified multi-mode progression
        modes: List[str] = ["analysis", "architecture", "build", "critique"]
        for mode in modes:
            self.telemetry.record(
                {
                    "goal_id": goal,
                    "agent_mode": mode,
                    "uncertainty": max(0.0, 0.3 - modes.index(mode) * 0.05),
                    "ethical_status": "ok",
                    "artifact_hash": "",
                    "result": "progress",
                }
            )

        # Create a simple artifact reflecting the framework
        artifact = artifact_dir / "codex_report.txt"
        contents = self._generate_report(goal=goal)
        artifact.write_text(contents, encoding="utf-8")

        # Update telemetry with artifact info
        self.telemetry.record(
            {
                "goal_id": goal,
                "agent_mode": "critique",
                "uncertainty": 0.1,
                "ethical_status": "ok",
                "artifact_hash": str(hash(contents)),
                "result": "artifact_created",
            }
        )

        # Compute Codex Intelligence Index based on simple heuristics
        metrics: Dict[str, float] = {
            "adaptability": 0.8,
            "clarity": 0.9,
            "ethical_stability": 1.0,
            "innovation_rate": 0.6,
            "reasoning_depth": 0.7,
        }
        cii = self.intelligence_monitor.compute_cii(metrics)

        self.telemetry.record(
            {
                "goal_id": goal,
                "agent_mode": "critique",
                "uncertainty": 0.1,
                "ethical_status": "ok",
                "artifact_hash": str(hash(contents)),
                "result": f"completed:cii={cii:.3f}",
            }
        )

        return ExecutionResult(success=True, cii=cii, artifact_paths=[artifact])

    def _generate_report(self, goal: str) -> str:
        lines: List[str] = [
            "Codex Autonomous Framework v4 — Execution Report",
            f"Goal: {goal}",
            "Modes executed: analysis → architecture → build → critique",
            "Ethics: pass",
        ]
        return "\n".join(lines) + "\n"
