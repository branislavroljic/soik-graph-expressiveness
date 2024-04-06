from os.path import abspath, dirname, join
from jinja2 import Environment, FileSystemLoader, select_autoescape

from api.services.visualizer import VisualizerService


class SimpleGraphVisualizer(VisualizerService):
    def __init__(self):
        path = join(dirname(dirname(abspath(__file__))), "static")
        print(path)
        env = Environment(
            loader=FileSystemLoader(path),
            autoescape=select_autoescape(enabled_extensions=("html", "xml")),
        )
        self.template = env.get_template("simple_visualization.html")

    def get_name(self):
        return "Simple graph visualization"

    def get_identifier(self):
        return "simple_graph_visualizer"

    def visualize(self, graph):

        nodes = self.parse_nodes(graph)
        edges = self.parse_edges(graph)
        print(len(nodes))

        return self.template.render(
            nodes=nodes,
            edges=edges,
            directed=graph.directed,
            name=self.get_identifier(),
        )

    def parse_nodes(self, graph):
        nodes = []
        for node in graph.nodes:
            if not node.id:
                continue

            node_data = {
                "id": node.id,
                "name": node.attributes["name"] if "name" in node.attributes else "N/A",
            }

            nodes.append(node_data)
        return nodes

    def parse_edges(self, graph):
        edges = []
        for edge in graph.edges:
            edge_data = {}
            if edge.source and edge.destination:
                edge_data["source_node"] = edge.source
                edge_data["destination_node"] = edge.destination
            edges.append(edge_data)
        return edges
