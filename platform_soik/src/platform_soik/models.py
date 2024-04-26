class Workspace:
    id = 1

    def __init__(
        self,
        name: str,
        data_source_id: str,
        search_param="",
        filter_params=None,
    ) -> None:

        self.id = Workspace.id
        Workspace.id += 1

        self.name = name
        self.data_source_id = data_source_id
        self.search_param = search_param
        self.filter_params = filter_params

    def update(self, name, data_source_id: str, search_param="", filter_params=None):
        self.name = name
        self.data_source_id = data_source_id
        self.search_param = search_param
        self.filter_params = filter_params
