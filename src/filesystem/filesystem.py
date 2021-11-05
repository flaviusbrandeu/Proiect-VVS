import os.path
from src.webserver.webserver import State


class Filesystem:
    def __init__(self, root: str, default_page: str, server_state: State, maintenance_page: str,
                 resource_not_found_page: str) -> str:
        self.root = root
        self.default_page = default_page
        self.server_state = server_state
        self.maintenance_page = maintenance_page
        self.resource_not_found_page = resource_not_found_page

    def get_resource_path(self, resource):
        path_to_resource = os.path.join(self.root, resource)
        if self.server_state == State.RUNNING:
            return self.__get_resource_path_server_running(path_to_resource)
        elif self.server_state == State.MAINTENANCE:
            return self.maintenance_page

    def __get_resource_path_server_running(self, path_to_resource) -> str:
        if os.path.isfile(path_to_resource):
            return path_to_resource
        else:
            return self.resource_not_found_page
