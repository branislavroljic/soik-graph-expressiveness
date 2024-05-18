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
            root_data = self._get_root(root)
            self._parse_nodes(root_data)
            self._make_edges()
            self._graph.edges = set(self._graph.edges)
            self._graph.remove_duplicates_in_edges()
            return self._graph

        except FileNotFoundError:
            print("File does not exist")
            raise FileNotFoundError("XML file not found!")

    def _get_root(self, data):
        data.set('id', 'root')
        self._add_ref_attr(data)
        for child in list(data):
            self._set_ref_to_parent(child, data)
        return data

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

    def _delete_attr(self, parent, attr_for_deleting):
        for attribute in attr_for_deleting:
            if attribute in parent.attrib:
                del parent.attrib[attribute]
        return parent

    def _make_node(self, parent):
        if 'id' not in parent.attrib:
            parent.set('id', 'value_' + str(self._counter))
            self._counter += 1
        id_p = parent.get('id')
        node = Node(id_p, self._element_to_dict(parent))
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

    def _parse_nodes(self, parent):
        attr_for_deleting = []
        self._add_ref_attr(parent)
        if parent is not None:
            for key, value in parent.attrib.items():
                if isinstance(value, str) and value.startswith('value_'):
                    self._set_ref_to_parent(parent, parent)
                    attr_for_deleting.append(key)

            for child in list(parent):
                self._set_ref_to_parent(child, parent)
                self._make_node(child)  # Only create nodes for direct children

            parent = self._delete_attr(parent, attr_for_deleting)
            self._make_node(parent)

    def _element_to_dict(self, element):
        data = {}
        for child in list(element):
            data[child.tag] = child.text
        data.update(element.attrib)
        data['tag'] = element.tag
        return data
