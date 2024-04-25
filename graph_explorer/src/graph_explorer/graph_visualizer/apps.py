from django.apps import AppConfig
import pkg_resources

from api.services.loader import Parser
from api.services.visualizer import VisualizerService


class GraphVisualizerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graph_visualizer"
    plugins_visualization : list[VisualizerService] = []
    plugins_loader : list[Parser] = []
    graph = None

    def ready(self) -> None:
        self.plugins_visualization = load_plugins("graph.visualization")
        self.plugins_loader = load_plugins("graph.loader")
        # self.graph = load_graph()


def load_plugins(group_name):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=group_name):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        # plugin = p()
        # plugins.append(plugin)
    return plugins
