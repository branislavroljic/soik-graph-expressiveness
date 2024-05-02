from api.services.loader import Parser
from api.services.visualizer import VisualizerService
from platform_soik.models import Workspace


class PlatformConfig:

    def __init__(
        self,
        plugins_visualization: list[VisualizerService],
        plugins_loader: list[Parser],
    ):
        self.plugins_visualization = plugins_visualization
        self.plugins_loader = plugins_loader
        self.workspaces: list[Workspace] = []
        self.current_workspace: Workspace | None = None

    def add_workspace(self, workspace):
        self.workspaces.append(workspace)
        self.current_workspace = workspace

    def delete_workspace(self, _id):
        self.workspaces = [ws for ws in self.workspaces if ws.id != _id]
        if self.current_workspace.id == _id:
            self.current_workspace = None

    def select_workspace(self, _id):
        for ws in self.workspaces:
            if ws.id == _id:
                self.current_workspace = ws
                break
        return self.current_workspace

    def get_context(self):
        content = {
            "data_sources": [
                {"id": ds.get_identifier(), "name": ds.get_name()}
                for ds in self.plugins_loader
            ],
            "visualizers": [
                {"id": v.get_identifier(), "name": v.get_name()}
                for v in self.plugins_visualization
            ],
            "current_visualizer": (
                self.current_workspace.visualizer_plugin.get_identifier()
                if self.current_workspace
                else None
            ),
            "current_data_source": (
                self.current_workspace.data_source_plugin.get_identifier()
                if self.current_workspace
                else None
            ),
            "content": (
                self.current_workspace.visualizer_plugin.visualize(
                    self.current_workspace.graph
                )
                if self.current_workspace
                else None
            ),
            "workspaces": [{"id": ws.id, "name": ws.name} for ws in self.workspaces],
            "current_ws_id": (
                self.current_workspace.id if self.current_workspace else None
            ),
        }
        return content
