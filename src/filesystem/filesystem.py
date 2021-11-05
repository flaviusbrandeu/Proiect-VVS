class Filesystem:
    def __init__(self, root: str, default_page: str, server_state: State, maintenance_page: str,
                 resource_not_found_page: str) -> str:
        self.root = root
        self.default_page = default_page
        self.server_state = server_state
        self.maintenance_page = maintenance_page
        self.resource_not_found_page = resource_not_found_page

    def get_resource_path(self, resource):
        raise NotImplementedError()
