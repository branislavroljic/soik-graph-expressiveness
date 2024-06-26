class Node:
    def __init__(self, id: str, data: dict = None):
        self._id = id
        self._data = data if data is not None else {}

    @property
    def id(self) -> str:
        return self._id

    @property
    def data(self) -> dict:
        return self._data

    def add_data(self, key: str, value) -> None:
        self._data[key] = value

    def __hash__(self) -> int:
        return hash(self._id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self._id == other.id

    def __str__(self) -> str:
        if not self._data:
            return ""
        return "\n".join(f"{key}: {value}" for key, value in self._data.items())

    def __contains__(self, givenValue):
        if givenValue in self.id:
            return True
        for key, value in self._data.items():
            if str(givenValue) in key:
                return True
            if value is not None and str(givenValue) in value:
                return True
        return False
