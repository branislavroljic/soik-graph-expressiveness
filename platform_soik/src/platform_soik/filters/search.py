from api.models.graph import Graph
from api.models.edge import Edge
from api.models.node import Node
from platform_soik.filters.basic_filter import BasicFilter
from abc import ABC, abstractmethod

class Search(BasicFilter):

    def __init__(self, search_word: str):
        super().__init__()
        self.search_word = search_word

    def filter(self, graph: Graph) -> Graph:     
        nodes_to_remove = set()
        for node in graph.nodes:
            if self.search_word not in node:
                nodes_to_remove.add(node)
        for item in nodes_to_remove:
            graph.remove_node(item)
        return graph
    





