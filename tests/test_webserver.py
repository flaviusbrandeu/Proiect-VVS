import pytest
from unittest.mock import Mock, patch, mock_open, call, DEFAULT
from src.webserver.webserver import Webserver
from src.webserver.state import State
import socket
import os.path

root_dir = "/home/user/website/www-root/"
default_page_path = "/home/user/website/www-root/index.html"
maintenance_page_path = "/home/user/website/www-root/maintenance.html"
resource_not_found_page_path = "/home/user/website/www-root/404.html"


class TestWebserver:
    @patch('socket.socket.accept')
    @patch('src.webserver.connection.Connection.handle_request')
    def test_webserver_start(self, m_handle_request, m_accept):
        webserver = Webserver(8081, root_dir, default_page_path, resource_not_found_page_path,
                              maintenance_page_path)
        m_accept.side_effect = [(Mock(), Mock()), Exception()]
        webserver.start()
        assert webserver.state == State.RUNNING
        m_handle_request.assert_called_once()

    def test_webserver_stop(self):
        webserver = Webserver(8081, root_dir, default_page_path, resource_not_found_page_path,
                              maintenance_page_path)
        webserver.stop()
        assert webserver.state == State.STOPPED

    def test_webserver_maintenance(self):
        webserver = Webserver(8081, root_dir, default_page_path, resource_not_found_page_path,
                              maintenance_page_path)
        webserver.go_to_maintenance()
        assert webserver.state == State.MAINTENANCE
