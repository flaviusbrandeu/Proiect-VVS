from enum import Enum, auto


class State(Enum):
    RUNNING = auto()
    MAINTENANCE = auto()
    STOPPED = auto()