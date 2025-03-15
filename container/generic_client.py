import tarfile
from io import BytesIO
import os
class GenericClient:
    def __init__(self):
        pass
    def run(self, command: str, install_command: str, output_file: str = "output.tar.gz", custom_download_path: bool = False) -> None:
        pass
    def __generate_tar__(self, tmpdirname: str, install_command: str, output_file: str):
        with tarfile.open(output_file, "w:gz") as tar:
                tar.add(tmpdirname, arcname=os.path.basename(tmpdirname))
                data = f'[install]\ninstall_command = {install_command}\ndirectory = {tmpdirname}'.encode('utf8')
                info = tarfile.TarInfo(name='install.ini')
                info.size = len(data)
                tar.addfile(tarinfo=info, fileobj=BytesIO(data))