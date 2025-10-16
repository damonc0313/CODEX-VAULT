"""Pytest configuration for Codex Framework tests."""

import sys
from types import SimpleNamespace


class DummyDiGraph:
    """Minimal stub of :mod:`networkx`'s :class:`DiGraph` for test imports."""

    def __init__(self, *args, **kwargs):  # noqa: D401 - simple stub
        self.args = args
        self.kwargs = kwargs


if "networkx" not in sys.modules:
    sys.modules["networkx"] = SimpleNamespace(DiGraph=DummyDiGraph)
