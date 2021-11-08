import urllib.parse

import socket
from src.webserver.state import State
from src.filesystem.filesystem import Filesystem

MAX_REQUEST_LENGTH = 8192


class Connection:
    def __init__(self, connection, root_directory, server_state: State,
                 default_page_path, resource_not_found_page_path, maintenance_page_path):
        self.socket_connection = connection
        self.root_directory = root_directory
        self.server_state = server_state
        self.default_page_path = default_page_path
        self.resource_not_found_page_path = resource_not_found_page_path
        self.maintenance_page_path = maintenance_page_path

    def handle_request(self):
        raise NotImplementedError()

    def __get_request_header(self) -> str:
        # TODO: implement __get_request_header
        pass

    def __extract_requested_resource(self, header: str) -> str:
        # TODO: implement __get_requested_resource
        pass

    def __send_response(self):
        # TODO: implement __send_response
        pass
