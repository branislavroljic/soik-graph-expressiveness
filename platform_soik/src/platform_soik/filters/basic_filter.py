from api.models.graph import Graph

from abc import ABC, abstractmethod

class BasicFilter(ABC):

    @abstractmethod
    def filter(self, graph: Graph) -> Graph:
        pass

 


