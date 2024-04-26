from django.apps import AppConfig

from api.services.loader import Parser
from api.services.visualizer import VisualizerService
from platform_soik.src.platform_soik.apps import load_plugins
from platform_soik.src.platform_soik.models import Workspace


class GraphVisualizerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graph_visualizer"
    plugins_visualization: list[VisualizerService] = []
    plugins_loader: list[Parser] = []
    workspaces: list[Workspace] = []

    def ready(self) -> None:
        self.plugins_loader, self.plugins_visualization = load_plugins()
