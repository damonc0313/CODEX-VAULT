"""Lightweight compatibility shim for a subset of :mod:`networkx` APIs."""

from __future__ import annotations

import typing as t

_Hashable = t.Hashable


class _NodesView(t.Mapping[_Hashable, dict[str, t.Any]]):
    """Minimal node view replicating :class:`networkx.classes.reportviews.NodeView`."""

    def __init__(self, graph: "DiGraph") -> None:
        self._graph = graph

    def __iter__(self) -> t.Iterator[_Hashable]:
        return iter(self._graph._node)

    def __len__(self) -> int:
        return len(self._graph._node)

    def __contains__(self, node: object) -> bool:
        return node in self._graph._node

    def __getitem__(self, node: _Hashable) -> dict[str, t.Any]:
        return self._graph._node[node]

    def data(self, data: bool | str = True, default: t.Any = None) -> t.Iterable[t.Any]:
        """Return iterable with node data following NetworkX semantics."""

        return self.__call__(data=data, default=default)

    def __call__(
        self, data: bool | str = False, default: t.Any = None
    ) -> t.Iterable[t.Any] | "_NodesView":
        """Return the node view or node/data pairs depending on ``data`` flag."""

        if not data:
            return self

        if data is True:
            return ((node, attrs) for node, attrs in self._graph._node.items())

        attr_name = t.cast(str, data)
        return (
            (node, self._graph._node[node].get(attr_name, default))
            for node in self._graph._node
        )


class _EdgesView(t.Iterable[tuple[_Hashable, _Hashable]]):
    """Minimal edge view replicating :class:`networkx.classes.reportviews.OutEdgeView`."""

    def __init__(self, graph: "DiGraph") -> None:
        self._graph = graph

    def __iter__(self) -> t.Iterator[tuple[_Hashable, _Hashable]]:
        for source, targets in self._graph._succ.items():
            for target in targets:
                yield source, target

    def __len__(self) -> int:
        return sum(len(targets) for targets in self._graph._succ.values())

    def __contains__(self, edge: object) -> bool:
        if not isinstance(edge, tuple) or len(edge) != 2:
            return False
        source, target = edge
        return source in self._graph._succ and target in self._graph._succ[source]

    def data(
        self, data: bool | str = True, default: t.Any = None
    ) -> t.Iterable[t.Any]:
        """Return iterable with edge data following NetworkX semantics."""

        return self.__call__(data=data, default=default)

    def __call__(
        self, data: bool | str = False, default: t.Any = None
    ) -> t.Iterable[t.Any] | "_EdgesView":
        """Return the edge view or edge/data tuples depending on ``data`` flag."""

        if not data:
            return self

        if data is True:
            return (
                (source, target, attrs)
                for source, targets in self._graph._succ.items()
                for target, attrs in targets.items()
            )

        attr_name = t.cast(str, data)
        return (
            (source, target, attrs.get(attr_name, default))
            for source, targets in self._graph._succ.items()
            for target, attrs in targets.items()
        )


class DiGraph:
    """Very small subset of :class:`networkx.DiGraph` required by the framework."""

    def __init__(self) -> None:
        self._node: dict[_Hashable, dict[str, t.Any]] = {}
        self._succ: dict[_Hashable, dict[_Hashable, dict[str, t.Any]]] = {}
        self._pred: dict[_Hashable, dict[_Hashable, dict[str, t.Any]]] = {}
        self._nodes_view = _NodesView(self)
        self._edges_view = _EdgesView(self)

    def add_node(self, node_for_adding: _Hashable, **attrs: t.Any) -> None:
        node_attrs = self._node.setdefault(node_for_adding, {})
        node_attrs.update(attrs)
        self._succ.setdefault(node_for_adding, {})
        self._pred.setdefault(node_for_adding, {})

    def add_nodes_from(
        self,
        nodes_for_adding: t.Iterable[_Hashable | tuple[_Hashable, dict[str, t.Any]]],
        **common_attrs: t.Any,
    ) -> None:
        for item in nodes_for_adding:
            if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], dict):
                node, attr_dict = item[0], dict(item[1])
            else:
                node, attr_dict = item, {}
            merged_attrs = {**attr_dict, **common_attrs}
            if node is not None:
                self.add_node(t.cast(_Hashable, node), **merged_attrs)

    def add_edge(
        self,
        u_of_edge: _Hashable,
        v_of_edge: _Hashable,
        **attrs: t.Any,
    ) -> None:
        self.add_node(u_of_edge)
        self.add_node(v_of_edge)
        edge_attrs = self._succ[u_of_edge].setdefault(v_of_edge, {})
        edge_attrs.update(attrs)
        self._pred[v_of_edge][u_of_edge] = edge_attrs

    def add_edges_from(
        self,
        ebunch_to_add: t.Iterable[
            tuple[_Hashable, _Hashable] | tuple[_Hashable, _Hashable, dict[str, t.Any]]
        ],
        **common_attrs: t.Any,
    ) -> None:
        for edge in ebunch_to_add:
            if len(edge) == 3 and isinstance(edge[2], dict):
                u, v, attr_dict = edge
                attrs = {**attr_dict, **common_attrs}
            elif len(edge) == 2:
                u, v = edge  # type: ignore[misc]
                attrs = dict(common_attrs)
            else:
                raise ValueError("Edges must be 2-tuples or 3-tuples with attribute dict")
            self.add_edge(u, v, **attrs)

    def number_of_nodes(self) -> int:
        return len(self._node)

    def number_of_edges(self) -> int:
        return sum(len(targets) for targets in self._succ.values())

    @property
    def nodes(self) -> _NodesView:
        return self._nodes_view

    @property
    def edges(self) -> _EdgesView:
        return self._edges_view

    def get_edge_data(
        self, u: _Hashable, v: _Hashable, default: t.Any = None
    ) -> dict[str, t.Any] | t.Any:
        return self._succ.get(u, {}).get(v, default)

    def __iter__(self) -> t.Iterator[_Hashable]:
        return iter(self._node)

    def __contains__(self, node: object) -> bool:
        return node in self._node


__all__ = ["DiGraph"]
