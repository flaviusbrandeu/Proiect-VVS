from src.webserver.state import State


class Webserver:
    def __init__(self):
        pass

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def go_to_maintenance(self):
        raise NotImplementedError()
