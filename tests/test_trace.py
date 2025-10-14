from pathlib import Path

from codex_framework.execution import ExecutionLoop
from codex_framework.telemetry import Telemetry


def test_trace_logger_creates_jsonl(tmp_path: Path) -> None:
    telemetry = Telemetry()
    loop = ExecutionLoop(telemetry=telemetry)
    result = loop.run(goal="trace-goal", artifact_dir=tmp_path, trace_path=tmp_path / "trace.jsonl")

    trace_file = tmp_path / "trace.jsonl"
    assert trace_file.exists()
    lines = trace_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) > 0
    # Ensure JSON lines structure: each line should contain stage and details
    assert "\"stage\"" in lines[0]
