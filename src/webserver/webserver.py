from enum import Enum, auto


class State(Enum):
    RUNNING = auto()
    MAINTENANCE = auto()
    STOPPED = auto()


class Webserver:
    def __init__(self):
        pass

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def go_to_maintenance(self):
        raise NotImplementedError()
