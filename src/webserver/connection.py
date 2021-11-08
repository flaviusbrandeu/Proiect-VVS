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
        request = self.socket_connection.recv(MAX_REQUEST_LENGTH)
        requested_resource = self.__extract_requested_resource(request)
        filesystem = Filesystem(self.root_directory, self.default_page_path, self.server_state,
                                self.maintenance_page_path, self.resource_not_found_page_path)
        resource_path = filesystem.get_resource_path(requested_resource)
        print(resource_path)
        try:
            with open(resource_path, "rb") as resource:
                content = resource.read()
        except OSError:
            resource_path = self.resource_not_found_page_path
            with open(resource_path, "rb") as resource:
                content = resource.read()
        response_header = self.__get_response_header(resource_path)
        try:
            self.socket_connection.sendall(response_header)
            self.socket_connection.sendall(content)
            self.socket_connection.sendall(b"\r\n\r\n")
        except socket.error:
            print("[ERROR] Sending data failed")
        finally:
            self.socket_connection.close()

    @staticmethod
    def __extract_requested_resource(data: bytes) -> str:
        request_line_bytes, _ = data.split(b"\r\n", 1)
        requests_line = request_line_bytes.decode("ISO-8859-1")
        return urllib.parse.unquote((requests_line.split(" ")[1]))

    def __get_response_header(self, resource_path: str) -> bytes:
        if self.server_state == State.RUNNING:
            if resource_path == self.resource_not_found_page_path:
                return b"HTTP/1.1 404 Not Found\r\n\r\n"
            else:
                return b"HTTP/1.1 200 OK\r\n\r\n"
        elif self.server_state == State.MAINTENANCE:
            return b"HTTP/1.1 503 Service Unavailable\r\n\r\n"
