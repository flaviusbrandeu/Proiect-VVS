class Connection:
    def __init__(self, connection, root_directory):
        self.socket_connection = connection
        self.root_directory = root_directory

    def handle_request(self):
        raise NotImplementedError()

    def __get_request_header(self):
        # TODO: implement __get_request_header
        pass

    def __get_requested_resource_path(self, header: str) -> str:
        # TODO: implement __get_requested_resource_path
        pass

    def __get_resource_content(self, path: str) -> str:
        # TODO: implement __get_resource_content
        pass
    def __send_response(self):
        # TODO: implement __send_response
        pass
