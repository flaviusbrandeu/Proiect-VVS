class Filesystem:
    def __init__(self, root, default_page, server_state, maintenance_page, resource_not_found_page):
        self.root = root
        self.default_page = default_page
        self.server_state = server_state
        self.maintenance_page = maintenance_page
        self.resource_not_found_page = resource_not_found_page

    def get_resource_path(self, resource):
        raise NotImplementedError()
