from django.apps import AppConfig

from api.services.loader import Parser
from api.services.visualizer import VisualizerService
from platform_soik.apps import load_plugins
from platform_soik.models import Workspace
from platform_soik.config import PlatformConfig


class GraphVisualizerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graph_visualizer"
    plugins_visualization: list[VisualizerService] = []
    plugins_loader: list[Parser] = []
    workspaces: list[Workspace] = []

    def ready(self) -> None:
        self.plugins_loader, self.plugins_visualization = load_plugins()

    def get_platform_config(self) -> PlatformConfig:
        return PlatformConfig(self.plugins_visualization, self.plugins_loader)
