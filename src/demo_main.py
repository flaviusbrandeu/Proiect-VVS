import os.path
from src.webserver.webserver import Webserver


def main():
    webserver = Webserver(8081, '/mnt/nvme0n1p6/Facultate/VVS/laborator/TestSite/',
                          '/mnt/nvme0n1p6/Facultate/VVS/laborator/TestSite/index.html',
                          '/mnt/nvme0n1p6/Facultate/VVS/laborator/TestSite/404.html',
                          '/mnt/nvme0n1p6/Facultate/VVS/laborator/TestSite/Maintenance.html')
    webserver.start()


if __name__ == "__main__":
    main()
