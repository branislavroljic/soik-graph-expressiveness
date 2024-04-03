from abc import ABC, abstractmethod


class VisualizerService(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_identifier(self):
        pass

    @abstractmethod
    def visualize(self, graph):
        pass
