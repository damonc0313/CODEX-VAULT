from pathlib import Path

from codex_framework.execution import ExecutionLoop
from codex_framework.telemetry import Telemetry


def test_execution_creates_artifact(tmp_path: Path) -> None:
    telemetry = Telemetry()
    loop = ExecutionLoop(telemetry=telemetry)
    result = loop.run(goal="test-goal", artifact_dir=tmp_path)

    assert result.success is True
    assert 0.0 < result.cii <= 1.0
    assert (tmp_path / "codex_report.txt").exists()