from .node import Node


class Edge:
    id_counter = 0

    def __init__(self, source: Node, destination: Node):
        self._source = source
        self._destination = destination
        self._id = Edge.id_counter
        Edge.id_counter += 1

    @property
    def source(self) -> Node:
        return self._source

    @property
    def destination(self) -> Node:
        return self._destination

    @property
    def id(self) -> int:
        return self._id

    def __hash__(self) -> int:
        return hash((self._source.id, self._destination.id))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Edge):
            return False
        return self._source == other.source and self._destination == other.destination

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def equal_undirected(self, other) -> bool:
        return self._source == other.destination and self._destination == other.source
