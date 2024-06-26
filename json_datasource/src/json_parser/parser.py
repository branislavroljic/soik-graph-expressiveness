import json
import os
from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge
from api.services.loader import Parser


class JSONParser(Parser):
    def __init__(self):
        self._nodes = {}
        self._graph = Graph()
        self._counter = 0

    def get_name(self):
        return "Parsiranje podataka iz JSON datoteke."

    def get_identifier(self):
        return "json_reader"

    def load(self, file):
        try:
            # Read the entire file content into a string
            content = file.read()
            if content != "":
                # Parse JSON data
                graph_data = json.loads(content)
                root_data = self._get_root(graph_data)
                # Create nodes from objects in the JSON data
                self._parse_nodes(root_data)
                # Make edges after all nodes and references between nodes are created
                self._make_edges()
                self._graph.edges = set(self._graph.edges)  
                self._graph.remove_duplicates_in_edges()
                return self._graph

        except FileNotFoundError:
            print("File does not exist")
            raise FileNotFoundError("JSON file not found!")

    # Set the first object to be root
    def _get_root(self, data):
        if isinstance(data, dict):
            data["id"] = "root"
            data_children = list(data.values())[0]
            # For every child of the root set the id and make references to the parent
            if isinstance(data_children, list):
                for child in data_children:
                    self._set_ref_to_parent(child, data)

            else:
                self._set_ref_to_parent(data_children, data)
            return data
        else:
            new_dict = {"id": "root", "data": data}
            return new_dict

    # If the child does not have id it sets it and makes the reference from parent to child
    def _set_ref_to_parent(self, child, parent):
        if child is not None:
            if "id" not in child.keys():
                child["id"] = "value_" + str(self._counter)
                self._counter += 1
            else:
                id_c = child["id"]
                child["id"] = str(id_c)
            if "@ref" in parent.keys():
                parent["@ref"].append(str(child["id"]))
            else:
                parent["@ref"] = [str(child["id"])]

    def _add_ref_attr(self, parent):
        if parent is not None:
            if "@ref" not in parent.keys():
                parent["@ref"] = []

    def _delete_attr(self, parent, attr_for_deleting):
        for attribute in attr_for_deleting:
            del parent[attribute]
        return parent

    def _make_node(self, parent):
        if "id" not in parent.keys():
            parent["id"] = "value_" + str(self._counter)
            self._counter += 1
        id_p = parent["id"]
        node = Node(id_p, parent)
        if node is not None:
            self._graph.nodes.add(node)
            self._nodes[str(id_p)] = node

    def _make_edges(self):
        for id, parent_node in self._nodes.items():
            if "@ref" in parent_node.data.keys():
                for child_node_id in parent_node.data["@ref"]:
                    child_node = self._nodes[child_node_id]
                    edge = Edge(parent_node, child_node)
                    self._graph.edges.add(edge)
                del parent_node.data["@ref"]

    def _parse_nodes(self, parent):
        attr_for_deleting = []
        self._add_ref_attr(parent)
        if parent is not None:
            # For every attribute is checked if it is object, list or simple tipe
            for key, value in parent.items():
                # If the value of the attribute is dictionary it is treated as object
                # and there is a recursive call of the _parse_nodes() function
                if isinstance(value, dict) and key != "@ref":
                    attr_for_deleting.append(key)
                    self._set_ref_to_parent(value, parent)
                    self._parse_nodes(value)

                # If the value is a list, then every list element is sent as
                # a parameter in a recursive call of the _parse_nodes() function
                elif isinstance(value, list) and key != "@ref":
                    if len(value) != 0 and isinstance(value[0], dict):
                        attr_for_deleting.append(key)
                        for child in value:
                            self._set_ref_to_parent(child, parent)
                            self._parse_nodes(child)

                # If the value is a None type
                elif value is None:
                    parent[key] = "no value"

            # Attributes of lists and objects are deleted
            parent = self._delete_attr(parent, attr_for_deleting)
            # Parent is made in to a node
            self._make_node(parent)











