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

    def _set_ref_to_parent(self, child, parent):
        if child is not None:
            if 'id' not in child.attrib:
                child.set('id', 'value_' + str(self._counter))
                self._counter += 1
            if '@ref' in parent.attrib:
                parent.attrib['@ref'] += ' ' + child.get('id')
            else:
                parent.attrib['@ref'] = child.get('id')

    def _add_ref_attr(self, parent):
        if parent is not None:
            if '@ref' not in parent.attrib:
                parent.attrib['@ref'] = ''

    def _make_node(self, element):
        if 'id' not in element.attrib:
            element.set('id', 'value_' + str(self._counter))
            self._counter += 1
        id_p = element.get('id')
        node = Node(id_p, self._element_to_dict(element))
        if node is not None:
            self._graph.nodes.add(node)
            self._nodes[id_p] = node

    def _make_edges(self):
        for id, parent_node in self._nodes.items():
            if '@ref' in parent_node.data.keys():
                child_ids = parent_node.data['@ref'].split()
                for child_id in child_ids:
                    if child_id in self._nodes:
                        child_node = self._nodes[child_id]
                        edge = Edge(parent_node, child_node)
                        self._graph.edges.add(edge)
                del parent_node.data['@ref']

    def _parse_nodes(self, element):
        self._add_ref_attr(element)
        for child in list(element):
            self._set_ref_to_parent(child, element)
            self._parse_nodes(child)
        self._make_node(element)

    def _element_to_dict(self, element):
        data = {child.tag: child.text for child in list(element)}
        data.update(element.attrib)
        data['tag'] = element.tag
        return data
