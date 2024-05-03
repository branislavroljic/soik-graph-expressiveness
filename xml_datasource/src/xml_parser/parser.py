import xml.etree.ElementTree as ET
from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge
from api.services.loader import Parser

class XMLParser(Parser):
    def __init__(self):
        self._nodes = {}
        self._graph = Graph()
        self._counter = 0

    def get_name(self):
        return "Parsiranje podataka iz XML datoteke."

    def get_identifier(self):
        return "xml_reader"

    def load(self, file):
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            self._parse_nodes(root)
            self._make_edges()
            self._graph.edges = set(self._graph.edges)
            self._graph.remove_duplicates_in_edges()
            return self._graph
        except FileNotFoundError:
            print("File does not exist")
            raise FileNotFoundError("XML file not found!")

    def _parse_nodes(self, parent):
        self._make_node(parent)
        for child in parent:
            self._parse_nodes(child)

    def _make_node(self, parent):
        node_data = {}
        for key, value in parent.items():
            node_data[key] = value
        node = Node("value_" + str(self._counter), node_data)
        self._counter += 1
        self._graph.nodes.add(node)
        self._nodes[node.id] = node

    def _make_edges(self):
        for parent_id, parent_node in self._nodes.items():
            for child in parent_node.data:
                child_id = child["id"]
                if child_id in self._nodes:
                    edge = Edge(parent_node, self._nodes[child_id])
                    self._graph.edges.add(edge)
