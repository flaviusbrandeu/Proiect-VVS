from src.webserver.state import State
from src.webserver.connection import Connection
import threading
import socket


class Webserver:
    def __init__(self, port, root_directory, default_page_path,
                 resource_not_found_page_path, maintenance_page_path):
        self.state = State.STOPPED
        self.port = port
        self.root_directory = root_directory
        self.default_page_path = default_page_path
        self.resource_not_found_page_path = resource_not_found_page_path
        self.maintenance_page_path = maintenance_page_path

    def start(self):
        addr = ('localhost', self.port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
        server.listen()
        self.state = State.RUNNING
        print(f"[LISTENING] Server is listening on {server.getsockname()}")
        try:
            while True:
                socket_connection, address = server.accept()
                connection = Connection(socket_connection, self.root_directory, self.state,
                                        self.default_page_path, self.resource_not_found_page_path,
                                        self.maintenance_page_path)
                thread = threading.Thread(target=connection.handle_request)
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        except Exception as exception:
            print(exception)
            print("[ERROR] Accept failed")
        finally:
            print("[CLOSING] Closing the socket")
            server.close()

    def stop(self):
        self.state = State.STOPPED

    def go_to_maintenance(self):
        self.state = State.MAINTENANCE
