from api.models.graph import Graph
from api.models.edge import Edge
from api.models.node import Node
from platform_soik.filters.basic_filter import BasicFilter
from abc import ABC, abstractmethod

class Filter(BasicFilter):

    operators = {
        "eq": lambda a, b: a == b,
        "gt": lambda a, b: a > b,
        "lt": lambda a, b: a < b,
        "ge": lambda a, b: a >= b,
        "le": lambda a, b: a <= b,
        "ne": lambda a, b: a != b,
    }

    def __init__(self, filter_attribute, filter_operator, filter_value):
        super().__init__()
        self.filter_attribute = filter_attribute
        self.filter_operator = filter_operator
        self.filter_value = filter_value

        if self.filter_operator not in Filter.operators:
            ValueError()
        self.operator = Filter.operators[self.filter_operator]


    def requiredCondition(self, node: Node) -> bool:
        if self.filter_attribute == 'id':
            return self.operator(node.id, self.filter_value)
        if self.filter_attribute not in node.data:
            return False
        return self.operator(node.data[self.filter_attribute], self.filter_value)


    def filter(self, graph: Graph) -> Graph:     
        nodes_to_remove = set()
        for node in graph.nodes:
            if not self.requiredCondition(node):
                nodes_to_remove.add(node)
        for item in nodes_to_remove:
            graph.remove_node(item)
        return graph