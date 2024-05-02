import time

from api.models.graph import Graph
from api.services.loader import Parser
from api.services.visualizer import VisualizerService
from visualizer.code.block_visualization import BlockGraphVisualizer
from visualizer.code.simple_visualization import SimpleGraphVisualizer
from json_parser.parser import JSONParser
from xml_parser.parser import XMLParser

data_source_plugins = {
    JSONParser().get_identifier(): JSONParser(),
    XMLParser().get_identifier(): XMLParser(),
}

visualizer_plugins = {
    SimpleGraphVisualizer().get_identifier(): SimpleGraphVisualizer(),
    BlockGraphVisualizer().get_identifier(): BlockGraphVisualizer(),
}


class Workspace:

    def __init__(self):
        self.__id: int = int(time.time())
        self.__name: str = ""
        self.__file = None
        self.__data_source_plugin: Parser | None = None
        self.__visualizer_plugin: VisualizerService | None = None
        self.__graph: Graph | None = None
        self.__initial_graph: Graph | None = None
        self.__search_param: str = ""
        self.__filter_params: list[str] = []

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> int:
        return self.__name

    @name.setter
    def name(self, name) -> None:
        self.__name = name

    @property
    def file(self) -> str:
        return self.__file

    @file.setter
    def file(self, file) -> None:
        self.__file = file

    @property
    def data_source_plugin(self) -> Parser:
        return self.__data_source_plugin

    # @data_source_plugin.setter
    # def data_source_plugin(self, value):
    #     self.__data_source_plugin = value

    @property
    def visualizer_plugin(self) -> VisualizerService:
        return self.__visualizer_plugin

    # @visualizer_plugin.setter
    # def visualizer_plugin(self, value):
    #     self.__visualizer_plugin = value

    @property
    def search_param(self) -> str:
        return self.__search_param

    @search_param.setter
    def search_param(self, value):
        self.__search_param = value

    @property
    def filter_params(self) -> list[str]:
        return self.__filter_params

    @filter_params.setter
    def filter_params(self, value):
        self.__filter_params = value

    @property
    def graph(self) -> str:
        return self.__graph

    @property
    def initial_graph(self) -> str:
        return self.__initial_graph

    def set_data_source_plugin(self, data_source_id: str) -> None:
        if data_source_id not in data_source_plugins:
            raise ValueError("Invalid data source type")
        self.__data_source_plugin = data_source_plugins[data_source_id]
        self.__initial_graph = self.__data_source_plugin.load(self.__file)
        self.__graph = self.__initial_graph

    def set_visualizer_plugin(self, visualizer_id: str) -> None:
        if visualizer_id not in visualizer_plugins:
            raise ValueError("Invalid visualizer type")
        self.__visualizer_plugin = visualizer_plugins[visualizer_id]
