import pytest
from unittest.mock import Mock, patch, mock_open, call, DEFAULT
from src.webserver.connection import Connection
from src.webserver.state import State
import socket
import os.path

# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
bin_html_content = b'''
    <html>
     <head>
      <title>Welcome!</title>
     </head>
     <body BGCOLOR="#FFFFFF" leftMargin=0 topMargin=0 rightMargin=0 marginheight="0" marginwidth="0">
      <center>
       Default page<br />
      </center>
     </body>
    </html>
    '''

# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
bin_maintenance_html_content = b'''
    <html>
     <head>
      <title>Maintenance</title>
     </head>
     <body BGCOLOR="#FFFFFF" leftMargin=0 topMargin=0 rightMargin=0 marginheight="0" marginwidth="0">
      <center>
       Server is in maintenance, please come back later<br />
      </center>
     </body>
    </html>
    '''

# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
bin_resource_not_found_html_content = b'''
    <html>
     <head>
      <title>Page not found</title>
     </head>
     <body BGCOLOR="#FFFFFF" leftMargin=0 topMargin=0 rightMargin=0 marginheight="0" marginwidth="0">
      <center>
       404 Not found
      </center>
     </body>
    </html>
    '''

# noinspection SpellCheckingInspection
request = b'GET /a/b/c.html HTTP/1.1\r\n' \
          b'Host: localhost:8080\r\n' \
          b'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0\r\n' \
          b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n' \
          b'Accept-Language: en-US,en;q=0.5\r\n' \
          b'Accept-Encoding: gzip, deflate\r\n' \
          b'DNT: 1\r\n' \
          b'Connection: keep-alive' \
          b'\r\n' \
          b'Upgrade-Insecure-Requests: 1' \
          b'\r\n' \
          b'Sec-Fetch-Dest: document' \
          b'\r\n' \
          b'Sec-Fetch-Mode: navigate' \
          b'\r\n' \
          b'Sec-Fetch-Site: none\r\n' \
          b'Sec-Fetch-User: ?1\r\n' \
          b'Cache-Control: max-age=0\r\n\r\n'

root_dir = "/home/user/website/www-root/"
default_page_path = "/home/user/website/www-root/index.html"
maintenance_page_path = "/home/user/website/www-root/maintenance.html"
resource_not_found_page_path = "/home/user/website/www-root/404.html"


@pytest.fixture
def f_connection_server_running():
    m_socket_connection = Mock()
    m_socket_connection.recv.return_value = request
    m_socket_connection.sendall = Mock()
    connection = Connection(m_socket_connection, root_dir, State.RUNNING,
                            default_page_path, resource_not_found_page_path, maintenance_page_path)
    return connection


@pytest.fixture
def f_connection_server_maintenance():
    m_socket_connection = Mock()
    m_socket_connection.recv.return_value = request
    m_socket_connection.sendall = Mock()
    m_socket_connection.close = Mock()
    connection = Connection(m_socket_connection, root_dir, State.MAINTENANCE,
                            default_page_path, resource_not_found_page_path, maintenance_page_path)
    return connection


class TestConnection:
    # noinspection PyUnusedLocal
    @patch("builtins.open", new_callable=mock_open, read_data=bin_html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_handle_request_resource_found(self, m_get_resource_path, m_open, f_connection_server_running):
        m_get_resource_path.return_value = os.path.join(root_dir, "a/b/c.html")
        f_connection_server_running.handle_request()
        expected_header = b"HTTP/1.1 200 OK\r\n\r\n"
        expected_calls = [call(expected_header), call(bin_html_content),
                          call(b'\r\n\r\n')]
        f_connection_server_running.socket_connection.sendall.assert_has_calls(expected_calls,
                                                                               any_order=False)
        f_connection_server_running.socket_connection.close.assert_called()

    # noinspection PyUnusedLocal
    @patch("builtins.open", new_callable=mock_open, read_data=bin_resource_not_found_html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_handle_request_resource_not_found(self, m_get_resource_path, m_open, f_connection_server_running):
        m_get_resource_path.return_value = resource_not_found_page_path
        f_connection_server_running.handle_request()
        expected_header = b"HTTP/1.1 404 Not Found\r\n\r\n"
        expected_calls = [call(expected_header), call(bin_resource_not_found_html_content),
                          call(b'\r\n\r\n')]
        f_connection_server_running.socket_connection.sendall.assert_has_calls(expected_calls,
                                                                               any_order=False)
        f_connection_server_running.socket_connection.close.assert_called()

    # noinspection PyUnusedLocal
    @patch('builtins.open', new_callable=mock_open, read_data=bin_maintenance_html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_handle_request_server_maintenance(self, m_get_resource_path, m_open, f_connection_server_maintenance):
        m_get_resource_path.return_value = maintenance_page_path
        f_connection_server_maintenance.handle_request()
        expected_header = b"HTTP/1.1 503 Service Unavailable\r\n\r\n"
        expected_calls = [call(expected_header), call(bin_maintenance_html_content),
                          call(b'\r\n\r\n')]
        f_connection_server_maintenance.socket_connection.sendall.assert_has_calls(expected_calls,
                                                                                   any_order=False)
        f_connection_server_maintenance.socket_connection.close.assert_called()

    # noinspection PyUnusedLocal
    @patch('builtins.open', new_callable=mock_open, read_data=bin_html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_connection_close_when_response_fail(self, m_get_resource_path, m_open, f_connection_server_running):
        m_get_resource_path.return_value = os.path.join(root_dir, "a/b/c.html")
        f_connection_server_running.socket_connection.sendall.side_effect = socket.error()
        f_connection_server_running.handle_request()
        f_connection_server_running.socket_connection.close.assert_called()

    @patch('builtins.open', new_callable=mock_open,
           read_data=bin_resource_not_found_html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_file_not_readable(self, m_get_resource_path, m_open, f_connection_server_running):
        m_open.side_effect = [OSError(), DEFAULT]
        m_get_resource_path.return_value = os.path.join(root_dir, "a/b/c/d.html")
        f_connection_server_running.handle_request()
        expected_header = b"HTTP/1.1 404 Not Found\r\n\r\n"
        expected_calls = [call(expected_header), call(bin_resource_not_found_html_content),
                          call(b'\r\n\r\n')]
        f_connection_server_running.socket_connection.sendall.assert_has_calls(expected_calls,
                                                                               any_order=False)
        f_connection_server_running.socket_connection.close.assert_called()
