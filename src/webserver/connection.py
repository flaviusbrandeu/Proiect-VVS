import os
from src.webserver.webserver import State


class Connection:
    def __init__(self, connection, root_directory, server_state: State,
                 default_page, not_found_page, maintenance_page):
        self.socket_connection = connection
        self.root_directory = root_directory
        self.server_state = server_state
        self.default_page = default_page
        self.not_found_page = not_found_page
        self.maintenance_page = maintenance_page

    def handle_request(self):
        raise NotImplementedError()

    def __get_request_header(self):
        # TODO: implement __get_request_header
        pass

    def __get_requested_resource_path(self, header: str) -> str:
        # TODO: implement __get_requested_resource_path
        pass

    def __send_response(self):
        # TODO: implement __send_response
        pass
