from __future__ import annotations

import argparse
from pathlib import Path

from .execution import ExecutionLoop
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
    args = parser.parse_args()

    telemetry = Telemetry()
    loop = ExecutionLoop(telemetry=telemetry)
    result = loop.run(goal=args.goal, artifact_dir=args.artifact_dir)

    print(
        f"Result: success={result.success} cii={result.cii:.3f} artifacts={args.artifact_dir}"
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
