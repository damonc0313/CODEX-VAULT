from pathlib import Path
import sys

from codex_framework.cli import main


def test_cli_runs_and_creates_artifacts(tmp_path: Path, capsys) -> None:
    artifact_dir = tmp_path / "artifacts"
    sys.argv = [
        "codex",
        "--goal",
        "cli-goal",
        "--artifact-dir",
        str(artifact_dir),
    ]
    rc = main()
    captured = capsys.readouterr()
    assert rc == 0
    assert (artifact_dir / "codex_report.txt").exists()
    assert "Result: success=True" in captured.out


def test_cli_with_trace_flag(tmp_path: Path, capsys) -> None:
    artifact_dir = tmp_path / "artifacts"
    trace_file = tmp_path / "trace.jsonl"
    sys.argv = [
        "codex",
        "--goal",
        "cli-goal",
        "--artifact-dir",
        str(artifact_dir),
        "--trace",
        "--trace-file",
        str(trace_file),
    ]
    rc = main()
    capsys.readouterr()
    assert rc == 0
    assert trace_file.exists()
