from podman import PodmanClient as pc
import tempfile
import os
from container.generic_client import GenericClient
import shlex

class PodmanClient(GenericClient):
    def __init__(self, distro):
        self.distro = distro
    def run(self, command: str, install_command: str, output_file: str = "output.tar.gz", custom_download_path: bool = False):
        with tempfile.TemporaryDirectory() as tmpdirname:
            if custom_download_path:
                command = command.replace("$DOWNLOAD_DIR", tmpdirname)
            with pc() as client:
                print("Executing: ", command)
                mounts = [
                    {
                        "type": "bind",             
                        "source": tmpdirname,     
                        "target": tmpdirname, 
                        "read_only": False
                    }
                ]
                output = client.containers.run(
                    self.distro,
                    command=["bash", "-c", command],
                    mounts=mounts,
                    detach=False,
                    remove=True,  
                    workdir=tmpdirname
                )
                print(f"Container output: {output.decode('utf-8')}")
                self.__generate_tar__(tmpdirname, install_command, output_file)
