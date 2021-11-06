from unittest.mock import patch
from src.webserver.webserver import State
from src.filesystem.filesystem import Filesystem
import pytest

root_dir = "/webserver/root/folder/"
default_page_path = "/webserver/root/folder/index.html"
maintenance_page_path = "/webserver/root/folder/maintenance.html"
resource_not_found_page_path = "/webserver/root/folder/404.html"


class TestFilesystem:
    @patch('os.path.isfile')
    def test_get_resource_root(self, m_isfile):
        m_isfile.return_value = True
        filesystem = Filesystem(root_dir, default_page_path, State.RUNNING,
                                maintenance_page_path, resource_not_found_page_path)
        path_to_resource = filesystem.get_resource_path("/")
        assert path_to_resource == default_page_path

    @patch('os.path.isfile')
    def test_get_resource_found(self, m_isfile):
        m_isfile.return_value = True
        filesystem = Filesystem(root_dir, default_page_path, State.RUNNING,
                                maintenance_page_path, resource_not_found_page_path)
        path_to_resource = filesystem.get_resource_path("/a/b/c.html")
        assert path_to_resource == "/webserver/root/folder/a/b/c.html"

    @patch('os.path.isfile')
    def test_get_resource_first_level(self, m_isfile):
        m_isfile.return_value = True
        filesystem = Filesystem(root_dir, default_page_path, State.RUNNING,
                                maintenance_page_path, resource_not_found_page_path)
        path_to_resource = filesystem.get_resource_path("/a.html")
        assert path_to_resource == "/webserver/root/folder/a.html"

    @patch('os.path.isfile')
    def test_get_resource_not_found(self, m_isfile):
        m_isfile.return_value = False
        filesystem = Filesystem(root_dir, default_page_path, State.RUNNING,
                                maintenance_page_path, resource_not_found_page_path)
        path_to_resource = filesystem.get_resource_path("/some/missing/resource.html")
        assert path_to_resource == resource_not_found_page_path

    def test_get_resource_server_maintenance(self):
        filesystem = Filesystem(root_dir, default_page_path, State.MAINTENANCE,
                                maintenance_page_path, resource_not_found_page_path)
        path_to_resource = filesystem.get_resource_path("/a/b/c.html")
        assert path_to_resource == maintenance_page_path
