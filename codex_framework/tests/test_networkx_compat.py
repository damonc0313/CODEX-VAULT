"""Tests ensuring the NetworkX compatibility shim mirrors core behaviours."""

from __future__ import annotations

import importlib
import sys
import typing as t

import networkx as maybe_nx

from codex_framework._compat import networkx as shim_nx


def _resolve_real_networkx() -> t.Any:
    """Return the genuine :mod:`networkx` module when the stub is active."""

    diagraph = getattr(maybe_nx, "DiGraph", None)
    if getattr(diagraph, "__module__", "").startswith("conftest"):
        sys.modules.pop("networkx", None)
        return importlib.import_module("networkx")
    return maybe_nx


real_nx = _resolve_real_networkx()


def _build_sample_graph(mod: t.Any) -> t.Any:
    graph = mod.DiGraph()
    graph.add_node("alpha", role="thesis")
    graph.add_node("beta")
    graph.add_edge("alpha", "beta", relation="supports")
    graph.add_edge("beta", "gamma")
    return graph


def test_nodes_data_access_matches_networkx() -> None:
    """Both implementations should expose node data via ``data`` keyword."""

    for module in (real_nx, shim_nx):
        graph = _build_sample_graph(module)

        nodes_with_dict = list(graph.nodes(data=True))
        assert ("alpha", {"role": "thesis"}) in nodes_with_dict
        assert ("beta", {}) in nodes_with_dict

        nodes_with_default = list(graph.nodes(data="role", default="unknown"))
        assert ("alpha", "thesis") in nodes_with_default
        assert ("beta", "unknown") in nodes_with_default

        # Ensure requesting without data still returns an iterable view
        plain_view = graph.nodes()
        assert hasattr(plain_view, "__iter__")
        assert "alpha" in list(plain_view)


def test_edges_data_access_matches_networkx() -> None:
    """Both implementations should expose edge data via ``data`` keyword."""

    for module in (real_nx, shim_nx):
        graph = _build_sample_graph(module)

        edges_without_data = list(graph.edges())
        assert ("alpha", "beta") in edges_without_data
        assert ("beta", "gamma") in edges_without_data

        edges_with_dict = list(graph.edges(data=True))
        assert ("alpha", "beta", {"relation": "supports"}) in edges_with_dict

        edges_with_default = list(
            graph.edges(data="relation", default="untyped")
        )
        assert ("beta", "gamma", "untyped") in edges_with_default
