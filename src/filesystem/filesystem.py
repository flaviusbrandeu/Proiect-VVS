import os.path
from src.webserver.webserver import State
import urllib.parse


class Filesystem:
    def __init__(self, root: str, default_page_path: str, server_state: State, maintenance_page_path: str,
                 resource_not_found_page_path: str) -> str:
        self.root = root
        self.default_page_path = default_page_path
        self.server_state = server_state
        self.maintenance_page_path = maintenance_page_path
        self.resource_not_found_page_path = resource_not_found_page_path

    def get_resource_path(self, resource):
        resource_unquoted = urllib.parse.unquote(resource)
        if resource_unquoted[0] == "/":
            resource_unquoted = resource_unquoted[1:]
        path_to_resource = os.path.join(self.root, resource_unquoted)
        if self.server_state == State.RUNNING:
            return self.__get_resource_path_server_running(path_to_resource)
        elif self.server_state == State.MAINTENANCE:
            return self.maintenance_page_path

    def __get_resource_path_server_running(self, path_to_resource) -> str:
        if path_to_resource == self.root:
            return self.default_page_path
        if os.path.isfile(path_to_resource):
            return path_to_resource
        else:
            return self.resource_not_found_page_path
