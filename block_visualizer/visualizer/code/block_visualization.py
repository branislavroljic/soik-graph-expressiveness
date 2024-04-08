from os.path import dirname, abspath, join
from jinja2 import Environment, select_autoescape, FileSystemLoader
from api.models.graph import Graph
from api.models.node import Node
from api.models.edge import Edge
from api.services.visualizer import VisualizerService


class BlockGraphVisualizer(VisualizerService):

    def __init__(self):
        path = join(dirname(dirname(abspath(__file__))), "static")
        print(path)
        env = Environment(
            loader=FileSystemLoader(path),
            autoescape=select_autoescape(enabled_extensions=("html", "xml")),
        )
        self.template = env.get_template("block_visualization.html")

    def get_name(self):
        return "Block graph visualization"

    def get_identifier(self):
        return "block_graph_visualizer"

    def visualize(self, graph):
        nodes = self.parse_nodes(graph)
        edges = self.parse_edges(graph)

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
                "name": node.data["name"] if "name" in node.data else "N/A",
                "data": node.data,
            }

            nodes.append(node_data)
        return nodes

    def parse_edges(self, graph):
        edges = []
        for edge in graph.edges:
            edge_data = {
                "source_node": edge.source,
                "destination_node": edge.destination,
            }
            edges.append(edge_data)
        return edges


class MockGraph(Graph):

    def load_graph(self):
        # Create nodes
        # Create nodes
        node1 = Node(id=1, data={"name": "A", "type": "typeA", "desc": "descA"})
        node2 = Node(id=2, data={"name": "B", "type": "typeA", "desc": "descB"})
        node3 = Node(id=3, data={"name": "C", "type": "typeA", "desc": "descC"})
        node4 = Node(
            id=4, data={"name": "DANAS", "type": "typeDANAS", "desc": "descDANAS"}
        )
        node5 = Node(id=5, data={"name": "E", "type": "typeA", "desc": "descE"})
        node6 = Node(id=6, data={"name": "F", "type": "typeA", "desc": "descF"})
        node7 = Node(id=7, data={"name": "G", "type": "typeA", "desc": "descG"})
        node8 = Node(id=8, data={"name": "H", "type": "typeA", "desc": "descH"})
        node9 = Node(id=9, data={"name": "I", "type": "typeA", "desc": "desci"})
        node10 = Node(id=10, data={"name": "J", "type": "typeA", "desc": "descj"})

        # Create edges
        edge1 = Edge(source=node1, destination=node2)
        edge2 = Edge(source=node2, destination=node3)
        edge3 = Edge(source=node3, destination=node4)
        edge4 = Edge(source=node4, destination=node5)
        edge5 = Edge(source=node5, destination=node1)
        edge6 = Edge(source=node6, destination=node7)
        edge7 = Edge(source=node7, destination=node8)
        edge8 = Edge(source=node8, destination=node6)
        edge9 = Edge(source=node9, destination=node9)  # Recursive connection
        edge10 = Edge(source=node10, destination=node10)  # Recursive connection

        nodes = {node1, node2, node3, node4, node5, node6, node7, node8, node9, node10}
        edges = {edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8, edge9, edge10}
        # Create a graph
        graph = Graph(nodes=nodes, edges=edges, directed=True)
        return graph


if __name__ == "__main__":
    visualizer = BlockGraphVisualizer()
    mock_graph = MockGraph()
    html_output = visualizer.visualize(mock_graph.load_graph())
    html_output = visualizer.visualize(mock_graph.load_graph())

    # Write the HTML content to a file
    with open("block_graph_visualization.html", "w") as html_file:
        html_file.write(html_output)
