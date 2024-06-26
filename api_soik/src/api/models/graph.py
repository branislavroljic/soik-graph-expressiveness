from .node import Node
from .edge import Edge
from typing import Set

class Graph:
    def __init__(
        self, nodes: Set[Node] = None, edges: Set[Edge] = None, directed: bool = True
    ):
        self._nodes = nodes if nodes is not None else set()
        self._edges = edges if edges is not None else set()
        self._directed = directed

    def add_node(self, node: Node):
        self._nodes.add(node)

    def remove_node(self, node: Node):
        self._nodes.remove(node)
        self._edges = {
            edge for edge in self._edges if node not in (edge.source, edge.destination)
        }

    def add_edge(self, edge: Edge):
        self._edges.add(edge)
        if not self._directed:
            inverted_edge = Edge(edge.destination, edge.source)
            self._edges.add(inverted_edge)

    @property
    def nodes(self) -> Set[Node]:
        return self._nodes

    @property
    def edges(self) -> Set[Edge]:
        return self._edges

    @edges.setter
    def edges(self, value: Set[Edge]):
        self._edges = value

    @property
    def directed(self) -> bool:
        return self._directed

    def remove_duplicates_in_edges(self):
        duplicates = []
        duplicates_id = []
        new_edges = self._edges
        for edge in self._edges:
            for new_edge in new_edges:
                if edge.equal_undirected(new_edge) and new_edge.id not in duplicates_id:
                    duplicates.append(edge)
                    duplicates_id.append(edge.id)
                    break
        for edge in duplicates:
            self._edges.remove(edge)
