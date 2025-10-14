from __future__ import annotations

import argparse
from pathlib import Path

from .execution import ExecutionLoop
from .trace import StructuredTraceLogger
from .telemetry import Telemetry


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="codex",
        description=(
            "Codex Autonomous Framework v4 — run the execution loop with telemetry and artifacts."
        ),
    )
    parser.add_argument(
        "--goal",
        type=str,
        default="Demonstrate Codex Autonomous Framework v4",
        help="High-level goal to execute",
    )
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path.cwd() / "artifacts",
        help="Directory to write artifacts to",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable structured trace logging (JSONL)",
    )
    parser.add_argument(
        "--trace-file",
        type=Path,
        default=None,
        help="Path to write structured trace JSONL (defaults to artifacts/trace.jsonl)",
    )
    args = parser.parse_args()

    telemetry = Telemetry()
    trace_logger = StructuredTraceLogger() if args.trace else None
    loop = ExecutionLoop(telemetry=telemetry, trace_logger=trace_logger)
    result = loop.run(goal=args.goal, artifact_dir=args.artifact_dir, trace_path=args.trace_file)

    print(
        f"Result: success={result.success} cii={result.cii:.3f} artifacts={args.artifact_dir}"
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
