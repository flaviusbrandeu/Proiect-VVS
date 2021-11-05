from unittest.mock import patch
from src.webserver.webserver import State
from src.filesystem.filesystem import Filesystem


class TestFilesystem:
    @patch('os.path.isfile')
    def test_get_resource_root(self, m_isfile):
        m_isfile.return_value = True
        filesystem = Filesystem("/webserver/root/folder", "index.html", State.RUNNING,
                                "maintenance.html", "404.html")
        path_to_resource = filesystem.get_resource_path("/")
        assert path_to_resource == "/webserver/root/folder/index.html"

    @patch('os.path.isfile')
    def test_get_resource_found(self, m_isfile):
        m_isfile.return_value = True
        filesystem = Filesystem("/webserver/root/folder", "index.html", State.RUNNING,
                                "maintenance.html", "404.html")
        path_to_resource = filesystem.get_resource_path("/a/b/c.html")
        assert path_to_resource == "/webserver/root/folder/a/b/c.html"

    @patch('os.path.isfile')
    def get_resource_first_level(self, m_isfile):
        m_isfile.return_value = True
        filesystem = Filesystem("/webserver/root/folder", "index.html", State.RUNNING,
                                "maintenance.html", "404.html")
        path_to_resource = filesystem.get_resource_path("/a.html")
        assert path_to_resource == "/webserver/root/folder/a.html"

    @patch('os.path.isfile')
    def test_get_resource_not_found(self, m_isfile):
        m_isfile.return_value = False
        filesystem = Filesystem("/webserver/root/folder/", "index.html", State.RUNNING,
                                "maintenance.html", "error_pages/404.html")
        path_to_resource = filesystem.get_resource_path("/some/missing/resource.html")
        assert path_to_resource == "/webserver/root/folder/error_pages/404.html"

    def test_get_resource_server_maintenance(self):
        filesystem = Filesystem("/webserver/root/folder/", "index.html", State.MAINTENANCE,
                                "maintenance.html", "error_pages/404.html")
        path_to_resource = filesystem.get_resource_path("/a/b/c.html")
        assert path_to_resource == "/webserver/root/folder/maintenance.html"
