import pytest
from unittest.mock import Mock, patch, mock_open
from src.webserver.connection import Connection
from src.webserver.webserver import State
import os.path

html_content = '''
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

maintenance_html_content = '''
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

resource_not_found_html_content = '''
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
    m_socket_connection.send_all = Mock()
    connection = Connection(m_socket_connection, root_dir, State.RUNNING,
                            default_page_path, resource_not_found_page_path, maintenance_page_path)
    return connection


@pytest.fixture
def f_connection_server_maintenance():
    m_socket_connection = Mock()
    m_socket_connection.recv.return_value = request
    m_socket_connection.send_all = Mock()
    connection = Connection(m_socket_connection, root_dir, State.MAINTENANCE,
                            default_page_path, resource_not_found_page_path, maintenance_page_path)
    return connection


class TestConnection:
    @patch("builtins.open", new_callable=mock_open, read_data=html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_handle_request_resource_found(self, m_get_resource_path, m_open, f_connection_server_running):
        m_get_resource_path.return_value = os.path.join(root_dir, "a/b/c.html")
        f_connection_server_running.handle_request()
        page_without_whitespaces = "".join(html_content.split())
        expected_response = f"HTTP/1.1 200 OK\n\n{page_without_whitespaces}"
        f_connection_server_running.socket_connection.send_all.assert_called_with(expected_response)

    @patch("builtins.open", new_callable=mock_open, read_data=resource_not_found_html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_handle_request_resource_not_found(self, m_get_resource_path, m_open, f_connection_server_running):
        m_get_resource_path.return_value = resource_not_found_page_path
        f_connection_server_running.handle_request()
        page_without_whitespaces = "".join(resource_not_found_html_content.split())
        expected_response = f"HTTP/1.1 404 Not Found\n\n{page_without_whitespaces}"
        f_connection_server_running.socket_connection.send_all.assert_called_with(expected_response)

    @patch('builtins.open', new_callable=mock_open, read_data=maintenance_html_content)
    @patch("src.filesystem.filesystem.Filesystem.get_resource_path")
    def test_handle_request_server_maintenance(self, m_get_resource_path, m_open, f_connection_server_maintenance):
        m_get_resource_path.return_value = maintenance_page_path
        f_connection_server_maintenance.handle_request()
        page_without_whitespaces = "".join(maintenance_html_content.split())
        expected_response = f"HTTP/1.1 503 Service Unavailable\n\n{page_without_whitespaces}"
        f_connection_server_maintenance.socket_connection.send_all.assert_called_with(expected_response)
