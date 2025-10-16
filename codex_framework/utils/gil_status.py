"""Utilities for probing CPython's Global Interpreter Lock status.

This module provides a :func:`probe` function for programmatic use, helpers
for asserting interpreter requirements, and a small command-line interface
that prints a structured report. The goal is to keep the helpers light-weight
so Codex operators can gate DALE-G workloads during container boot scripts
without introducing heavy dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import sysconfig
from dataclasses import asdict, dataclass
from typing import Optional, Tuple


@dataclass
class GilStatus:
    """Snapshot of interpreter-level GIL configuration."""

    implementation: str
    version: str
    gil_enabled: Optional[bool]
    api_available: bool
    explanation: str

    def human_readout(self) -> str:
        """Return a single-line summary suitable for console output."""
        state = {
            True: "ENABLED",
            False: "DISABLED",
            None: "UNKNOWN",
        }[self.gil_enabled]
        return (
            f"Python {self.version} ({self.implementation}) — GIL {state}. "
            f"{self.explanation}"
        )


def _call_is_gil_enabled() -> Optional[bool]:
    """Invoke ``sys._is_gil_enabled`` when available.

    The helper uses ``getattr`` with ``raising=False`` semantics to avoid
    AttributeError on interpreters that pre-date the probe API.
    """

    probe = getattr(sys, "_is_gil_enabled", None)
    if probe is None:
        return None
    try:
        return bool(probe())
    except Exception:  # pragma: no cover - defensive: shouldn't happen
        return None


def _infer_from_build_metadata() -> Tuple[Optional[bool], Optional[str]]:
    """Best-effort inference when ``sys._is_gil_enabled`` is missing.

    Newer CPython builds expose ``Py_GIL_DISABLED`` via ``sysconfig`` or
    advertise a ``'t'`` ABI flag for the free-threaded interpreter. We also
    respect ``PYTHON_GIL`` overrides so boot scripts that toggle the setting
    can surface an explanation even on older builds.
    """

    gil_disabled = sysconfig.get_config_var("Py_GIL_DISABLED")
    if gil_disabled is not None:
        gil_disabled_bool = bool(gil_disabled)
        if gil_disabled_bool:
            return False, "Build config Py_GIL_DISABLED=1 indicates a free-threaded interpreter."
        return True, "Build config Py_GIL_DISABLED=0 indicates the standard GIL build."

    abiflags = getattr(sys, "abiflags", "")
    if abiflags and "t" in abiflags:
        return False, "ABI flag 't' found; this build targets the free-threaded ABI."

    env_override = os.environ.get("PYTHON_GIL")
    if env_override == "0":
        return False, "Environment variable PYTHON_GIL=0 requests a disabled GIL."
    if env_override == "1":
        return True, "Environment variable PYTHON_GIL=1 enforces the traditional GIL."

    return None, None


def probe() -> GilStatus:
    """Capture the interpreter's GIL status."""

    gil = _call_is_gil_enabled()
    implementation = platform.python_implementation()
    version = platform.python_version()

    if gil is None:
        inferred, note = _infer_from_build_metadata()
        if inferred is not None:
            return GilStatus(
                implementation=implementation,
                version=version,
                gil_enabled=inferred,
                api_available=False,
                explanation=note or "Interpreter build metadata inferred the GIL state.",
            )
        explanation = (
            "Interpreter does not expose sys._is_gil_enabled(); upgrade to "
            "Python 3.13+ or install the free-threaded build."
        )
        return GilStatus(
            implementation=implementation,
            version=version,
            gil_enabled=None,
            api_available=False,
            explanation=explanation,
        )

    if gil:
        explanation = (
            "This is a GIL-enabled build. Use the python3.14t binary or set "
            "PYTHON_GIL=0 to run free-threaded workloads."
        )
    else:
        explanation = "Free-threaded interpreter detected; threads may run in parallel."

    return GilStatus(
        implementation=implementation,
        version=version,
        gil_enabled=gil,
        api_available=True,
        explanation=explanation,
    )


def _status_dict(status: GilStatus) -> dict[str, object]:
    data = asdict(status)
    # Backwards compatibility helper: expose an explicit free-threading flag.
    data["free_threading_available"] = status.api_available and status.gil_enabled is False
    return data


class GilRequirementError(RuntimeError):
    """Raised when an interpreter fails a requested GIL requirement."""

    def __init__(self, status: GilStatus, message: str):
        super().__init__(message)
        self.status = status


def assert_free_threading(*, allow_unknown: bool = False) -> GilStatus:
    """Ensure the interpreter is running without the GIL.

    Parameters
    ----------
    allow_unknown:
        When ``True`` the function returns the status even if the GIL state
        cannot be detected. Otherwise a :class:`GilRequirementError` is raised
        so callers can halt the workflow.
    """

    status = probe()
    if status.gil_enabled is False:
        return status
    if status.gil_enabled is None:
        if allow_unknown:
            return status
        raise GilRequirementError(
            status,
            "GIL status unknown — interpreter lacks reliable detection mechanisms.",
        )
    raise GilRequirementError(
        status,
        "GIL is enabled — launch a python3.14t (free-threaded) interpreter before running DALE-G.",
    )


def assert_gil_enabled(*, allow_unknown: bool = False) -> GilStatus:
    """Ensure the interpreter retains the traditional GIL."""

    status = probe()
    if status.gil_enabled is True:
        return status
    if status.gil_enabled is None:
        if allow_unknown:
            return status
        raise GilRequirementError(
            status,
            "GIL status unknown — interpreter lacks reliable detection mechanisms.",
        )
    raise GilRequirementError(
        status,
        "GIL is disabled — run a standard CPython build for this workflow.",
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Probe CPython GIL status.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument(
        "--require-free-threading",
        action="store_true",
        help="Exit non-zero when the interpreter is not free-threaded.",
    )
    parser.add_argument(
        "--require-gil",
        action="store_true",
        help="Exit non-zero when the interpreter does not have the GIL enabled.",
    )
    args = parser.parse_args(argv)

    status = probe()

    if args.json:
        print(json.dumps(_status_dict(status), sort_keys=True))
    else:
        print(status.human_readout())

    exit_code = 0
    if args.require_free_threading:
        try:
            assert_free_threading(allow_unknown=False)
        except GilRequirementError as exc:
            print(str(exc), file=sys.stderr)
            exit_code = max(exit_code, 1 if exc.status.gil_enabled is not None else 2)

    if args.require_gil:
        try:
            assert_gil_enabled(allow_unknown=False)
        except GilRequirementError as exc:
            print(str(exc), file=sys.stderr)
            exit_code = max(exit_code, 1 if exc.status.gil_enabled is not None else 2)

    return exit_code


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
