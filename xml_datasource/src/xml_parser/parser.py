import os
import xml.etree.ElementTree as ET
from apl.graph.models import Graph, Node, Edge
from apl.graph.services.loader import Parser

def get_absolute_path(path):
    return os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", path)

class XMLParser(Parser):
    def __init__(self):
        self._nodes = {}
        self._graph = Graph()
        self._counter = 0  

    def name(self):
        return "Parsiranje podataka iz XML datoteke."

    def identifier(self):
        return "xml_reader"
    
    #Metoda za ucitavanje XML fajla i kreiranje grafa
    def load(self, path):
        absolute_path = get_absolute_path(path)
        try:
            #Citanje XML fajla i dobijanje korena
            tree = ET.parse(absolute_path)
            root = tree.getroot()

            if root is not None:
                #Kreiranje strukture grafa iz korena
                root_data = self._get_root(root)
                self._parse_elements(root_data)
                self._apply_semantics()

                #Uklanjanje duplikata u granama grafa
                self._graph.edges = set(self._graph.edges)
                self._graph.remove_duplicates_in_edges()

                return self._graph

        except FileNotFoundError:
            print("File does not exist")
            raise FileNotFoundError("XML file " + path + " not found!")

        except ET.ParseError:
            print("Error parsing XML")
            raise ValueError("Error parsing the XML file " + path)
    
    #Metoda za dobijanje korena XML strukture
    def _get_root(self, element):        
        root_data = {'tag': 'root', 'attributes': element.attrib, 'children': list(element)}
        for child in root_data['children']:
            self._set_ref_to_parent(child, root_data)
        return root_data
    
    #Metoda za postavljanje referenci ka roditelju
    def _set_ref_to_parent(self, child, parent):        
        if child is not None:
            if 'id' not in child.attrib:
                child.attrib['id'] = "value_" + str(self._counter)
                self._counter += 1
            if 'ref' in parent:
                parent['ref'].append(child.attrib['id'])
            else:
                parent['ref'] = [child.attrib['id']]
    
    #Metoda za dodavanje ref atributa roditelju
    def _add_ref_attr(self, parent):        
        if 'ref' not in parent:
            parent['ref'] = []
    
    #Metoda za brisanje atributa
    def _delete_attr(self, parent, attr_for_deleting):        
        for attribute in attr_for_deleting:
            del parent[attribute]
        return parent
    
    #Metoda za kreiranje cvora u grafu
    def _make_node(self, element):        
        if 'id' not in element.attrib:
            element.attrib['id'] = "value_" + str(self._counter)
            self._counter += 1
        id_e = element.attrib['id']
        node = Node(id_e, {'tag': element.tag, 'attributes': element.attrib})
        self._graph.nodes.append(node)
        self._nodes[str(id_e)] = node
    
    #Metoda za kreiranje grane u grafu
    def _make_edge(self, parent_node, child_node):        
        edge = Edge(parent_node, child_node, False)
        self._graph.edges.append(edge)
    
    #Rekurzivna metoda za analizu XML elemenata
    def _parse_elements(self, parent):        
        attr_for_deleting = []
        self._add_ref_attr(parent)
        for child in parent['children']:
            attr_for_deleting.append('children')
            self._set_ref_to_parent(child, parent)

            child_id = child.attrib['id']
            parent_id = parent['attributes']['id']
            child_node = self._nodes[child_id]
            parent_node = self._nodes[parent_id]

            self._make_edge(parent_node, child_node)

            if child_id not in self._nodes:
                self._make_node(child)

            self._parse_elements(child)

        parent = self._delete_attr(parent, attr_for_deleting)
        self._make_node(parent)
    
    #Metoda za primenu semantike
    def _apply_semantics(self):        
        for edge in self._graph.edges:
            if 'ref' in edge.source.attributes:
                for ref_id in edge.source.attributes['ref']:
                    ref_node = self._nodes.get(ref_id)
                    if ref_node:
                        self._graph.edges.add(Edge(ref_node, edge.target, False))
                        