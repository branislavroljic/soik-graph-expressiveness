from api.services.loader import Parser
from api.services.visualizer import VisualizerService
import pkg_resources


def _load_plugins(group_name):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=group_name):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins


def load_plugins() -> tuple[list[Parser], list[VisualizerService]]:
    plugins_loader = _load_plugins("graph.datasources")
    plugins_visualization = _load_plugins("graph.visualization")
    return plugins_loader, plugins_visualization
