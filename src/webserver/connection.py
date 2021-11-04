class Connection:
    def __init__(self, connection):
        self.connection = connection

    def handle_request(self):
        raise NotImplementedError()

    def __get_request_header(self):
        # TODO: implement __get_request_header
        pass

    def __get_requested_resource_path(self) -> str:
        # TODO: implement __get_requested_resource_path
        pass

    def __get_resource_content(self, path: str) -> str:
        # TODO: implement __get_resource_content
        pass
    def __send_response(self):
        # TODO: implement __send_response
        pass
