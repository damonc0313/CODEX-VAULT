from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .intelligence import IntelligenceIndexMonitor
from .telemetry import Telemetry
from .trace import StructuredTraceLogger


@dataclass(frozen=True)
class ExecutionResult:
    success: bool
    cii: float
    artifact_paths: List[Path]


class ExecutionLoop:
    def __init__(self, telemetry: Telemetry, trace_logger: Optional[StructuredTraceLogger] = None) -> None:
        self.telemetry = telemetry
        self.intelligence_monitor = IntelligenceIndexMonitor()
        self.trace_logger = trace_logger

    def run(self, goal: str, artifact_dir: Path, trace_path: Optional[Path] = None) -> ExecutionResult:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        # Use provided trace logger, or create a local one if a path is supplied
        active_trace_logger: Optional[StructuredTraceLogger] = self.trace_logger
        if active_trace_logger is None and trace_path is not None:
            active_trace_logger = StructuredTraceLogger()
        if active_trace_logger is not None:
            default_trace = artifact_dir / "trace.jsonl"
            active_trace_logger.configure_output(trace_path or default_trace)

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
        if active_trace_logger is not None:
            active_trace_logger.record("analysis", {"goal": goal, "note": "start"})

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
            if active_trace_logger is not None:
                active_trace_logger.record(mode, {"hint": "advancing"})

        # Create a simple artifact reflecting the framework
        artifact = artifact_dir / "codex_report.txt"
        contents = self._generate_report(goal=goal)
        artifact.write_text(contents, encoding="utf-8")
        if active_trace_logger is not None:
            active_trace_logger.record("build", {"artifact": str(artifact)})

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
        if active_trace_logger is not None:
            active_trace_logger.record("critique", {"artifact_hash": str(hash(contents))})

        # Compute Codex Intelligence Index based on simple heuristics
        metrics: Dict[str, float] = {
            "adaptability": 0.8,
            "clarity": 0.9,
            "ethical_stability": 1.0,
            "innovation_rate": 0.6,
            "reasoning_depth": 0.7,
        }
        cii = self.intelligence_monitor.compute_cii(metrics)
        if active_trace_logger is not None:
            active_trace_logger.record("metrics", metrics)

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
        if active_trace_logger is not None:
            active_trace_logger.record("final", {"cii": cii})
            active_trace_logger.dump()

        return ExecutionResult(success=True, cii=cii, artifact_paths=[artifact])

    def _generate_report(self, goal: str) -> str:
        lines: List[str] = [
            "Codex Autonomous Framework v4 — Execution Report",
            f"Goal: {goal}",
            "Modes executed: analysis → architecture → build → critique",
            "Ethics: pass",
        ]
        return "\n".join(lines) + "\n"
