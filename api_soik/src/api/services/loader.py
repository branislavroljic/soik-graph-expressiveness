from abc import abstractmethod, ABC

class GraphService(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_identifier(self):
        pass

class Parser(GraphService):
    @abstractmethod
    def load(self, path):
        pass
