import importlib
import json
from typing import Callable, Optional

import pytest

gil_status = importlib.import_module("codex_framework.utils.gil_status")


@pytest.fixture(autouse=True)
def restore_sys(monkeypatch: pytest.MonkeyPatch):
    # Ensure mutations to sys._is_gil_enabled do not leak between tests.
    original = getattr(gil_status.sys, "_is_gil_enabled", None)
    yield
    if original is None:
        monkeypatch.delattr(gil_status.sys, "_is_gil_enabled", raising=False)
    else:
        monkeypatch.setattr(gil_status.sys, "_is_gil_enabled", original, raising=False)


@pytest.fixture(autouse=True)
def restore_sysconfig(monkeypatch: pytest.MonkeyPatch):
    original = gil_status.sysconfig.get_config_var
    yield
    monkeypatch.setattr(gil_status.sysconfig, "get_config_var", original, raising=False)


@pytest.fixture(autouse=True)
def restore_abiflags(monkeypatch: pytest.MonkeyPatch):
    original = getattr(gil_status.sys, "abiflags", "")
    yield
    monkeypatch.setattr(gil_status.sys, "abiflags", original, raising=False)


def _set_probe(monkeypatch: pytest.MonkeyPatch, value: Optional[bool | Callable[[], bool]]):
    if value is None:
        monkeypatch.delattr(gil_status.sys, "_is_gil_enabled", raising=False)
    else:
        if isinstance(value, bool):
            monkeypatch.setattr(gil_status.sys, "_is_gil_enabled", lambda: value, raising=False)
        else:
            monkeypatch.setattr(gil_status.sys, "_is_gil_enabled", value, raising=False)


def test_probe_handles_missing_api(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    status = gil_status.probe()
    assert status.gil_enabled is None
    assert status.api_available is False
    assert "upgrade" in status.explanation


def test_probe_infers_from_sysconfig(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    monkeypatch.setattr(
        gil_status.sysconfig,
        "get_config_var",
        lambda name: 1 if name == "Py_GIL_DISABLED" else None,
        raising=False,
    )
    status = gil_status.probe()
    assert status.gil_enabled is False
    assert "Py_GIL_DISABLED" in status.explanation
    assert status.api_available is False


def test_probe_infers_gil_enabled_from_sysconfig(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    monkeypatch.setattr(
        gil_status.sysconfig,
        "get_config_var",
        lambda name: 0 if name == "Py_GIL_DISABLED" else None,
        raising=False,
    )
    status = gil_status.probe()
    assert status.gil_enabled is True
    assert "Py_GIL_DISABLED" in status.explanation


def test_probe_infers_from_abiflags(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    monkeypatch.setattr(
        gil_status.sysconfig,
        "get_config_var",
        lambda name: None,
        raising=False,
    )
    monkeypatch.setattr(gil_status.sys, "abiflags", "t")
    status = gil_status.probe()
    assert status.gil_enabled is False
    assert "ABI flag" in status.explanation


def test_probe_infers_from_env_override(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    monkeypatch.setattr(
        gil_status.sysconfig,
        "get_config_var",
        lambda name: None,
        raising=False,
    )
    monkeypatch.setenv("PYTHON_GIL", "0")
    status = gil_status.probe()
    assert status.gil_enabled is False
    assert "PYTHON_GIL" in status.explanation


def test_probe_infers_from_env_override_enabled(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    monkeypatch.setattr(
        gil_status.sysconfig,
        "get_config_var",
        lambda name: None,
        raising=False,
    )
    monkeypatch.setenv("PYTHON_GIL", "1")
    status = gil_status.probe()
    assert status.gil_enabled is True
    assert "PYTHON_GIL" in status.explanation


def test_probe_reports_free_threading(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, False)
    status = gil_status.probe()
    assert status.gil_enabled is False
    assert status.api_available is True
    assert "Free-threaded" in status.explanation


def test_cli_json_output(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    _set_probe(monkeypatch, False)
    exit_code = gil_status.main(["--json"])
    assert exit_code == 0
    captured = json.loads(capsys.readouterr().out)
    assert captured["free_threading_available"] is True


def test_cli_enforces_free_threading(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    _set_probe(monkeypatch, True)
    exit_code = gil_status.main(["--require-free-threading"])
    output = capsys.readouterr()
    assert exit_code == 1
    assert "free-threaded" in output.err


def test_cli_enforces_gil(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    _set_probe(monkeypatch, False)
    exit_code = gil_status.main(["--require-gil"])
    output = capsys.readouterr()
    assert exit_code == 1
    assert "GIL is disabled" in output.err


def test_cli_unknown_status(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    _set_probe(monkeypatch, None)
    exit_code = gil_status.main(["--require-free-threading"])
    output = capsys.readouterr()
    assert exit_code == 2
    assert "status unknown" in output.err


def test_assert_free_threading_requires_disabled(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, True)
    with pytest.raises(gil_status.GilRequirementError):
        gil_status.assert_free_threading()


def test_assert_free_threading_allows_unknown(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    status = gil_status.assert_free_threading(allow_unknown=True)
    assert status.gil_enabled is None


def test_assert_free_threading_passes_when_disabled(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, False)
    status = gil_status.assert_free_threading()
    assert status.gil_enabled is False


def test_assert_gil_enabled(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, True)
    status = gil_status.assert_gil_enabled()
    assert status.gil_enabled is True


def test_assert_gil_enabled_raises_when_disabled(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, False)
    with pytest.raises(gil_status.GilRequirementError):
        gil_status.assert_gil_enabled()


def test_assert_gil_enabled_unknown_requires_detection(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    with pytest.raises(gil_status.GilRequirementError):
        gil_status.assert_gil_enabled()


def test_assert_gil_enabled_allows_unknown(monkeypatch: pytest.MonkeyPatch):
    _set_probe(monkeypatch, None)
    status = gil_status.assert_gil_enabled(allow_unknown=True)
    assert status.gil_enabled is None
